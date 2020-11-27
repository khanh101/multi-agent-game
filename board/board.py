from typing import Tuple, Union, List, Dict, Optional

import numpy as np

from board.controller import AutoController, Controller

Coord = Tuple[int, int]


class Board(object):
    shape: Tuple[int, int]  # hw
    obstacle_list: List[Coord]
    customer_list: List[Coord]
    salesman_list: List[Coord]

    # graph
    adj: np.ndarray
    index2coord: List[Tuple[int, int]]
    coord2index: Dict[Tuple[int, int], int]
    # controller cache
    last_path: Optional[List[List[Tuple[int, int]]]]

    def __init__(
            self,
            shape: Tuple[int, int],
            obstacle: Union[List[Coord], int],
            customer: Union[List[Coord], int],
            salesman: Union[List[Coord], int],
    ):
        super(Board, self).__init__()
        # shape
        self.shape = shape
        # obstacle
        if isinstance(obstacle, int):
            self.obstacle_list = Board.__random_mask(shape, obstacle)
        else:
            self.obstacle_list = obstacle
        # customer
        if isinstance(customer, int):
            self.customer_list = Board.__random_mask(shape, customer)
        else:
            self.customer_list = customer
        # salesman
        if isinstance(salesman, int):
            self.salesman_list = Board.__random_mask(shape, salesman)
        else:
            self.salesman_list = salesman
        # graph
        self.adj, self.index2coord, self.coord2index = Board.__create_graph(self.shape, self.obstacle_list)
        # cache controller
        self.last_path = None
        self.__ensure_valid()

    def control_auto(self, controller: AutoController):
        if self.last_path is None:
            salesman_index_path_list = controller(
                self.adj,
                [self.coord2index[coord] for coord in self.salesman_list],
                [self.coord2index[coord] for coord in self.customer_list],
            )
            salesman_path_list = []
            for index_path in salesman_index_path_list:
                salesman_path_list.append([self.index2coord[index] for index in index_path])
            self.last_path = salesman_path_list

        customer_reach = False
        for i, path in enumerate(self.last_path):
            if len(path) == 1:
                continue
            if len(path) == 2:
                customer_reach = True
                self.salesman_list[i] = path[-1]
                continue
            self.salesman_list[i] = path[1]
            self.last_path[i] = path[1:]
        if customer_reach:
            self.last_path = None

        self.__ensure_valid()

    def control_force(self, controller: Controller):
        self.salesman_list = controller(self.salesman_list)
        self.last_path = None
        self.__ensure_valid()


    def view(self) -> Tuple[List[Coord], List[Coord], List[Coord]]:
        return (
            self.obstacle_list,
            self.customer_list,
            self.salesman_list,
        )

    def __ensure_valid(self):
        # remove all invalid obstacle: outside of the map
        del_obstacle_indices = []
        for i, coord in enumerate(self.obstacle_list):
            if not self.__in_range(coord):
                del_obstacle_indices.append(i)
        del_obstacle_indices.reverse()
        for i in del_obstacle_indices:
            del self.obstacle_list[i]
        # remove all invalid salesman: outside of the map or on an obstacle
        del_salesman_indices = []
        for i, coord in enumerate(self.salesman_list):
            if (not self.__in_range(coord)) or (coord in self.obstacle_list):
                del_salesman_indices.append(i)
        del_salesman_indices.reverse()
        for i in del_salesman_indices:
            del self.salesman_list[i]
            if self.last_path is not None:
                del self.last_path[i]

        # remove all invalid customer: outside of the map or on an obstacle or a salesman
        del_customer_indices = []
        for i, coord in enumerate(self.customer_list):
            if (not self.__in_range(coord)) or (coord in self.obstacle_list) or (coord in self.salesman_list):
                del_customer_indices.append(i)
        del_customer_indices.reverse()
        for i in del_customer_indices:
            del self.customer_list[i]

    @staticmethod
    def __random_mask(shape: Tuple[int, int], count: int) -> List[Coord]:
        coord_list = []
        for h in range(shape[0]):
            for w in range(shape[1]):
                coord_list.append((h, w))
        indices = np.random.choice(range(len(coord_list)), size=(count,), replace=False)
        return [coord for i_c, coord in enumerate(coord_list) if i_c in indices]

    def __in_range(self, coord: Tuple[int,int]) -> bool:
        H, W = self.shape
        h, w = coord
        return h < H and h >= 0 and w < W and w >= 0

    @staticmethod
    def __create_graph(shape: Tuple[int, int], obstacle: List[Coord]) -> Tuple[
        np.ndarray, List[Coord], Dict[Coord, int]]:
        height, width = shape
        index2coord: List[Coord] = []
        coord2index: Dict[Coord, int] = {}
        for h in range(height):
            for w in range(width):
                if (h, w) not in obstacle:
                    index2coord.append((h, w))
                    coord2index[(h, w)] = len(index2coord) - 1
        num_nodes = len(index2coord)
        adj = np.zeros(shape=(num_nodes, num_nodes), dtype=bool)
        for index1 in range(num_nodes):
            h0, w0 = index2coord[index1]
            neighbours = [
                (h0 + 1, w0),
                (h0 - 1, w0),
                (h0, w0 + 1),
                (h0, w0 - 1),
            ]
            for h1, w1 in neighbours:
                if (h1, w1) in coord2index:
                    index2 = coord2index[(h1, w1)]
                    if index2 > index1:
                        adj[index1][index2] = True
                        adj[index2][index1] = True
        return adj, index2coord, coord2index

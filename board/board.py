from typing import Tuple, Union, List, Dict, Optional

import numpy as np

from board.auto_controller import auto_control

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
            obstacle: Union[List[Coord], float],
            customer: Union[List[Coord], float],
            salesman: Union[List[Coord], float],
    ):
        super(Board, self).__init__()
        # shape
        self.shape = shape
        # obstacle
        if isinstance(obstacle, float):
            self.obstacle_list = Board.__random_mask(shape, obstacle)
        else:
            self.obstacle_list = obstacle
        # customer
        if isinstance(customer, float):
            self.customer_list = Board.__random_mask(shape, customer)
        else:
            self.customer_list = customer
        # salesman
        if isinstance(salesman, float):
            self.salesman_list = Board.__random_mask(shape, salesman)
        else:
            self.salesman_list = salesman
        # graph
        self.adj, self.index2coord, self.coord2index = Board.__create_graph(self.shape, self.obstacle_list)
        # cache controller
        self.last_path = None
        self.__ensure_valid()

    def control_auto(self):
        if self.last_path is None:
            print("generated path")
            salesman_index_path_list = auto_control(
                self.adj,
                [self.coord2index[coord] for coord in self.salesman_list],
                [self.coord2index[coord] for coord in self.customer_list],
            )
            salesman_path_list = []
            for index_path in salesman_index_path_list:
                salesman_path_list.append([self.index2coord[index] for index in index_path])
            self.last_path = salesman_path_list

        print("cached path")
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
        pass

    def control_one(self, shift: str):
        shift_vector = {
            "w": (-1, 0),
            "s": (+1, 0),
            "a": (0, -1),
            "d": (0, +1),
        }
        if shift in shift_vector:
            first = self.salesman_list[0]
            new_first = (first[0] + shift_vector[shift][0], first[1] + shift_vector[shift][1])
            if not Board.__in_range(self.shape, new_first[0], new_first[1]):
                self.salesman_list = self.salesman_list[1:]
            else:
                self.salesman_list[0] = new_first
            self.__ensure_valid()

    def view(self) -> Tuple[List[Coord], List[Coord], List[Coord]]:
        return (
            self.obstacle_list,
            self.customer_list,
            self.salesman_list,
        )

    def __ensure_valid(self):
        obstacle = Board.__mask_to_array(self.shape, self.obstacle_list)
        customer = Board.__mask_to_array(self.shape, self.customer_list)
        salesman = Board.__mask_to_array(self.shape, self.salesman_list)
        salesman_bool = salesman.astype(bool)
        customer[salesman_bool] = 0  # if a salesman stands on a customer, remove customer
        cs = customer + salesman
        invalid = cs * obstacle
        invalid_bool = invalid.astype(bool)
        customer[invalid_bool] = 0  # if a salesman or a customer stands on a obstacle, remove it
        salesman[invalid_bool] = 0
        self.obstacle_list = Board.__array_to_mask(obstacle)
        self.customer_list = Board.__array_to_mask(customer)
        self.salesman_list = Board.__array_to_mask(salesman)

    @staticmethod
    def __array_to_mask(arr: np.ndarray) -> List[Coord]:
        mask = []
        for h in range(arr.shape[0]):
            for w in range(arr.shape[1]):
                for _ in range(arr[h, w]):
                    mask.append((h, w))
        return mask

    @staticmethod
    def __mask_to_array(shape: Tuple[int, int], mask: List[Coord]) -> np.ndarray:
        arr = np.zeros(shape=shape, dtype=int)
        for h, w in mask:
            arr[h, w] += 1
        return arr

    @staticmethod
    def __random_mask(shape: Tuple[int, int], prob: float) -> List[Coord]:
        mask_float = np.random.random(size=shape)
        mask = mask_float < prob
        out = []
        height, width = mask.shape
        for h in range(height):
            for w in range(width):
                if mask[h][w]:
                    out.append((h, w))
        return out

    @staticmethod
    def __in_range(shape: Tuple[int, int], h: int, w: int) -> bool:
        return h < shape[0] and h >= 0 and w < shape[1] and w >= 0

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

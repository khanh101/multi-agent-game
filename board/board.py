from typing import Tuple, Union, List

import numpy as np


class Board(object):
    shape: Tuple[int, int]
    obstacle: np.ndarray
    customer: np.ndarray
    salesman: np.ndarray

    def __init__(
            self,
            shape: Tuple[int, int],
            obstacle: Union[np.ndarray, float],
            customer: Union[np.ndarray, float],
            salesman: Union[np.ndarray, float],
    ):
        """
        :param shape: shape of the board
        :param obstacle: a mask of obstacle locations or probablity of a cell be an obstacle
        :param customer: a mask of customer locations or probabilty of a cell be a customer
        :param salesman: a mask of salesman locations or probability of a cell be a salesman
        """
        super(Board, self).__init__()
        # shape
        if shape[0] <= 0 and shape[1] <= 0:
            raise Exception("shape: invalid")
        self.shape = shape
        # obstacle
        if not isinstance(obstacle, np.ndarray):
            self.obstacle = Board.__random_mask(shape, obstacle)
        else:
            self.obstacle = obstacle
        # customer
        if not isinstance(customer, np.ndarray):
            self.customer = Board.__random_mask(shape, customer)
        else:
            self.customer = customer
        # salesman
        if not isinstance(salesman, np.ndarray):
            self.salesman = Board.__random_mask(shape, salesman)
        else:
            self.salesman = salesman

        self.__ensure_valid()

    def iterate(self):
        pass

    def obstacle_indices(self) -> List[Tuple[int, int]]:
        return Board.__mask_to_indices(self.obstacle)

    def customer_indices(self) -> List[Tuple[int, int]]:
        return Board.__mask_to_indices(self.customer)

    def salesman_indices(self) -> List[Tuple[int, int]]:
        return Board.__mask_to_indices(self.salesman)

    def __ensure_valid(self):
        # ensure there is no customer and salesman stands on the obstacle
        obstacle = self.obstacle
        customer = self.customer
        salesman = self.salesman
        cs = np.logical_or(customer, salesman)
        invalid = np.logical_and(cs, obstacle)
        self.customer[invalid] = False
        self.salesman[invalid] = False
        pass

    def __repr__(self) -> str:
        height, width = self.shape
        obstacle = self.obstacle
        customer = self.customer
        salesman = self.salesman

        def create_item(o: bool, c: bool, s: bool) -> str:
            out = ""
            if o:
                out += "O"
            else:
                out += " "
            if c:
                out += "C"
            else:
                out += " "
            if s:
                out += "S"
            else:
                out += " "
            return f"[{out}]"

        out = ""
        for row in range(height):
            line = ""
            for col in range(width):
                line += create_item(obstacle[row][col], customer[row][col], salesman[row][col]) + " "
            line += "\n"
            out += line
        return out

    @staticmethod
    def __random_mask(shape: Tuple[int, int], prob: float) -> np.ndarray:
        mask_arr_float = np.random.random(size=shape)
        mask_arr_bool = mask_arr_float < prob
        return mask_arr_bool

    @staticmethod
    def __mask_to_indices(mask: np.ndarray) -> List[Tuple[int, int]]:
        out = []
        height, width = mask.shape
        for h in range(height):
            for w in range(width):
                if mask[h][w]:
                    out.append((h, w))
        return out

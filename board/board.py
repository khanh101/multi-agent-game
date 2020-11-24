from typing import Tuple, Union

import numpy as np
import scipy as sp
import scipy.sparse

class Board(object):
    shape: Tuple[int, int]
    obstacle: sp.sparse.coo_matrix
    customer: sp.sparse.coo_matrix
    salesman: sp.sparse.coo_matrix
    def __init__(
            self,
            shape: Tuple[int, int],
            obstacle: Union[sp.sparse.coo_matrix, float],
            customer: Union[sp.sparse.coo_matrix, float],
            salesman: Union[sp.sparse.coo_matrix, float],
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
        if not isinstance(obstacle, sp.sparse.coo_matrix):
            self.obstacle = Board.__random_mask(shape, obstacle)
        else:
            self.obstacle = obstacle.copy()
        # customer
        if not isinstance(customer, sp.sparse.coo_matrix):
            self.customer = Board.__random_mask(shape, customer)
        else:
            self.customer = customer.copy()
        # salesman
        if not isinstance(salesman, sp.sparse.coo_matrix):
            self.salesman = Board.__random_mask(shape, salesman)
        else:
            self.salesman = salesman.copy()


    def __repr__(self) -> str:
        height, width = self.shape
        obstacle = self.obstacle.toarray()
        customer = self.customer.toarray()
        salesman = self.salesman.toarray()
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
    def __random_mask(shape: Tuple[int, int], prob: float) -> sp.sparse.coo_matrix:
        mask_arr_float = np.random.random(size=shape)
        mask_arr_bool = mask_arr_float < prob
        mask = sp.sparse.coo_matrix(mask_arr_bool)
        return mask

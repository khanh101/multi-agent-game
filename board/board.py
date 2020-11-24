from typing import Tuple, Union, List

import numpy as np

class Board(object):
    shape: Tuple[int, int] # hw
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

    def global_control(self, shift: str):
        shift_vector = {
            "w": (-1, 0),
            "s": (+1, 0),
            "a": (0, -1),
            "d": (0, +1),
        }
        self.salesman = Board.__2dshift(self.salesman, shift_vector[shift])
        self.__ensure_valid()

    def view(self) -> Tuple[str, List[Tuple[int, int]], List[Tuple[int, int]], List[Tuple[int, int]]]:
        win = np.sum(self.customer) == 0
        lose = np.sum(self.salesman) == 0
        state = ""
        if lose:
            state = "lose"
        if win:
            state = "win"

        return (
            state,
            Board.__mask_to_indices(self.obstacle),
            Board.__mask_to_indices(self.customer),
            Board.__mask_to_indices(self.salesman),
        )

    def __ensure_valid(self):
        # ensure there is no customer and salesman stands on the obstacle
        obstacle = self.obstacle
        customer = self.customer
        salesman = self.salesman
        self.customer[salesman] = False  # if a salesman stands on a customer, remove customer
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

    @staticmethod
    def __2dshift(arr: np.ndarray, shift: Tuple[int, int]) -> np.ndarray:
        out = np.zeros(shape=arr.shape, dtype=arr.dtype)
        for h in range(arr.shape[0]):
            for w in range(arr.shape[1]):
                h1 = h + shift[0]
                w1 = w + shift[1]
                if h1 < arr.shape[0] and h1 >= 0 and w1 < arr.shape[1] and w1 >= 0:
                    out[h1, w1] = arr[h, w]
        return out
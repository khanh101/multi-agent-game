from typing import Tuple, List, Optional

from algorithm.msoc import minimal_sum_of_costs_controller
from algorithm.gp import graph_partitioning_controller
from board.board import Board
from board.controller import AutoController
from game import game

import numpy as np

np.random.seed(1234)


def board_size(shape: Tuple[int, int]) -> int:
    return shape[0] * shape[1]


def play(shape: Tuple[int, int], cell_size: Tuple[int, int], init_salesman_list: List[Tuple[int, int]] = None,
         auto_controller: Optional[AutoController] = None):
    while True:
        if init_salesman_list is not None:
            board = Board(
                shape=shape,
                obstacle=int(0.1 * board_size(shape)),
                customer=int(0.05 * board_size(shape)),
                salesman=init_salesman_list,
            )
        else:
            board = Board(
                shape=shape,
                obstacle=int(0.1 * board_size(shape)),
                customer=int(0.05 * board_size(shape)),
                salesman=int(0.01 * board_size(shape)),
            )
        g = game.Game(board, cell_size)
        output = g.loop(auto_controller)
        if output == "r":
            continue
        break


def auto():
    play(
        shape=(45, 60),
        cell_size=(15, 15),
        init_salesman_list=None,
        auto_controller=minimal_sum_of_costs_controller,
        # auto_controller=graph_partitioning_controller,
    )


def single():
    play(
        shape=(15, 20),
        cell_size=(40, 40),
        init_salesman_list=[(0, 0)],
        auto_controller=None,
    )


if __name__ == "__main__":
    single()
    auto()

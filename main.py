from typing import Tuple

from algorithm.msoc import minimal_sum_of_costs_controller
from algorithm.gp import graph_partitioning_controller
from board.board import Board
from game import game

import numpy as np
np.random.seed(1234)

def board_size(shape: Tuple[int, int]) -> int:
    return shape[0] * shape[1]

def auto():
    while True:
        shape = (30, 40)
        board = Board(
            shape=shape,
            obstacle=int(0.1 * board_size(shape)),
            customer=int(0.05 * board_size(shape)),
            salesman=int(0.01 * board_size(shape)),
        )
        g = game.Game(board, (15, 15))
        output = g.loop(minimal_sum_of_costs_controller)
        # output = g.loop(graph_partitioning_controller)
        if output == "r":
            continue
        break



def single():
    while True:
        shape = (15, 20)
        board = Board(
            shape=shape,
            obstacle=int(0.1 * board_size(shape)),
            customer=int(0.05 * board_size(shape)),
            salesman=0,
        )
        try:
            board.obstacle_list.remove((0, 0))
        except ValueError as e:
            print(e)
        board.salesman_list = [(0, 0)]
        g = game.Game(board, (40, 40))
        output = g.loop()
        if output == "r":
            continue
        break


if __name__ == "__main__":
    single()
    auto()

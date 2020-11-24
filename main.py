import numpy as np

from board.board import Board
from game import game

shape = (30, 30)
board = Board(
    shape=shape,
    obstacle=0.1,
    customer=0.05,
    salesman=0.0,
)
board.obstacle[0, 0] = False
board.salesman[0, 0] = True

game = game.Game(board, (20, 20))

game.loop()
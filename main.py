from board.board import Board
from board_drawer import board_drawer
from game import game

board = Board(
    shape=(5, 5),
    obstacle=0.3,
    customer=0.1,
    salesman=0.1,
)
screen = board_drawer.screen_init(
    board.shape,
    (50, 50),
)
print(board)
game.loop(board_drawer.screen_update(board, screen))

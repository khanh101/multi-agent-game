from board.board import Board
from board_drawer import board_drawer

board = Board(
    shape=(5, 5),
    obstacle=0.3,
    customer=0.1,
    salesman=0.1,
)
game = board_drawer.Game(board)

game.loop()
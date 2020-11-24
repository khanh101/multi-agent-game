from board.board import Board
from game import game

shape = (30, 40)
board = Board(
    shape=shape,
    obstacle=0.1,
    customer=0.05,
    salesman=0.01,
)
'''
try:
    board.obstacle.remove((0, 0))
    board.customer.remove((0, 0))
except ValueError as err:
    print(err)
board.salesman = [(0, 0)]
'''
game = game.Game(board, (20, 20))

game.loop()

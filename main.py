from board.board import Board
from game import game

def auto():
    shape = (30, 40)
    board = Board(
        shape=shape,
        obstacle=0.1,
        customer=0.05,
        salesman=0.01,
    )
    g = game.Game(board, (20, 20))
    g.loop(single=False)

def single():
    shape = (15, 20)
    board = Board(
        shape=shape,
        obstacle=0.1,
        customer=0.05,
        salesman=0.01,
    )
    try:
        board.obstacle.remove((0, 0))
    except ValueError as e:
        print(e)
    board.salesman = [(0, 0)]
    g = game.Game(board, (40, 40))
    g.loop(single=True)

if __name__ == "__main__":
    single()

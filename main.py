from board.board import Board
from game import game

def main():
    shape = (30, 40)
    board = Board(
        shape=shape,
        obstacle=0.1,
        customer=0.05,
        salesman=0.01,
    )
    g = game.Game(board, (20, 20))
    g.loop()

if __name__ == "__main__":
    main()

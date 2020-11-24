from typing import Tuple, List

import pygame

from board.board import Board
from game import game


class Game(game.Game):
    board: Board
    cell_dim: Tuple[int, int]
    cell_size: Tuple[int, int]
    obstacle_surf: pygame.Surface = pygame.image.load("./board_drawer/assets/obstacle.png")
    customer_surf: pygame.Surface = pygame.image.load("./board_drawer/assets/customer.png")
    salesman_surf: pygame.Surface = pygame.image.load("./board_drawer/assets/salesman.png")

    def __init__(self, board: Board, cell_size: Tuple[int, int] = (50, 50)):
        height, width = board.shape
        c_height, c_width = cell_size
        super(Game, self).__init__(screen_size=(c_height * height, c_width * width))
        self.board = board
        self.cell_dim = board.shape
        self.cell_size = cell_size
        self.obstacle_surf = pygame.transform.scale(Game.obstacle_surf, cell_size)
        self.customer_surf = pygame.transform.scale(Game.customer_surf, cell_size)
        self.salesman_surf = pygame.transform.scale(Game.salesman_surf, cell_size)

    def loop(self):
        def update():
            self.screen.fill((255, 255, 255))
            self.screen.blits(
                self.__blits_sequence(self.board.obstacle_indices(), self.obstacle_surf),
                doreturn=False,
            )
            self.screen.blits(
                self.__blits_sequence(self.board.customer_indices(), self.customer_surf),
                doreturn=False,
            )
            self.screen.blits(
                self.__blits_sequence(self.board.salesman_indices(), self.salesman_surf),
                doreturn=False,
            )

        def callback():
            self.board.iterate()

        super(Game, self).loop(
            update=update,
            callback=callback,
        )
        pass

    def __blits_sequence(self, indices: List[Tuple[int, int]], surface: pygame.Surface) -> List[
        Tuple[pygame.Surface, pygame.Rect]]:
        c_height, c_width = self.cell_size
        sequence = []
        for h, w in indices:
            sequence.append(
                (surface, pygame.Rect((w * c_width, h * c_height), self.cell_size))
            )
        return sequence

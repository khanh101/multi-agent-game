from typing import Tuple, List

import pygame

from board.board import Board


class Game(object):
    board: Board
    cell_dim: Tuple[int, int]
    cell_size: Tuple[int, int]
    obstacle_surf: pygame.Surface = pygame.image.load("./game/assets/obstacle.png")
    customer_surf: pygame.Surface = pygame.image.load("./game/assets/customer.png")
    salesman_surf: pygame.Surface = pygame.image.load("./game/assets/salesman.png")
    screen: pygame.Surface

    def __init__(self, board: Board, cell_size: Tuple[int, int] = (50, 50)):
        self.board = board
        self.cell_dim = board.shape
        self.cell_size = cell_size
        self.obstacle_surf = pygame.transform.scale(Game.obstacle_surf, cell_size)
        self.customer_surf = pygame.transform.scale(Game.customer_surf, cell_size)
        self.salesman_surf = pygame.transform.scale(Game.salesman_surf, cell_size)
        height, width = board.shape
        c_height, c_width = cell_size
        screen_size = (c_height * height, c_width * width)
        self.screen = pygame.display.set_mode(size=screen_size)


    def loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
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
            pygame.display.flip()
        pygame.quit()
    def __blits_sequence(self, indices: List[Tuple[int, int]], surface: pygame.Surface) -> List[
        Tuple[pygame.Surface, pygame.Rect]]:
        c_height, c_width = self.cell_size
        sequence = []
        for h, w in indices:
            sequence.append(
                (surface, pygame.Rect((w * c_width, h * c_height), self.cell_size))
            )
        return sequence

from typing import Tuple, List

import pygame

from board.board import Board


class Game(object):
    board: Board
    cell_dim: Tuple[int, int] # wh
    cell_size: Tuple[int, int] # wh
    screen_size: Tuple[int, int] # wh
    obstacle_surf: pygame.Surface = pygame.image.load("./game/assets/obstacle.png")
    customer_surf: pygame.Surface = pygame.image.load("./game/assets/customer.png")
    salesman_surf: pygame.Surface = pygame.image.load("./game/assets/salesman.png")
    youwin_surf: pygame.Surface = pygame.image.load("./game/assets/youwin.png")
    youlose_surf: pygame.Surface = pygame.image.load("./game/assets/youlose.png")
    screen: pygame.Surface

    def __init__(self, board: Board, cell_size: Tuple[int, int] = (50, 50)):
        height, width = board.shape
        c_width, c_height = cell_size
        screen_size = (c_width * width, c_height * height)
        self.board = board
        self.cell_dim = board.shape[1], board.shape[0]
        self.cell_size = cell_size
        self.screen_size = screen_size
        self.obstacle_surf = pygame.transform.scale(Game.obstacle_surf, cell_size)
        self.customer_surf = pygame.transform.scale(Game.customer_surf, cell_size)
        self.salesman_surf = pygame.transform.scale(Game.salesman_surf, cell_size)
        self.youwin_surf = pygame.transform.scale(Game.youwin_surf, screen_size)
        self.youlose_surf = pygame.transform.scale(Game.youlose_surf, screen_size)
        self.screen = pygame.display.set_mode(size=screen_size)


    def loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.TEXTINPUT:
                    self.board.global_control(event.text)

            state, obstacle_indices, customer_indices, salesman_indices = self.board.view()
            if state == "win":
                self.screen.fill((255, 255, 255))
                self.screen.blit(self.youwin_surf, pygame.Rect((0, 0), self.screen_size))
            if state == "lose":
                self.screen.fill((255, 255, 255))
                self.screen.blit(self.youlose_surf, pygame.Rect((0, 0), self.screen_size))

            if state == "":
                self.screen.fill((255, 255, 255))
                self.screen.blits(
                    self.__blits_sequence(obstacle_indices, self.obstacle_surf),
                    doreturn=False,
                )
                self.screen.blits(
                    self.__blits_sequence(customer_indices, self.customer_surf),
                    doreturn=False,
                )
                self.screen.blits(
                    self.__blits_sequence(salesman_indices, self.salesman_surf),
                    doreturn=False,
                )

            pygame.display.flip()
        pygame.quit()
    def __blits_sequence(self, indices: List[Tuple[int, int]], surface: pygame.Surface) -> List[
        Tuple[pygame.Surface, pygame.Rect]]:
        # indices h w
        c_width, c_height = self.cell_size
        sequence = []
        for h, w in indices:
            sequence.append(
                (surface, pygame.Rect((w * c_width, h * c_height), self.cell_size))
            )
        return sequence

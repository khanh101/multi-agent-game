from typing import Tuple, List, Optional

import pygame

from board.board import Board
from board.controller import AutoController
from game.global_controller import global_control


def darken_and_blur(surface: pygame.Surface, amt: float = 30, opacity=200):
    if amt < 1.0:
        raise ValueError("Arg 'amt' must be greater than 1.0, passed in value is %s" % amt)
    surf = surface.copy()
    darken = pygame.Surface(surf.get_size())
    darken.fill((0, 0, 0))
    darken.set_alpha(opacity)
    surf.blit(darken, (0, 0))
    scale = 1.0 / float(amt)
    surf_size = surf.get_size()
    scale_size = (int(surf_size[0] * scale), int(surf_size[1] * scale))
    surf = pygame.transform.smoothscale(surf, scale_size)
    surf = pygame.transform.smoothscale(surf, surf_size)
    return surf


class Game(object):
    board: Board
    cell_dim: Tuple[int, int]  # wh
    cell_size: Tuple[int, int]  # wh
    screen_size: Tuple[int, int]  # wh
    obstacle_surf: pygame.Surface = pygame.image.load("./game/assets/obstacle.png")
    customer_surf: pygame.Surface = pygame.image.load("./game/assets/customer.png")
    salesman_surf: pygame.Surface = pygame.image.load("./game/assets/salesman.png")
    salesman_surf_left: pygame.Surface = pygame.image.load("./game/assets/salesman_left.png")
    salesman_surf_right: pygame.Surface = pygame.transform.flip(salesman_surf_left, True, False)
    youwin_surf: pygame.Surface = pygame.image.load("./game/assets/youwin_qr.png")
    youlose_surf: pygame.Surface = pygame.image.load("./game/assets/youlose_qr.png")
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
        self.salesman_surf_left = pygame.transform.scale(Game.salesman_surf_left, cell_size)
        self.salesman_surf_right = pygame.transform.scale(Game.salesman_surf_right, cell_size)
        self.youwin_surf = pygame.transform.scale(Game.youwin_surf, screen_size)
        self.youlose_surf = pygame.transform.scale(Game.youlose_surf, screen_size)
        self.screen = pygame.display.set_mode(size=screen_size)

    def loop(self, auto_controller: Optional[AutoController] = None) -> str:
        output = ""
        salesman_surf = self.salesman_surf
        state = ""
        running = True
        step = 0
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    output = "q"
                    running = False
                if event.type == pygame.TEXTINPUT:
                    if not (state == ""):
                        if event.text in ["r", "q"]:
                            output = event.text
                            running = False
                    else:
                        if auto_controller is None:
                            step += 1
                            self.board.control_force(global_control(event.text))
                            salesman_surf_dict = {
                                "a": self.salesman_surf_left,
                                "w": self.salesman_surf,
                                "d": self.salesman_surf_right,
                                "s": self.salesman_surf,
                            }
                            salesman_surf = salesman_surf_dict.get(event.text, salesman_surf)
            if not (state == ""):
                continue
            obstacle_indices, customer_indices, salesman_indices = self.board.view()
            win = len(customer_indices) == 0
            lose = len(salesman_indices) == 0
            state = ""
            if lose:
                state = "lose"
            if win:
                state = "win"

            if state == "win":
                self.screen.blit(darken_and_blur(self.screen), pygame.Rect((0, 0), self.screen_size))
                self.screen.blit(self.youwin_surf, pygame.Rect((0, 0), self.screen_size))
            if state == "lose":
                self.screen.blit(darken_and_blur(self.screen), pygame.Rect((0, 0), self.screen_size))
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
                    self.__blits_sequence(salesman_indices, salesman_surf),
                    doreturn=False,
                )

            pygame.display.flip()
            if auto_controller is not None and state == "":
                step += 1
                self.board.control_auto(auto_controller)
        pygame.quit()
        print(f"finished in {step} steps")
        return output

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

from enum import Enum
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
    gui: bool
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

    def __init__(self, board: Board, cell_size: Tuple[int, int] = None):
        self.board = board
        self.gui = cell_size is not None
        if self.gui:
            height, width = board.shape
            c_width, c_height = cell_size
            screen_size = (c_width * width, c_height * height)
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

    def get_salesman_surf(self, current: pygame.Surface, command: str) -> pygame.Surface:
        text2salesmandsurf = {
            "a": self.salesman_surf_left,
            "w": self.salesman_surf,
            "d": self.salesman_surf_right,
            "s": self.salesman_surf,
        }
        return text2salesmandsurf.get(command, current)

    def loop(self, auto_controller: Optional[AutoController] = None) -> str:
        class State(Enum):
            RUNNING = 0 # playing
            QUIT = 1 # quit
            ENDED = 2 # won or lost


        salesman_surf = self.salesman_surf
        num_steps = 0
        state: State = State.RUNNING
        return_msg: str = ""

        while state != State.QUIT:
            # event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    state = State.QUIT
                if event.type == pygame.TEXTINPUT:
                    if state == State.ENDED:
                        if event.text in ("r", "q"):
                            state = State.QUIT
                            return_msg = event.text
                    if state == State.RUNNING and auto_controller is None:
                        num_steps += 1
                        self.board.control_force(global_control(event.text))
                        text2salesmandsurf = {
                            "a": self.salesman_surf_left,
                            "w": self.salesman_surf,
                            "d": self.salesman_surf_right,
                            "s": self.salesman_surf,
                        }
                        salesman_surf = text2salesmandsurf.get(event.text, salesman_surf)
            #
            if state == State.RUNNING:
                # draw
                obstacle_list, customer_list, salesman_list = self.board.view()
                if len(customer_list) == 0:  # win
                    self.screen.blit(darken_and_blur(self.screen), pygame.Rect((0, 0), self.screen_size))
                    self.screen.blit(self.youwin_surf, pygame.Rect((0, 0), self.screen_size))
                    state = State.ENDED
                elif len(salesman_list) == 0:  # lose
                    self.screen.blit(darken_and_blur(self.screen), pygame.Rect((0, 0), self.screen_size))
                    self.screen.blit(self.youlose_surf, pygame.Rect((0, 0), self.screen_size))
                    state = State.ENDED
                else:  # running
                    self.screen.fill((255, 255, 255))
                    self.screen.blits(self.__blits_sequence(obstacle_list, self.obstacle_surf))
                    self.screen.blits(self.__blits_sequence(customer_list, self.customer_surf))
                    self.screen.blits(self.__blits_sequence(salesman_list, salesman_surf))

                pygame.display.flip()

                # control
                if auto_controller is not None:
                    num_steps += 1
                    self.board.control_auto(auto_controller)

        pygame.quit()
        print(f"finished in {num_steps} steps")
        return return_msg

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

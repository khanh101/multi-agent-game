from typing import Callable, Any, Tuple, List

import numpy as np
import pygame

from board.board import Board
from game import game


def screen_init(
        cell_dim: Tuple[int, int],
        cell_size: Tuple[int, int],
) -> pygame.Surface:
    global __obstacle, __customer, __salesman
    __obstacle = pygame.transform.scale(__obstacle, cell_size)
    __customer = pygame.transform.scale(__customer, cell_size)
    __salesman = pygame.transform.scale(__salesman, cell_size)
    global __cell_dim, __cell_size
    __cell_dim = cell_dim
    __cell_size = cell_size
    height, width = cell_dim
    c_height, c_width = cell_size
    screen_size = (c_height * height, c_width * width)
    return game.screen_init(screen_size=screen_size)


def screen_update(
        board: Board,
        screen: pygame.Surface,
) -> Callable[[], Any]:

    def update():
        screen.fill((255, 255, 255))
        # draw obstacle
        screen.blits(
            __blits_sequence(board.obstacle_indices(), __obstacle),
            doreturn= False,
        )
        # draw customer
        screen.blits(
            __blits_sequence(board.customer_indices(), __customer),
            doreturn= False,
        )
        # draw salesman
        screen.blits(
            __blits_sequence(board.salesman_indices(), __salesman),
            doreturn= False,
        )

    return update


__cell_dim: Tuple[int, int] = (0, 0)
__cell_size: Tuple[int, int] = (0, 0)

__obstacle: pygame.Surface = pygame.image.load("./board_drawer/assets/obstacle.png")
__customer: pygame.Surface = pygame.image.load("./board_drawer/assets/customer.png")
__salesman: pygame.Surface = pygame.image.load("./board_drawer/assets/salesman.png")


def __blits_sequence(indices: List[Tuple[int, int]], surface: pygame.Surface) -> List[Tuple[pygame.Surface, pygame.Rect]]:
    c_height, c_width = __cell_size
    sequence = []
    for h, w in indices:
        sequence.append(
            (surface, pygame.Rect((w * c_width, h * c_height), __cell_size))
        )
    return sequence

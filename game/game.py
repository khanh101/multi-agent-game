from typing import Tuple, Callable, Any

import pygame

pygame.init()


class Game(object):
    screen: pygame.Surface

    def __init__(self, screen_size: Tuple[int, int]):
        super(Game, self).__init__()
        self.screen = pygame.display.set_mode(size=screen_size)

    def loop(self, update: Callable[[], Any], callback: Callable[[], Any]):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            update()
            pygame.display.flip()
            callback()
        pygame.quit()

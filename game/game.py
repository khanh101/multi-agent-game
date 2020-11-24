from typing import Optional, Tuple, Callable, Any

import pygame
pygame.init()

screen: Optional[pygame.Surface] = None

def screen_init(screen_size: Tuple[int, int]) -> pygame.Surface:
    global screen
    screen = pygame.display.set_mode(size=screen_size)
    return screen

def loop(screen_update: Callable[[], Any]):
    running: bool = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen_update()

        pygame.display.flip()
    pygame.quit()

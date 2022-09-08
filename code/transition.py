import pygame
from settings import *


class Transition:
    def __init__(self, func, player=None):
        self.display_surface = pygame.display.get_surface()
        self.func = func
        self.player = player

        # overlay image
        self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.color = 255
        self.speed = -2

    def play(self):
        self.color += self.speed
        if self.color <= 0:
            self.speed *= -1
            self.color = 0
            self.func()
        if self.color > 255:
            self.color = 255
            self.speed = -2
            if self.player:
                self.player.sleep = False

        self.image.fill((self.color, self.color, self.color))
        self.display_surface.blit(
            self.image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT
        )


class DayTransition(Transition):
    def __init__(self, reset, player):
        super().__init__(reset, player)

    def play(self):
        super().play()

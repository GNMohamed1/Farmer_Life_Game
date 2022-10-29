from random import randint
import pygame, sys
from settings import *


class Partical(pygame.sprite.Sprite):
    def __init__(self, pos, groups, color, z=LAYERS["particals"]):
        super().__init__(groups)
        self.display = pygame.display.get_surface()
        self.z = z

        self.radius = 10
        self.pos_x = randint(pos[0] - 2, pos[0] + 2)
        self.pos_y = randint(pos[1] - 2, pos[1] + 2)

        self.color = color

        self.direction_x = randint(-40, 40)
        self.direction_y = randint(-40, 40)

        self.image = pygame.Surface((20, 20))
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))

    def update(self, dt):
        if self.radius < 0:
            self.kill()
            return
        self.pos_x += self.direction_x * dt
        self.pos_y += self.direction_y * dt
        self.radius -= 10 * dt
        self.image = pygame.Surface((self.radius * 2, self.radius * 2))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))

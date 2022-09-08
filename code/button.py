import pygame, sys
from settings import *


class Button(pygame.sprite.Sprite):
    def __init__(self, text, width, height, pos, func):
        # setup
        self.display_surf = pygame.display.get_surface()
        self.pos = pos
        self.func = func

        # graphics
        self.img = pygame.image.load("../graphics/ui/buttons/button.png")
        self.img = pygame.transform.scale(self.img, (width, height))
        self.rect = self.img.get_rect(topleft=pos)

        # text init
        self.font = pygame.font.Font("../font/forw.ttf", 32)
        self.text_surf = self.font.render(text, False, "White")
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

        # timer
        self.duraction = 200
        self.start_time = 0
        self.cycle = False

    def draw(self):
        self.display_surf.blit(self.img, self.rect)
        self.display_surf.blit(self.text_surf, self.text_rect)

    def timer(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.duraction:
            self.cycle = False

    def check_mouse(self):
        if self.cycle:
            self.timer()
        mouse_pos = pygame.mouse.get_pos()
        if (
            self.rect.collidepoint(mouse_pos)
            and pygame.mouse.get_pressed()[0]
            and not self.cycle
        ):
            self.start_time = pygame.time.get_ticks()
            self.cycle = True
            self.func()

    def update(self):
        self.draw()
        self.check_mouse()

import pygame

from settings import *


class Button(pygame.sprite.Sprite):
    def __init__(self, text, width, height, pos, func, img_path, font_path):
        # setup
        self.display_surf = pygame.display.get_surface()
        self.pos = pos
        self.func = func
        self.text = text

        # graphics
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(self.img, (width, height))
        self.rect = self.img.get_rect(topleft=pos)

        # text init
        self.font = pygame.font.Font(font_path, 32)
        self.text_surf = self.font.render(text, False, "White")
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

        # timer
        self.duration = 200
        self.start_time = -self.duration
        self.cycle = False

    def set_text(self, text):
        self.text = text
        self.text_surf = self.font.render(text, False, "White")
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self):
        self.display_surf.blit(self.img, self.rect)
        self.display_surf.blit(self.text_surf, self.text_rect)

    def check_mouse(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.start_time = pygame.time.get_ticks()
            self.cycle = True
            self.func()

        if self.cycle and pygame.time.get_ticks() - self.start_time >= self.duration:
            self.cycle = False

    def update(self, event):
        self.draw()
        self.check_mouse(event)

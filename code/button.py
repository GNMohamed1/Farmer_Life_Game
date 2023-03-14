import pygame
from settings import *

class Button(pygame.sprite.Sprite):
    def __init__(self, text, width, height, pos, func, img_path, font_path):
        super().__init__()
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
        self.hovered = False

    def set_text(self, text):
        self.text = text
        self.text_surf = self.font.render(text, False, "White")
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, surface):
        if self.hovered:
            surface.blit(pygame.transform.scale(self.img, (int(self.rect.width*1.1), int(self.rect.height*1.1))), (self.rect.x-int(self.rect.width*0.05), self.rect.y-int(self.rect.height*0.05)))
        else:
            surface.blit(self.img, self.rect)
        surface.blit(self.text_surf, self.text_rect)

    def check_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.hovered = True
        else:
            self.hovered = False

        if pygame.mouse.get_pressed()[0] and self.hovered:
            self.start_time = pygame.time.get_ticks()
            self.cycle = True
            self.func()

        if self.cycle and pygame.time.get_ticks() - self.start_time >= self.duration:
            self.cycle = False

    def update(self):
        self.check_mouse()
        self.draw(self.display_surf)

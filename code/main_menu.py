import pygame, sys
from settings import *
from button import Button


class MainMenu:
    def __init__(self, menu_start):
        # setup
        self.display_surf = pygame.display.get_surface()
        self.btn_width = 256
        self.btn_height = 128
        self.padding = ((SCREEN_WIDTH // 2) - self.btn_width // 2, self.btn_height)
        self.start = menu_start

        # buttons
        self.buttons = []
        self.setup()

    def exit(self):
        pygame.quit()
        sys.exit()

    def setup(self):
        # start button
        pos = (self.padding[0], 0)
        self.buttons.append(
            Button("Start", self.btn_width, self.btn_height, pos, self.start)
        )

        # exit button
        pos = (pos[0], pos[1] + self.padding[1])
        self.buttons.append(
            Button("Exit", self.btn_width, self.btn_height, pos, self.exit)
        )

    def update(self):
        for btn in self.buttons:
            if isinstance(btn, Button):
                btn.update()

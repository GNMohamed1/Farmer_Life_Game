import pygame, sys, time
from settings import *
from level import Level
from main_menu import MainMenu


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Stardew Vally Clone")
        self.clock = pygame.time.Clock()
        # self.level = Level()
        self.main_menu = MainMenu(self.menu_start)
        self.state = ["main menu", "level"]
        self.idx = 0
        self.level_init = False

    def level_fade(self):
        fade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        fade.fill((0, 0, 0))
        for alpha in range(300):
            fade.set_alpha(alpha)
            self.screen.fill("#DCDDDB")
            self.main_menu.update()
            self.screen.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(5)

        self.level = Level()
        self.level_init = True

        for alpha in range(300, 0, -1):
            fade.set_alpha(alpha)
            self.level.run(self.dt)
            self.screen.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(5)

    def menu_start(self):
        self.idx = 1

    def run(self):
        previous_time = time.time()
        while True:
            self.dt = time.time() - previous_time
            previous_time = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if self.state[self.idx] == "level":
                if not self.level_init:
                    self.level_fade()
                    self.level = Level()
                    self.level_init = True

                self.level.run(self.dt)
            else:
                self.screen.fill("#DCDDDB")
                self.main_menu.update()

            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()

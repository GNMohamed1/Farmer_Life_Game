import pygame, sys, time, threading
from settings import *
from level import Level
from menu import MainMenu
from animator import Animator
from bars import LoadingBar


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Stardew Vally Clone")
        self.clock = pygame.time.Clock()
        # self.level = Level()
        self.main_menu = MainMenu(self.menu_start)
        self.state = ["main menu", "level"]
        self.idx = 0
        self.level = None
        self.level_init = False
        self.main_menu_animator = Animator(self.main_menu, "main menu")
        self.basic = pygame.font.Font("../font/forw.ttf", 16)
        self.loading_bar = LoadingBar()

    def level_load(self):
        self.level = Level(True, self.loading_bar)

    def level_fade(self):
        fade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        fade.fill((0, 0, 0))
        for alpha in range(256):
            fade.set_alpha(alpha)
            self.screen.fill("#DCDDDB")
            self.main_menu.update()
            self.screen.blit(fade, (0, 0))
            pygame.display.update()

    def menu_start(self):
        self.idx = 1

    def run(self):
        once = False
        previous_time = time.time()
        thread = threading.Thread(target=self.level_load)

        while True:
            self.dt = time.time() - previous_time
            previous_time = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if self.state[self.idx] == "level":
                if not self.level_init and not once:
                    self.level_fade()
                    once = True
                    thread.start()
                if self.level is not None:
                    if self.loading_bar.couts < 120:
                        self.loading_bar.update()
                        self.level.trans = False
                    self.level.run(self.dt)
                else:
                    self.loading_bar.update()

            else:
                pos_y = SCREEN_HEIGHT // 2
                self.screen.fill("#DCDDDB")
                self.main_menu_animator.move(
                    [
                        (SCREEN_WIDTH // 2),
                        pos_y,
                    ],
                    speed=550,
                    dt=self.dt,
                    idx=0,
                )
                pos_y += self.main_menu.btn_height - 1
                self.main_menu_animator.move(
                    [
                        (SCREEN_WIDTH // 2),
                        (pos_y),
                    ],
                    speed=550,
                    dt=self.dt,
                    idx=1,
                )
                pos_y += self.main_menu.btn_height
                self.main_menu_animator.update()
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()

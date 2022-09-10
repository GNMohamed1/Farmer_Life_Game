import pygame, sys, time
from settings import *
from level import Level
from menu import MainMenu
from animator import Animator


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
        self.level_init = False
        self.main_menu_animator = Animator(self.main_menu, "main menu")
        self.basic = pygame.font.Font("../font/forw.ttf", 16)

    def level_fade(self):
        font = pygame.font.Font("../font/forw.ttf", 32)
        fade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        fade.fill((0, 0, 0))
        for alpha in range(256):
            fade.set_alpha(alpha)
            self.screen.fill("#DCDDDB")
            self.main_menu.update()
            self.screen.blit(fade, (0, 0))
            pygame.display.update()

        self.level = Level(True)
        self.level_init = True
        text_surf = font.render("Loading..", True, "White")

        for alpha in range(256, 0, -1):
            fade.set_alpha(alpha)
            self.level.run(self.dt)
            self.screen.blit(fade, (0, 0))
            pos_x = SCREEN_WIDTH // 2 - text_surf.get_width() // 2
            self.screen.blit(text_surf, (pos_x, 32))
            pygame.display.update()

        self.level.trans = False

    def menu_start(self):
        self.idx = 1

    def run(self):
        previous_time = time.time()

        while True:
            fps = self.clock.get_fps()
            self.dt = time.time() - previous_time
            previous_time = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if self.state[self.idx] == "level":
                if not self.level_init:
                    self.level_fade()

                self.level.run(self.dt)
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

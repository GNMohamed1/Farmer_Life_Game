import pygame, sys, time
from settings import *
from level import Level


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Stardew Vally Clone")
        self.clock = pygame.time.Clock()
        self.level = Level()

    def run(self):
        previous_time = time.time()
        while True:
            dt = time.time() - previous_time
            previous_time = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.level.run(dt)
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()

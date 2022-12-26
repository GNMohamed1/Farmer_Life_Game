import pygame
from settings import *


class LoadingBar:
    """
    The loading bar class. This class is used to display the loading bar during the loading of the game.
    """
    def __init__(self):
        self.display = pygame.display.get_surface()
        self.font = pygame.font.SysFont("Roboto", 128)
        self.bar_back = []
        self.bar_front = []
        self.seed_bar = []
        self.seed_bar_visible = False

        # add bars
        self.add_bars()

        # bar attribute
        self.pos = pygame.math.Vector2(0, 0)
        self.loading_finished = False
        self.loading_progress = 0
        self.finished = self.font.render("Ready!", False, "White")
        self.finished_rect = self.finished.get_rect(center=(640, 360))
        self.finished_couts = 0
        self.couts = -120

    def add_bars(self):
        # horse
        self.horse_surf = pygame.Surface((128, 64))
        self.horse_rect = self.horse_surf.get_rect(topleft=(0, SCREEN_HEIGHT - 128))
        self.horse_surf.fill("Blue")

        # farmer
        self.farmer_surf = pygame.Surface((64, 64))
        self.farmer_rect = self.farmer_surf.get_rect(topleft=(-64, SCREEN_HEIGHT - 128))
        self.farmer_surf.fill("Red")

        # back bar
        for i in range(SCREEN_WIDTH // TILE_SIZE):
            surf = pygame.image.load("../graphics/soil/x.png")
            rect = surf.get_rect(topleft=(i * TILE_SIZE, SCREEN_HEIGHT - TILE_SIZE))
            self.bar_back.append([surf, rect])
        # front bar
        for i in range(SCREEN_WIDTH // TILE_SIZE):
            surf = pygame.image.load("../graphics/test/Grass.png")
            rect = surf.get_rect(topleft=(i * TILE_SIZE, SCREEN_HEIGHT - TILE_SIZE))
            self.bar_front.append([surf, rect])

        # seed bar
        for i in range(SCREEN_WIDTH // TILE_SIZE):
            surf = pygame.image.load("../graphics/fruit/corn/0.png")
            rect = surf.get_rect(center=self.bar_back[i][1].center)
            self.seed_bar.append([surf, rect, False])

    def bar_draw(self):
        # Clear the Screen
        self.display.fill("Grey")
        # Checking for the seed bar
        if self.loading_progress > 50:
            # Turning the seed bar on
            self.seed_bar_visible = True
            # Move the seed bar
            self.pos.x = ((self.loading_progress - 50) / 100) * SCREEN_WIDTH * 2
            self.farmer_rect.x = self.pos.x
            for i in range(SCREEN_WIDTH // TILE_SIZE):
                if self.pos.x >= i * TILE_SIZE:
                    self.seed_bar[i][2] = True
                    continue
                break
        else:
            # Move the grass bar
            self.pos.x = (self.loading_progress / 100) * SCREEN_WIDTH * 2
            for idx, bar_front_list in enumerate(self.bar_front):
                bar_front_list[1].left = self.pos.x + (idx * TILE_SIZE)
            self.horse_rect.x = self.pos.x

        # Display the Changes
        self.display.blit(self.horse_surf, self.horse_rect)
        for bar_back_list in self.bar_back:
            self.display.blit(bar_back_list[0], bar_back_list[1])
        if self.seed_bar_visible:
            self.display.blit(self.farmer_surf, self.farmer_rect)
            for seed_bar_list in self.seed_bar:
                if seed_bar_list[2]:
                    self.display.blit(seed_bar_list[0], seed_bar_list[1])
                    continue
                break
            return
        for bar_front_list in self.bar_front:
            self.display.blit(bar_front_list[0], bar_front_list[1])

    def add_progress(self, amout):
        self.loading_progress += amout
        self.loading_progress = min(self.loading_progress, 100)

    def update(self):
        if not self.loading_finished:
            self.bar_draw()

        elif self.finished_couts < 25:
            self.bar_draw()
            self.finished_couts += 1

        else:
            self.couts += 1
            self.display.fill("Black")
            self.display.blit(self.finished, self.finished_rect)

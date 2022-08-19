import pygame
from settings import *


class Overlay:
    def __init__(self, player):
        # general setup
        self.display_surface = pygame.display.get_surface()
        self.player = player

        # imports
        overlay_path = "../graphics/overlay/"
        self.tools_surfs = {
            tool: pygame.image.load(f"{overlay_path}{tool}.png").convert_alpha()
            for tool in self.player.tools
        }
        self.seeds_surfs = {
            seed: pygame.image.load(f"{overlay_path}{seed}.png").convert_alpha()
            for seed in self.player.seeds
        }

    def display(self):

        # tool
        tool_surf = self.tools_surfs[self.player.selected_tool]
        tool_rect = tool_surf.get_rect(midbottom=OVERLAY_POSITIONS["tool"])
        self.display_surface.blit(tool_surf, tool_rect)

        # seed
        seed_surf = self.seeds_surfs[self.player.selected_seed]
        seed_rect = seed_surf.get_rect(midbottom=OVERLAY_POSITIONS["seed"])
        self.display_surface.blit(seed_surf, seed_rect)
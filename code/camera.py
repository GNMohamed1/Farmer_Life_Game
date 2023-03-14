import pygame
from settings import *

class CameraGroup(pygame.sprite.Group):
    """A custom Sprite group for camera movement

    Uses Layers as name "z" to view its sprite
    according to its Layer

    and Uses the player position to move the other sprites
    in the Screen
    """

    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        self.offset.x = player.rect.x - SCREEN_WIDTH / 2
        self.offset.y = player.rect.y - SCREEN_HEIGHT / 2

        for layer in LAYERS.values():
            for sprite in sorted(
                self.sprites(), key=lambda sprite: sprite.rect.centery
            ):
                if sprite.z == layer:
                    offset_rect = sprite.rect.move(-self.offset)
                    self.display_surface.blit(sprite.image, offset_rect)

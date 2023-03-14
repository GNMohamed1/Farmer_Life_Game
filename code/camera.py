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
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

        visible_sprites = []

        for sprite in self.sprites():
            if sprite.rect.colliderect(pygame.Rect((self.offset.x, self.offset.y), (SCREEN_WIDTH, SCREEN_HEIGHT))):
                visible_sprites.append(sprite)

        for layer in LAYERS.values():
            for sprite in sorted(visible_sprites, key=lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)
                    # if hasattr(sprite, 'hitbox'):
                    #     #pygame.draw.rect(self.display_surface, 'red', offset_rect, 5)
                    #     hitbox_rect = sprite.hitbox.copy()
                    #     hitbox_rect.center = offset_rect.center
                    #     pygame.draw.rect(self.display_surface,'green',hitbox_rect,5)

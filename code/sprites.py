from random import randint, choice
import pygame
from settings import *
from timer import Timer


class Generic(pygame.sprite.Sprite):
    def __init__(
        self, pos: tuple, surf: pygame.Surface, groups: list, z=LAYERS["main"]
    ):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate(
            -self.rect.width * 0.2, -self.rect.height * 0.75
        )


class Water(Generic):
    def __init__(self, pos: tuple, frames: list, groups):

        # Animation setup
        self.frames = frames
        self.frame_idx = 0

        # sprite setup
        super().__init__(pos, frames[self.frame_idx], groups, LAYERS["water"])

    def animate(self, dt):
        self.frame_idx += 5 * dt
        if self.frame_idx >= len(self.frames):
            self.frame_idx = 0
        self.image = self.frames[int(self.frame_idx)]

    def update(self, dt):
        self.animate(dt)


class WildFlower(Generic):
    def __init__(self, pos: tuple, surf: pygame.Surface, groups: list):
        super().__init__(pos, surf, groups)
        self.hitbox = self.rect.copy().inflate(-20, -self.rect.height * 0.9)


class Tree(Generic):
    def __init__(self, pos: tuple, surf: pygame.Surface, groups: list, name):
        super().__init__(pos, surf, groups)

        # tree attributes
        self.health = 5
        self.alive = True
        stump_path = f'../graphics/stumps/{"small" if name == "Small" else "large"}.png'
        self.stump_surf = pygame.image.load(stump_path).convert_alpha()
        self.invul_timer = Timer(200)

        # apple
        self.apple_surf = pygame.image.load("../graphics/fruit/apple.png")
        self.apples_pos = APPLE_POS[name]
        self.apple_sprites = pygame.sprite.Group()
        self.create_fruit()

    def damage(self):
        # Take Damage
        self.health -= 1

        # Destroy random apple
        if len(self.apple_sprites.sprites()) > 0:
            random_apple = choice(self.apple_sprites.sprites())
            random_apple.kill()

    def check_death(self):
        if self.health <= 0:
            self.image = self.stump_surf
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
            self.hitbox = self.rect.copy().inflate(-10, -self.rect.height * 0.6)
            self.alive = False

    def create_fruit(self):
        for pos in self.apples_pos:
            if randint(0, 10) < 2:
                x = pos[0] + self.rect.left
                y = pos[1] + self.rect.top
                Generic(
                    pos=(x, y),
                    surf=self.apple_surf,
                    groups=[self.apple_sprites, self.groups()[0]],
                    z=LAYERS["fruit"],
                )

    def update(self, dt):
        if self.alive:
            self.check_death()
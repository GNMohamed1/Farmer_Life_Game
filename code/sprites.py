from random import randint, choice
import pygame
from settings import *
from timer import Timer
from praticales import Partical


class Generic(pygame.sprite.Sprite):
    """
    Generic sprite class that can be used for any sprite that is not a player or enemy.
    @param pos - the position of the sprite in the game window.
    @param surf - the surface of the sprite.
    @param groups - the groups the sprite is in.
    @param z - the layer the sprite is in.
    """

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


class HouseWalls(pygame.sprite.Sprite):
    """
    Initialize the house walls.
    @param pos - the position of the house walls
    @param surf - the surface of the house walls
    @param groups - the groups the house walls are in
    @param z - the z layer of the house walls
    @param side - the side of the house walls
    """

    def __init__(
        self,
        pos: tuple,
        surf: pygame.Surface,
        groups: list,
        z=LAYERS["main"],
        side="center",
    ):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(
            topleft=pos
            if side == "center"
            else (pos[0] - 20, pos[1])
            if side == "right"
            else (pos[0] + 20, pos[1])
        )
        self.z = z
        self.hitbox = self.rect.copy().inflate(
            -self.rect.width * 0.52, -self.rect.height * 0.75
        )


class Interaction(Generic):
    """
    The interaction class is a generic class that is used to create the buttons and the           
    text boxes that are used throughout the program. It is a subclass of the generic class.
    @param pos - the position of the object (x,y)
    @param size - the size of the object (width, height)
    @param groups - the groups the object belongs to
    @param name - the name of the object
    """
    def __init__(self, pos: tuple, size, groups: list, name):
        surf = pygame.Surface(size)
        super().__init__(pos, surf, groups)
        self.name = name


class MaskPratical(Generic):
    """
    The mask practical class is a subclass of the Generic class. It is used to create a mask
    that is used to mask the background of the game. It is used to create a mask that is used
    to mask the background of the game. It is used to create a mask that is used to mask the
    background of the game. It is used to create a mask that is used to mask the background of
    the game. It is used to create a mask that is used to mask the background of the game.
    It is used to create a mask that is used to mask the background of the game. It is used to
    create a mask that is used to mask the background of the game. It is used to create
    """
    def __init__(
        self, pos: tuple, surf: pygame.Surface, groups: list, z, duraction=200
    ):
        super().__init__(pos, surf, groups, z)
        self.start_time = pygame.time.get_ticks()
        self.duraction = duraction

        # white Surface
        mask_surf = pygame.mask.from_surface(self.image)
        new_surf = mask_surf.to_surface()
        new_surf.set_colorkey((0, 0, 0))
        self.image = new_surf

    def update(self, dt):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.duraction:
            self.kill()


class Water(Generic):
    """
    The water class is a subclass of the Generic class. It is used to create water objects.
    @param pos - the position of the water object
    @param frames - the frames of the water object
    @param groups - the groups of the water object
    """
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
    """
    A class that represents a wild flower. The flower is a generic object that is drawn on the screen.
    @param pos - the position of the flower in the world.
    @param surf - the surface of the flower.
    @param groups - the groups the flower belongs to.
    """
    def __init__(self, pos: tuple, surf: pygame.Surface, groups: list):
        super().__init__(pos, surf, groups)
        self.hitbox = self.rect.copy().inflate(-20, -self.rect.height * 0.9)


class Tree(Generic):
    """
    The tree class. This class is used to represent the trees in the game. It is a subclass of the generic class.
    @param pos - the position of the tree in the game.
    @param surf - the surface of the tree.
    @param groups - the groups the tree is in.
    @param name - the name of the tree.
    @param player_add - the function to add the player's resources.
    @param data - the data of the tree.
    """
    def __init__(
        self, pos: tuple, surf: pygame.Surface, groups: list, name, player_add, data
    ):
        super().__init__(pos, surf, groups)

        # tree attributes
        self.data = data
        self.pos = pos
        self.surf = surf
        self.agroups = groups
        self.name = name
        self.health = data[0]
        self.alive = data[1]
        stump_path = f'../graphics/stumps/{"small" if name == "Small" else "large"}.png'
        self.stump_surf = pygame.image.load(stump_path).convert_alpha()
        self.invul_timer = Timer(200)

        # apple
        self.apple_surf = pygame.image.load("../graphics/fruit/apple.png")
        self.apples_pos = APPLE_POS[name]
        self.apple_sprites = pygame.sprite.Group()
        self.create_fruit()

        self.player_add = player_add
        self.day_passed = data[2]

        # sounds
        self.axe_sound = pygame.mixer.Sound("../audio/axe.mp3")

        # Particals
        self.particals = []

    def damage(self):
        # Take Damage
        self.health -= 1

        # Play Sound
        self.axe_sound.play()

        for _ in range(randint(5, 10)):
            self.particals.append(
                Partical(
                    self.rect.center, self.groups()[0], "brown", LAYERS["particals"]
                )
            )

        # Destroy random apple
        if len(self.apple_sprites.sprites()) > 0:
            random_apple = choice(self.apple_sprites.sprites())
            MaskPratical(
                pos=random_apple.rect.topleft,
                surf=random_apple.image,
                groups=self.groups()[0],
                z=LAYERS["fruit"],
            )
            self.player_add("apple", 1)
            random_apple.kill()

    def realive(self):
        self.health = 5

        self.image = self.surf
        self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        self.hitbox = self.rect.copy().inflate(-10, -self.rect.height * 0.6)
        self.alive = True
        self.create_fruit()

        self.day_passed = 0

    def check_death(self):
        if self.health <= 0:
            MaskPratical(
                self.rect.topleft, self.image, self.groups()[0], LAYERS["fruit"], 300
            )
            self.image = self.stump_surf
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
            self.hitbox = self.rect.copy().inflate(-10, -self.rect.height * 0.6)
            self.alive = False
            self.player_add("wood", 5)

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

    def reset(self):
        # destroying all apples
        for apple in self.apple_sprites.sprites():
            apple.kill()

        if not self.alive:
            self.day_passed += 1
            if self.day_passed >= 2:
                self.realive()
        else:
            self.create_fruit()

    def update(self, dt):
        if self.alive:
            self.check_death()
        for i in self.particals:
            i.update(dt)

    def load(self):
        if self.health <= 0:
            self.image = self.stump_surf
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
            self.hitbox = self.rect.copy().inflate(-10, -self.rect.height * 0.6)
            self.alive = False
            for apple in self.apple_sprites.sprites():
                apple.kill()

    def save(self):
        self.data = [self.health, self.alive, self.day_passed]

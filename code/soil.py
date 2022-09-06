from random import choice
import pygame
from settings import *
from pytmx.util_pygame import load_pygame
from support import *


class SoilTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS["soil"]


class WaterTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS["soil water"]


class Plant(pygame.sprite.Sprite):
    def __init__(self, plant_type, groups, soil, check_watered, player_add):
        super().__init__(groups)

        # setup
        self.plant_type = plant_type
        self.frames = import_folder(f"../graphics/fruit/{plant_type}")
        self.soil = soil
        self.check_watered = check_watered
        self.harvestable = False

        # plant growing
        self.age = 0
        self.max_age = len(self.frames) - 1
        self.grow_speed = GROW_SPEED[self.plant_type]

        # sprite setup
        self.image = self.frames[self.age]
        self.y_offset = -16 if plant_type == "corn" else -8
        self.rect = self.image.get_rect(
            midbottom=self.soil.rect.midbottom + pygame.math.Vector2(0, self.y_offset)
        )
        self.z = LAYERS["ground plant"]
        self.player_add = player_add

    def grow(self):
        if self.check_watered(self.rect.center):
            self.age += self.grow_speed

            if self.age > self.max_age:
                self.age = self.max_age
                self.harvestable = True
            self.image = self.frames[int(self.age)]
            self.rect = self.image.get_rect(
                midbottom=self.soil.rect.midbottom
                + pygame.math.Vector2(0, self.y_offset)
            )


class SoilLayer:
    def __init__(self, all_sprites, player_add):

        # sprite groups
        self.all_sprites = all_sprites
        self.soil_sprites = pygame.sprite.Group()
        self.soil_water_sprites = pygame.sprite.Group()
        self.plant_sprites = pygame.sprite.Group()

        # graphics
        self.soil_surfs = import_folder_dict("../graphics/soil/")
        self.watered_surfs = import_folder("../graphics/soil_water/")

        self.create_soil_grid()
        self.create_hit_rects()
        self.player_add = player_add

        # sounds
        self.hoe_sound = pygame.mixer.Sound("../audio/hoe.wav")
        self.hoe_sound.set_volume(0.1)

        self.plant_sound = pygame.mixer.Sound("../audio/plant.wav")
        self.plant_sound.set_volume(0.2)

    def create_soil_grid(self):
        ground = pygame.image.load("../graphics/world/ground.png")
        h_tiles, v_tiles = (
            ground.get_width() // TILE_SIZE,
            ground.get_height() // TILE_SIZE,
        )

        self.grid = [[[] for _ in range(h_tiles)] for _ in range(v_tiles)]
        for x, y, _ in (
            load_pygame("../data/map.tmx").get_layer_by_name("Farmable").tiles()
        ):
            self.grid[y][x].append("F")

    def create_hit_rects(self):
        self.hit_rects = []
        for row_idx, row in enumerate(self.grid):
            for col_idx, col in enumerate(row):
                if "F" in col:
                    x = col_idx * TILE_SIZE
                    y = row_idx * TILE_SIZE
                    rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    self.hit_rects.append(rect)

    def get_hit(self, point):
        for rect in self.hit_rects:
            if rect.collidepoint(point):
                self.hoe_sound.play()

                x = rect.x // TILE_SIZE
                y = rect.y // TILE_SIZE

                if "F" in self.grid[y][x]:
                    self.grid[y][x].append("X")
                    self.create_soil_tiles()
                    if self.raining:
                        self.water_all()

    def water(self, target_pos: tuple):
        for soil_sprite in self.soil_sprites.sprites():
            if soil_sprite.rect.collidepoint(target_pos):

                x = soil_sprite.rect.x // TILE_SIZE
                y = soil_sprite.rect.y // TILE_SIZE
                if "W" not in self.grid[y][x]:
                    # 1. add an entry to the soil grid -> "W"
                    self.grid[y][x].append("W")

                    # 2. Create a Water sprite
                    WaterTile(
                        pos=soil_sprite.rect.topleft,
                        surf=choice(self.watered_surfs),
                        groups=[self.all_sprites, self.soil_water_sprites],
                    )

    def water_all(self):
        for row_idx, row in enumerate(self.grid):
            for col_idx, col in enumerate(row):
                if "X" in col and "W" not in col:
                    col.append("W")
                    x = col_idx * TILE_SIZE
                    y = row_idx * TILE_SIZE
                    WaterTile(
                        (x, y),
                        choice(self.watered_surfs),
                        [self.all_sprites, self.soil_water_sprites],
                    )

    def remove_water(self):

        # destroy all water
        for sprite in self.soil_water_sprites.sprites():
            sprite.kill()

        # clean up the grid
        for row in self.grid:
            for col in row:
                if "W" in col:
                    col.remove("W")

    def check_watered(self, pos):
        x = pos[0] // TILE_SIZE
        y = pos[1] // TILE_SIZE

        col = self.grid[y][x]
        return "W" in col

    def plant_seed(self, target_pos, seed, outside=False):
        for soil_sprite in self.soil_sprites.sprites():
            if soil_sprite.rect.collidepoint(target_pos):

                self.plant_sound.play()

                x = soil_sprite.rect.x // TILE_SIZE
                y = soil_sprite.rect.y // TILE_SIZE

                if "P" not in self.grid[y][x]:
                    self.grid[y][x].append("P")
                    Plant(
                        seed,
                        [self.all_sprites, self.plant_sprites],
                        soil_sprite,
                        self.check_watered,
                        self.player_add,
                    )
                    if outside:
                        return True
                    break
                elif outside:
                    return False

                break

    def harvset_plant(self, target_pos):
        for plant_sprite in self.plant_sprites.sprites():
            if plant_sprite.rect.collidepoint(target_pos):
                x = plant_sprite.rect.x // TILE_SIZE
                y = plant_sprite.rect.x // TILE_SIZE

                if "P" in self.grid[y][x]:
                    self.grid[y][x].remove("P")
                    plant_sprite.harvset()

    def update_plants(self):
        for plant in self.plant_sprites.sprites():
            plant.grow()

    def create_soil_tiles(self):
        self.soil_sprites.empty()
        for row_idx, row in enumerate(self.grid):
            for col_idx, col in enumerate(row):
                if "X" in col:
                    t, b, r, l = False, False, False, False

                    if row_idx != 0:
                        t = "X" in self.grid[row_idx - 1][col_idx]
                    if row_idx != len(self.grid) - 1:
                        b = "X" in self.grid[row_idx + 1][col_idx]
                    if col_idx != 0:
                        l = "X" in row[col_idx - 1]
                    if row_idx != len(row) - 1:
                        r = "X" in row[col_idx + 1]

                    tile_type = self.tile_type_getter(t, b, r, l)

                    SoilTile(
                        pos=(col_idx * TILE_SIZE, row_idx * TILE_SIZE),
                        surf=self.soil_surfs[tile_type],
                        groups=[self.all_sprites, self.soil_sprites],
                    )

    def tile_type_getter(self, t, b, r, l) -> str:
        tile_type = "o"

        # all sides
        if all((t, r, b, l)):
            tile_type = "x"

        # horizontal tiles only
        if l and not any((t, r, b)):
            tile_type = "r"
        if r and not any((t, l, b)):
            tile_type = "l"
        if r and l and not any((t, b)):
            tile_type = "lr"

        # vertical only
        if t and not any((r, l, b)):
            tile_type = "b"
        if b and not any((r, l, t)):
            tile_type = "t"
        if b and t and not any((r, l)):
            tile_type = "tb"

        # corners
        if l and b and not any((t, r)):
            tile_type = "tr"
        if r and b and not any((t, l)):
            tile_type = "tl"
        if l and t and not any((b, r)):
            tile_type = "br"
        if r and t and not any((b, l)):
            tile_type = "bl"

        # T shapes
        if all((t, b, r)) and not l:
            tile_type = "tbr"
        if all((t, b, l)) and not r:
            tile_type = "tbl"
        if all((l, r, t)) and not b:
            tile_type = "lrb"
        if all((l, r, b)) and not t:
            tile_type = "lrt"

        return tile_type

import pygame
from settings import *
from pytmx.util_pygame import load_pygame
from support import import_folder_dict


class SoilTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS["soil"]


class SoilLayer:
    def __init__(self, all_sprites):

        # sprite groups
        self.all_sprites = all_sprites
        self.soil_sprites = pygame.sprite.Group()

        # graphics
        self.soil_surf = pygame.image.load("../graphics/soil/o.png")
        self.soil_surfs = import_folder_dict("../graphics/soil/")

        self.create_soil_grid()
        self.create_hit_rects()

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
                x = rect.x // TILE_SIZE
                y = rect.y // TILE_SIZE

                if "F" in self.grid[y][x]:
                    self.grid[y][x].append("X")
                    self.create_soil_tiles()

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

                    SoilTile(
                        pos=(col_idx * TILE_SIZE, row_idx * TILE_SIZE),
                        surf=self.soil_surfs[tile_type],
                        groups=[self.all_sprites, self.soil_sprites],
                    )

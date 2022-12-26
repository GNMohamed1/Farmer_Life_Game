from random import randint
import pygame
from sprites import MaskPratical
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic, Water, WildFlower, Tree, Interaction
from pytmx.util_pygame import load_pygame
from support import *
from transition import Transition
from soil import SoilLayer
from sky import Rain, Sky
from menu import ShopMenu, PauseMenu
from bars import LoadingBar
from camera import CameraGroup


class Level:
    def __init__(self, trans=False, loading_bar: LoadingBar = None):
        self.trans = trans
        self.loading_bar = loading_bar
        self.font = pygame.font.SysFont("Roboto", 64)

        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # Sprite Group
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.tree_sprites = pygame.sprite.Group()
        self.interaction_sprites = pygame.sprite.Group()

        self.loading_bar.add_progress(5)

        # Shop
        self.shop_active = False

        self.loading_bar.add_progress(5)

        # Setup
        self.data = load_file()
        self.loading_bar.add_progress(5)
        self.player_data = self.data["Player"]
        self.soil_layer = SoilLayer(
            self.all_sprites, self.player_add, self.data["Soil"], self.data["Plants"]
        )
        self.loading_bar.add_progress(5)
        self.setup()
        self.overlay = Overlay(self.player)
        self.transition = Transition(self.reset, self.player)
        self.loading_bar.add_progress(5)

        # sky
        self.rain = Rain(self.all_sprites)
        self.sky = Sky()
        self.raining = randint(0, 10) > 7
        self.soil_layer.raining = self.raining

        self.loading_bar.add_progress(5)

        # menu
        self.shop_menu = ShopMenu(self.player, self.toggle_shop)
        self.loading_bar.add_progress(5)

        # sounds
        self.success_sound = pygame.mixer.Sound("../audio/success.wav")
        self.success_sound.set_volume(0.3)

        self.bg_sound = pygame.mixer.Sound("../audio/bg.mp3")
        self.bg_sound.set_volume(0.1)
        self.bg_sound.play(loops=-1)

        self.sleep_music = pygame.mixer.Sound("../audio/music.mp3")
        self.sleep_music.set_volume(0.1)

        self.loading_bar.add_progress(5)

        # pause
        self.paused = False
        self.pause_menu = PauseMenu(self.continue_func)

        self.loading_bar.add_progress(5)

        # timer
        self.start_time = 0
        self.duraction = 200
        self.timer_cy = False
        self.trans = trans
        self.count = 0

        # load
        self.load()

        self.loading_bar.add_progress(5)
        self.loading_bar.loading_finished = True

    def continue_func(self):
        self.paused = not self.paused

    def setup(self):
        tmx_data = load_pygame("../data/map.tmx")

        # House
        for layer in ["HouseFloor", "HouseFurnitureBottom"]:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic(
                    (x * TILE_SIZE, y * TILE_SIZE),
                    surf,
                    self.all_sprites,
                    LAYERS["house bottom"],
                )

        self.loading_bar.add_progress(5)

        for layer in ["HouseWalls", "HouseFurnitureTop"]:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic(
                    (x * TILE_SIZE, y * TILE_SIZE),
                    surf,
                    self.all_sprites,
                )

        self.loading_bar.add_progress(5)

        # Fence
        for x, y, surf in tmx_data.get_layer_by_name("Fence").tiles():
            Generic(
                (x * TILE_SIZE, y * TILE_SIZE),
                surf,
                [self.all_sprites, self.collision_sprites],
            )

        self.loading_bar.add_progress(5)

        # Water
        water_frames = import_folder("../graphics/water")
        for x, y, surf in tmx_data.get_layer_by_name("Water").tiles():
            Water((x * TILE_SIZE, y * TILE_SIZE), water_frames, self.all_sprites)

        self.loading_bar.add_progress(5)

        # Tree
        for idx, obj in enumerate(tmx_data.get_layer_by_name("Trees")):
            Tree(
                pos=(obj.x, obj.y),
                surf=obj.image,
                groups=[self.all_sprites, self.collision_sprites, self.tree_sprites],
                name=obj.name,
                player_add=self.player_add,
                data=self.data["Trees"][idx],
            )

        self.loading_bar.add_progress(5)

        # Decoration
        for obj in tmx_data.get_layer_by_name("Decoration"):
            WildFlower(
                (obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites]
            )

        for x, y, surf in tmx_data.get_layer_by_name("Collision").tiles():
            Generic(
                (x * TILE_SIZE, y * TILE_SIZE),
                pygame.Surface((TILE_SIZE, TILE_SIZE)),
                self.collision_sprites,
            )

        self.loading_bar.add_progress(5)

        # Player
        self.player = Player(
            group=self.all_sprites,
            collision_sprites=self.collision_sprites,
            trees_sprites=self.tree_sprites,
            interaction=self.interaction_sprites,
            soil_layer=self.soil_layer,
            toggle_shop=self.toggle_shop,
            trans=self.trans,
            data=self.player_data,
        )

        self.loading_bar.add_progress(5)

        for obj in tmx_data.get_layer_by_name("Player"):
            # Bed
            if obj.name == "Bed":
                Interaction(
                    (obj.x, obj.y),
                    (obj.width, obj.height),
                    self.interaction_sprites,
                    obj.name,
                )

            self.loading_bar.add_progress(5)

            # Trader
            if obj.name == "Trader":
                Interaction(
                    (obj.x, obj.y),
                    (obj.width, obj.height),
                    self.interaction_sprites,
                    obj.name,
                )

            self.loading_bar.add_progress(5)

        Generic(
            pos=(0, 0),
            surf=pygame.image.load("../graphics/world/ground.png").convert_alpha(),
            groups=self.all_sprites,
            z=LAYERS["ground"],
        )

        self.loading_bar.add_progress(5)

    def player_add(self, item, amount):
        self.player.item_inventory[item] += amount
        self.success_sound.play()

    def toggle_shop(self):
        self.shop_active = not self.shop_active

    def reset(self):
        # plants
        self.soil_layer.update_plants()

        # soil
        self.soil_layer.remove_water()
        # Randmoize the rain
        self.raining = randint(0, 10) > 7
        self.soil_layer.raining = self.raining
        if self.raining:
            self.soil_layer.water_all()

        # apples on trees
        for tree in self.tree_sprites.sprites():
            tree.reset()
        # sky
        self.sky.start_color = [255, 255, 255]

    def plant_collision(self):
        if self.soil_layer.plant_sprites:
            for plant in self.soil_layer.plant_sprites.sprites():
                if plant.harvestable and plant.rect.colliderect(self.player.rect):
                    self.player_add(plant.plant_type, 3)
                    plant.kill()
                    MaskPratical(
                        plant.rect.topleft,
                        plant.image,
                        self.all_sprites,
                        LAYERS["main"],
                    )
                    x = plant.rect.centerx // TILE_SIZE
                    y = plant.rect.centery // TILE_SIZE
                    self.soil_layer.grid[y][x].remove("P")

    def timer(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.duraction:
            self.timer_cy = False

    def save(self):
        self.soil_layer.save()
        for idx, tree in enumerate(self.tree_sprites.sprites()):
            tree.save()
            self.data["Trees"][idx] = tree.data
        self.data["Player"] = self.player.data
        self.data["Soil"] = self.soil_layer.data_soil
        self.data["Plants"] = self.soil_layer.data_plants
        save_file(self.data)

    def load(self):
        self.soil_layer.load()
        for tree in self.tree_sprites.sprites():
            tree.load()

    def run(self, dt):
        if self.loading_bar.couts < 120:
            return
        self.player.trans = False
        keys = pygame.key.get_pressed()
        self.display_surface.fill("black")
        if self.timer_cy:
            self.timer()
        if keys[pygame.K_ESCAPE] and not self.timer_cy:
            self.start_time = pygame.time.get_ticks()
            self.timer_cy = True
            self.continue_func()
        self.all_sprites.custom_draw(self.player)
        if self.shop_active:
            self.shop_menu.update()
        elif self.paused:
            self.pause_menu.update()
        else:
            self.all_sprites.update(dt)
            self.plant_collision()
        self.overlay.display()
        if self.raining and not self.shop_active and not self.paused:
            self.rain.update()
        self.sky.display(dt)
        if self.player.sleep:
            self.save()
            self.transition.play()




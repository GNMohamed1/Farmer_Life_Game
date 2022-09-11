from random import randint
import pygame
from sprites import Partical
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


class Level:
    def __init__(self, trans=False):
        self.trans = trans

        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # Sprite Group
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.tree_sprites = pygame.sprite.Group()
        self.interaction_sprites = pygame.sprite.Group()

        # Shop
        self.shop_active = False

        # Setup
        self.data = load_file()
        self.player_data = self.data["Player"]
        self.soil_layer = SoilLayer(
            self.all_sprites, self.player_add, self.data["Soil"], self.data["Plants"]
        )
        self.soil_layer.load()
        self.setup()
        self.overlay = Overlay(self.player)
        self.transition = Transition(self.reset, self.player)

        # sky
        self.rain = Rain(self.all_sprites)
        self.sky = Sky()
        self.raining = randint(0, 10) > 7
        self.soil_layer.raining = self.raining

        # menu
        self.shop_menu = ShopMenu(self.player, self.toggle_shop)

        # sounds
        self.success_sound = pygame.mixer.Sound("../audio/success.wav")
        self.success_sound.set_volume(0.3)

        self.bg_sound = pygame.mixer.Sound("../audio/bg.mp3")
        self.bg_sound.set_volume(0.1)
        self.bg_sound.play(loops=-1)

        self.sleep_music = pygame.mixer.Sound("../audio/music.mp3")
        self.sleep_music.set_volume(0.1)

        # pause
        self.paused = False
        self.pause_menu = PauseMenu(self.continue_func)

        # timer
        self.start_time = 0
        self.duraction = 200
        self.timer_cy = False
        self.trans = trans
        self.count = 0

        for tree in self.tree_sprites.sprites():
            tree.load()

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

        for layer in ["HouseWalls", "HouseFurnitureTop"]:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic(
                    (x * TILE_SIZE, y * TILE_SIZE),
                    surf,
                    self.all_sprites,
                )

        # Fence
        for x, y, surf in tmx_data.get_layer_by_name("Fence").tiles():
            Generic(
                (x * TILE_SIZE, y * TILE_SIZE),
                surf,
                [self.all_sprites, self.collision_sprites],
            )

        # Water
        water_frames = import_folder("../graphics/water")
        for x, y, surf in tmx_data.get_layer_by_name("Water").tiles():
            Water((x * TILE_SIZE, y * TILE_SIZE), water_frames, self.all_sprites)

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

        # Player
        for obj in tmx_data.get_layer_by_name("Player"):
            # Player start
            if obj.name == "Start":
                self.player = Player(
                    pos=(obj.x, obj.y),
                    group=self.all_sprites,
                    collision_sprites=self.collision_sprites,
                    trees_sprites=self.tree_sprites,
                    interaction=self.interaction_sprites,
                    soil_layer=self.soil_layer,
                    toggle_shop=self.toggle_shop,
                    trans=self.trans,
                    data=self.player_data,
                )
            # Bed
            if obj.name == "Bed":
                Interaction(
                    (obj.x, obj.y),
                    (obj.width, obj.height),
                    self.interaction_sprites,
                    obj.name,
                )
            # Trader
            if obj.name == "Trader":
                Interaction(
                    (obj.x, obj.y),
                    (obj.width, obj.height),
                    self.interaction_sprites,
                    obj.name,
                )

        Generic(
            pos=(0, 0),
            surf=pygame.image.load("../graphics/world/ground.png").convert_alpha(),
            groups=self.all_sprites,
            z=LAYERS["ground"],
        )

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
            for apple in tree.apple_sprites.sprites():
                apple.kill()
            if not tree.alive:
                tree.day_passed += 1
                if tree.day_passed >= 2:
                    tree.realive()
            else:
                tree.create_fruit()

        # sky
        self.sky.start_color = [255, 255, 255]

    def plant_collision(self):
        if self.soil_layer.plant_sprites:
            for plant in self.soil_layer.plant_sprites.sprites():
                if plant.harvestable and plant.rect.colliderect(self.player.rect):
                    self.player_add(plant.plant_type, 3)
                    plant.kill()
                    Partical(
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
        self.data["Plant"] = self.soil_layer.data_plants
        save_file(self.data)

    def run(self, dt):
        if self.trans:
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


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

        for layer in LAYERS.values():
            for sprite in sorted(
                self.sprites(), key=lambda sprite: sprite.rect.centery
            ):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)

                    # debug
                    # if sprite == player:
                    #    pygame.draw.rect(self.display_surface, "red", offset_rect, 5)
                    #    hitbox_rect = player.hitbox.copy()
                    #    hitbox_rect.center = offset_rect.center
                    #    pygame.draw.rect(self.display_surface, "green", hitbox_rect, 5)
                    #    target_pos = (
                    #        offset_rect.center
                    #        + PLAYER_TOOL_OFFSET[player.status.split("_")[0]]
                    #    )
                    #    pygame.draw.circle(self.display_surface, "blue", target_pos, 5)

import pygame
from settings import *
from support import *
from timer import Timer
from sprites import HouseWalls


class Player(pygame.sprite.Sprite):
    def __init__(
        self,
        group: list,
        collision_sprites: pygame.sprite.Group,
        trees_sprites: pygame.sprite.Group,
        interaction: pygame.sprite.Group,
        soil_layer,
        toggle_shop,
        trans,
        data,
    ):
        super().__init__(group)

        # fixes bug
        self.trans = trans

        # load data
        self.data = data

        # Animations setup
        self.import_assets()
        self.status = data["status"]
        self.frame_idx = 0
        self.animation_speed = 4

        # Player setup
        self.image = self.animations[self.status][self.frame_idx]
        self.rect = self.image.get_rect(center=data["pos"])
        self.z = LAYERS["main"]

        # Collision
        self.hitbox = self.rect.copy().inflate(-126, -70)
        self.collision_sprites = collision_sprites

        # Movement attributies
        self.direction = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 300

        # Times
        self.timers = {
            "tool use": Timer(350, self.use_tool),
            "tool switch": Timer(200),
            "seed use": Timer(350, self.use_seed),
            "seed switch": Timer(200),
            "interact": Timer(200),
        }

        # Tool Use
        self.tools = self.data["tools"]
        self.tool_idx = self.data["tool_idx"]
        self.selected_tool = self.tools[self.tool_idx]

        # Seeds
        self.seeds = self.data["seeds"]
        self.seed_idx = self.data["seed_idx"]
        self.selected_seed = self.seeds[self.seed_idx]

        # interaction
        self.trees_sprites = trees_sprites
        self.interaction = interaction
        self.sleep = False
        self.soil_layer = soil_layer

        # Inventory
        self.item_inventory = self.data["item_inventory"]

        self.seed_inventory = self.data["seed_inventory"]
        self.toggle_shop = toggle_shop
        self.money = self.data["money"]

        # sound
        self.watering = pygame.mixer.Sound("../audio/water.mp3")
        self.watering.set_volume(0.2)

    def use_tool(self):
        if self.selected_tool == "hoe":
            self.soil_layer.get_hit(self.target_pos)
            self.soil_layer.harvset_plant(self.target_pos)

        if self.selected_tool == "axe":
            for tree in self.trees_sprites.sprites():
                if tree.rect.collidepoint(self.target_pos):
                    tree.damage()

        if self.selected_tool == "water":
            self.soil_layer.water(self.target_pos)
            self.watering.play()

    def get_target_pos(self):
        self.target_pos = (
            self.rect.center + PLAYER_TOOL_OFFSET[self.status.split("_")[0]]
        )

    def use_seed(self):
        if self.seed_inventory[self.selected_seed] > 0 and self.soil_layer.plant_seed(
            self.target_pos, self.selected_seed, True
        ):
            self.seed_inventory[self.selected_seed] -= 1

    def animate(self, dt):
        self.frame_idx += 4 * dt
        if self.frame_idx >= len(self.animations[self.status]):
            self.frame_idx = 0
        self.image = self.animations[self.status][int(self.frame_idx)]

    def import_assets(self):
        self.animations = {
            "up": [],
            "down": [],
            "left": [],
            "right": [],
            "up_idle": [],
            "down_idle": [],
            "left_idle": [],
            "right_idle": [],
            "up_hoe": [],
            "down_hoe": [],
            "left_hoe": [],
            "right_hoe": [],
            "up_axe": [],
            "down_axe": [],
            "left_axe": [],
            "right_axe": [],
            "up_water": [],
            "down_water": [],
            "left_water": [],
            "right_water": [],
        }

        for animation in self.animations:
            full_path = f"../graphics/character/{animation}"
            self.animations[animation] = import_folder(full_path)

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.timers["tool use"].active and not self.sleep and not self.trans:
            self.movement_input(keys)

            self.tool_inputs(keys)

            self.seed_inputs(keys)

            # interAct
            if keys[pygame.K_RETURN] and not self.timers["interact"].active:
                if collied_interaction_sprite := pygame.sprite.spritecollide(
                    self, self.interaction, False
                ):
                    if collied_interaction_sprite[0].name == "Trader":
                        self.timers["interact"].activate()
                        self.toggle_shop()
                    else:
                        self.timers["interact"].activate()
                        self.status = "left_idle"
                        self.sleep = True
                        self.save()

    def save(self):
        self.data = {
            "tools": self.tools,
            "tool_idx": self.tool_idx,
            "seeds": self.seeds,
            "seed_idx": self.seed_idx,
            "item_inventory": self.item_inventory,
            "seed_inventory": self.seed_inventory,
            "money": self.money,
            "pos": self.rect.center,
            "status": self.status,
        }

    def tool_inputs(self, keys):
        # Tool Use
        if keys[pygame.K_SPACE] or keys[pygame.K_LCTRL]:
            self.timers["tool use"].activate()
            self.direction = pygame.math.Vector2()
            self.frame_idx = 0

        # Tool Switch
        if keys[pygame.K_q] and not self.timers["tool switch"].active:
            self.timers["tool switch"].activate()
            self.tool_idx += 1
            if self.tool_idx >= len(self.tools):
                self.tool_idx = 0
            self.selected_tool = self.tools[self.tool_idx]

    def seed_inputs(self, keys):
        # Seed Use
        if keys[pygame.K_LALT]:
            self.timers["seed use"].activate()
            self.direction = pygame.math.Vector2()
            self.frame_idx = 0

        # Seed Switch
        if keys[pygame.K_c] and not self.timers["seed switch"].active:
            self.timers["seed switch"].activate()
            self.seed_idx += 1
            if self.seed_idx >= len(self.seeds):
                self.seed_idx = 0
            self.selected_seed = self.seeds[self.seed_idx]

    def movement_input(self, keys):
        # Vertical Movement
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
            self.status = "up"
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
            self.status = "down"
        else:
            self.direction.y = 0

        # Horizontal Movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.status = "left"
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.status = "right"
        else:
            self.direction.x = 0

    def get_states(self):
        # get idling player
        if self.direction.magnitude() == 0:
            self.status = self.status.split("_")[0] + "_idle"

        # Get Tool Using
        if self.timers["tool use"].active:
            self.status = self.status.split("_")[0] + "_" + self.selected_tool

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, "hitbox") and sprite.hitbox.colliderect(self.hitbox):
                if direction == "horizontal":
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
                    self.rect.centerx = self.hitbox.centerx
                    self.pos.x = self.hitbox.centerx
                elif direction == "vertical":
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
                    self.rect.centery = self.hitbox.centery
                    self.pos.y = self.hitbox.centery
    def move(self, dt):
        # Normalizing the vector
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
        # Horizontal Movement
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision("horizontal")

        # Vertical Movement
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision("vertical")

    def update(self, dt):
        self.input()
        self.move(dt)
        self.update_timers()
        self.get_states()
        self.animate(dt)
        self.get_target_pos()

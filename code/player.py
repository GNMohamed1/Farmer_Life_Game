import pygame
from settings import *
from support import *
from timer import Timer


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        # Animations setup
        self.import_assets()
        self.status = "down_idle"
        self.frame_idx = 0
        self.animation_speed = 4

        # Player setup
        self.image = self.animations[self.status][self.frame_idx]
        self.rect = self.image.get_rect(center=pos)

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
        }

        # Tool Use
        self.tools = ["axe", "hoe", "water"]
        self.tool_idx = 0
        self.selected_tool = self.tools[self.tool_idx]

        # Seeds
        self.seeds = ["corn", "tomato"]
        self.seed_idx = 0
        self.selected_seed = self.seeds[self.seed_idx]

    def use_tool(self):
        # print(self.selected_tool)
        pass

    def use_seed(self):
        pass

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

        if not self.timers["tool use"].active:
            self.movement_input(keys)

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

    def move(self, dt):
        # Normalizing the vector
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
        # Horizontal Movement
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x

        # Vertical Movement
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y

    def update(self, dt):
        self.input()
        self.move(dt)
        self.update_timers()
        self.get_states()
        self.animate(dt)

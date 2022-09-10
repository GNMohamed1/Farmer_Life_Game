import pygame
from settings import *
from button import Button


class Animator:
    def __init__(self, obj, type):
        self.obj = obj
        self.type = type
        self.obj_sub = []
        self.obj_contains()
        self.poses = [
            pygame.math.Vector2(self.obj_sub[0].rect.x, self.obj_sub[0].rect.y)
            for _ in range(len(self.obj_sub) + 1)
        ]

    def obj_contains(self):
        if self.type == "main menu":
            self.obj_sub.extend(iter(self.obj.buttons))

    def move(self, end_pos: list, speed: float, dt, idx):
        obj = self.obj_sub[idx]
        self.pos = self.poses[idx]
        if end_pos[0] > self.pos.x:
            self.pos.x += speed * dt
        if end_pos[0] < self.pos.x:
            self.pos.x -= speed * dt
        if end_pos[1] > self.pos.y:
            self.pos.y += speed * dt
        if end_pos[1] < self.pos.y:
            self.pos.y -= speed * dt
        obj.rect.topleft = (round(self.pos.x), round(self.pos.y))
        if isinstance(obj, Button):
            obj.text_rect.center = obj.rect.center

    def update(self):
        self.obj.update()

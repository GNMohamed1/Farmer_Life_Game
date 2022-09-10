import pygame
from settings import *
from button import Button


class Animator:
    def __init__(self, obj, type):
        self.obj = obj
        self.type = type
        self.obj_sub = []
        self.obj_contains()

    def obj_contains(self):
        if self.type == "main menu":
            self.obj_sub.extend(iter(self.obj.buttons))

    def move(self, end_pos: list, speed: float, dt, idx):
        obj = self.obj_sub[idx]
        pos = pygame.math.Vector2(obj.rect.center)
        if end_pos[0] > pos.x:
            pos.x += speed * dt
        if end_pos[0] < pos.x:
            pos.x -= speed * dt
        if end_pos[1] > pos.y:
            pos.y += speed * dt
        if end_pos[1] < pos.y:
            pos.y -= speed * dt
        obj.rect.center = (round(pos.x), round(pos.y))
        if isinstance(obj, Button):
            obj.text_rect.center = obj.rect.center

    def update(self):
        self.obj.update()

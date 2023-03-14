import pygame
from settings import *
from button import Button


class AnimatorMenu:
    def __init__(self, obj, type):
        self.obj = obj
        self.type = type
        self.obj_sub = list(obj.buttons)  # initialize obj_sub with contents of obj.buttons

    def move(self, end_pos: list, speed: float, dt, idx):
        obj = self.obj_sub[idx]
        pos = pygame.math.Vector2(obj.rect.center)
        direction = pygame.math.Vector2(end_pos) - pos
        distance = direction.length()
        if distance > 0:
            direction.normalize_ip()
            pos += direction * min(distance, speed * dt)
            obj.rect.center = (round(pos.x), round(pos.y))
            if isinstance(obj, Button):
                obj.text_rect.center = obj.rect.center


    def update(self):
        self.obj.update()


class AnimatorSprite:
    def __init__(self, sprite):
        self.sprite = sprite
        self.animations = {}
        
    def add_animation(self, name, frames, fps):
        self.animations[name] = {
            "frames": frames,
            "fps": fps,
            "index": 0,
            "timer": 0
        }
        
    def play_animation(self, name, loop=True):
        if name not in self.animations:
            print(f"Error: Animation '{name}' not found for sprite '{self.sprite}'")
            return
        
        self.sprite.image = self.animations[name]["frames"][self.animations[name]["index"]]
        self.animations[name]["timer"] += pygame.time.get_ticks()
        
        if self.animations[name]["timer"] >= 1000 / self.animations[name]["fps"]:
            self.animations[name]["index"] += 1
            self.animations[name]["timer"] = 0
            
            if self.animations[name]["index"] >= len(self.animations[name]["frames"]):
                if loop:
                    self.animations[name]["index"] = 0
                else:
                    self.animations[name]["index"] = len(self.animations[name]["frames"]) - 1
    
    def move(self, end_pos: tuple, speed: float, dt):
        pos = pygame.math.Vector2(self.sprite.rect.center)
        end_pos = pygame.math.Vector2(end_pos)
        distance = end_pos - pos
        
        if distance.length() > 0:
            direction = distance.normalize()
            displacement = direction * speed * dt
            if displacement.length() >= distance.length():
                self.sprite.rect.center = (round(end_pos.x), round(end_pos.y))
            else:
                pos += displacement
                self.sprite.rect.center = (round(pos.x), round(pos.y))
        
    def update(self):
        for animation in self.animations.values():
            self.play_animation(animation)

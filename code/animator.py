import pygame
import math
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
            distance_to_travel = min(distance, speed * dt)
            eased_distance = self.ease_out(distance_to_travel / distance)
            pos += direction * (eased_distance * distance)
            obj.rect.center = (round(pos.x), round(pos.y))
            if isinstance(obj, Button):
                obj.text_rect.center = obj.rect.center
    
    def ease_out(self, t):
        return math.sin(t * math.pi / 2)

    def update(self):
        self.obj.update()



class AnimatorSprite:
    def __init__(self, sprite):
        """
        Initialize the AnimatorSprite object with a sprite.

        Args:
        sprite: The sprite object to be animated.
        """
        self.sprite = sprite
        self.animations = {}
        self.idx = 0

    def add_animation(self, name, frames, fps):
        """
        Add an animation to the sprite.

        Args:
        name: The name of the animation.
        frames: A list of surfaces representing each frame of the animation.
        fps: The number of frames per second to play the animation at.
        """
        self.animations[name] = {
            "frames": frames,
            "fps": fps,
            "index": 0,
            "timer": 0
        }

    def play_animation(self, name, dt=0.1, loop=True):
        """
        Play an animation on the sprite.

        Args:
        name: The name of the animation to play.
        loop: Whether or not to loop the animation.

        Returns:
        None
        """
        if name not in self.animations.keys():
            print(f"Error: Animation '{name}' not found for sprite '{self.sprite}'")
            return

        self.sprite.image = self.animations[name]["frames"][self.animations[name]["index"]]
        self.animations[name]["timer"] += pygame.time.get_ticks()

        if self.animations[name]["timer"] >= 1000 / (self.animations[name]["fps"] * dt):
            self.animations[name]["index"] += 1
            self.animations[name]["timer"] = 0

            if self.animations[name]["index"] >= len(self.animations[name]["frames"]):
                if loop:
                    self.animations[name]["index"] = 0
                else:
                    self.animations[name]["index"] = len(self.animations[name]["frames"]) - 1

    def move(self, end_pos: tuple, speed: float, dt):
        """
        Move the sprite to a new position.

        Args:
        end_pos: The end position to move the sprite to.
        speed: The speed at which to move the sprite.
        dt: The time since the last update.

        Returns:
        None
        """
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
        """
        Update the sprite's animation.

        Args:
        None

        Returns:
        None
        """
        for animation in self.animations.keys():
            self.play_animation(animation)
 
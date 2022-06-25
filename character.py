from engine import utils
from engine.entity import Entity
from engine.graphics.animations import AnimManager
from engine.state import Game
import pygame
from engine.input import Input, Key

class Character(Entity):
    MAX_SPEED = 2

    def __init__(self, pos, name):
        img = AnimManager.anim_data["run"].images[0]
        self.on_ground = False
        super().__init__(pos, (img.get_width() / 16, img.get_height() / 16), name, static_img=img)

    def update(self, tilemap):
        self.move()
        self.rigidbody.velocity.x = utils.clamp(self.rigidbody.velocity.x, -Character.MAX_SPEED, Character.MAX_SPEED)
        self.on_ground = False
        super().update(tilemap)

    def on_collision(self, collisions, collision_dirs):
        if collision_dirs["bottom"]:
            self.on_ground = True

    def move(self):
        speed = 4 * Game.dt
        movement = pygame.Vector2()
        if Input.key_down(Key.SPACE) and self.on_ground:
            self.rigidbody.add_vel(pygame.Vector2(0, -0.3))
        if Input.key_down(Key.a):
            movement.x -= speed
        if Input.key_down(Key.d):
            movement.x += speed
        self.rigidbody.add_vel(movement)
        if movement.length() == 0:
            self.sprite.set_anim(None)
        elif self.sprite.current_animation is None:
            self.sprite.set_anim("run")
        self.sprite.flip[0] = movement.x < 0

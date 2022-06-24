import math

import pygame
from pygame.locals import *

from engine.graphics import Camera, animations
from engine import Entity
from engine.input import Input, Key
from engine.state import Game, Scene
from engine.tile import TileMap


class MainScene(Scene):
    def __init__(self):
        super().__init__()
        s = animations.AnimManager.anim_data["run"].images[0].get_size()
        self.player = Entity((0, 0), (s[0]/16, s[1]/16), "player", static_img=animations.AnimManager.anim_data["run"].images[0])
        self.player.sprite.set_anim("run")
        self.game_surf = pygame.Surface(Game.screen_size * 0.3)
        self.ui_surf = pygame.Surface(Game.screen_size / 3, flags=SRCALPHA)
        self.tm = TileMap("assets/test.tmx")
        self.camera = Camera((10, 10), pygame.Vector2(self.game_surf.get_size()) / 16, (16, 16))

    def update(self):
        if Input.key_down(Key.ESCAPE):
            Game.quit()
        speed = 5*Game.dt
        movement = pygame.Vector2()
        if Input.key_down(Key.SPACE) and self.player.on_ground:
            self.player.rigidbody.add_vel(pygame.Vector2(0, -0.5))
        if Input.key_down(Key.a):
            movement.x -= speed
        if Input.key_down(Key.d):
            movement.x += speed
        if movement.length() == 0:
            self.player.sprite.set_anim(None)
        elif self.player.sprite.current_animation is None:
            self.player.sprite.set_anim("run")
        self.player.sprite.flip[0] = movement.x < 0
        self.player.rigidbody.move(movement)
        self.player.update(self.tm)
        self.camera.lerp_to(self.player.pos, min(1, 5*Game.dt))

    def render(self):
        self.game_surf.fill(0)
        self.tm.render(self.game_surf, self.camera)
        self.player.render(self.game_surf, self.camera)

        # pygame.draw.circle(self.game_surf, (255, 0, 0), (self.game_surf.get_width()//2, self.game_surf.get_height()//2), 2)
        # pygame.draw.rect(self.game_surf, (0, 0, 255), (self.camera.project((self.player.rect.x, self.player.rect.y)), (self.player.rect.width*16, self.player.rect.height*16)))
        Game.display.blit(pygame.transform.scale(self.ui_surf, Game.screen_size), (0,0))
        Game.display.blit(pygame.transform.scale(self.game_surf, Game.screen_size), (0,0))

        pygame.display.flip()

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
        self.player = Entity((10, 10), (s[0]/16, s[1]/16), "player", static_img=animations.AnimManager.anim_data["run"].images[0])
        self.player.sprite.set_anim("run")
        self.game_surf = pygame.Surface(Game.screen_size * 0.3)
        self.ui_surf = pygame.Surface(Game.screen_size / 3, flags=SRCALPHA)
        self.tm = TileMap("assets/test.tmx")
        self.camera = Camera((10, 10), pygame.Vector2(self.game_surf.get_size()) / 16, (16, 16))

    def update(self):
        if Input.key_down(Key.ESCAPE):
            Game.quit()
        cam_speed = 5*Game.dt
        movement = pygame.Vector2()
        if Input.key_down(Key.w):
            movement.y -= cam_speed
        if Input.key_down(Key.s):
            movement.y += cam_speed
        if Input.key_down(Key.a):
            movement.x -= cam_speed
        if Input.key_down(Key.d):
            movement.x += cam_speed
        if movement.length() == 0:
            self.player.sprite.set_anim(None)
        elif self.player.sprite.current_animation is None:
            self.player.sprite.set_anim("run")
        self.player.sprite.flip[0] = movement.x < 0
        self.camera.center += movement
        self.player.pos = self.camera.center
        self.player.sprite.update()

    def render(self):
        self.game_surf.fill(0)
        self.tm.render(self.game_surf, self.camera)
        self.player.render(self.game_surf, self.camera)
        # Use for debugging to find 0, 0
        pygame.draw.circle(self.game_surf, (255, 0, 0), self.camera.project(self.player.rect.center), 4)
        Game.display.blit(pygame.transform.scale(self.ui_surf, Game.screen_size), (0,0))
        Game.display.blit(pygame.transform.scale(self.game_surf, Game.screen_size), (0,0))

        pygame.display.flip()

import pygame
from pygame.locals import *

from engine.graphics import animations, Camera
import engine.utils
from engine.graphics import animations, image, Sprite
from engine.input import Input, Key
from engine.state import Game, Scene
from engine.tile import TileMap


class MainScene(Scene):
    def __init__(self):
        super().__init__()
        self.anim = animations.AnimManager.new_anim("run")
        self.game_surf = pygame.Surface(Game.screen_size * 0.3)
        self.ui_surf = pygame.Surface(Game.screen_size / 3, flags=SRCALPHA)
        self.tm = TileMap("assets/test.tmx")
        self.camera = Camera((10, 10), pygame.Vector2(self.game_surf.get_size()) / 16, (16, 16))

    def update(self):
        if Input.key_down(Key.ESCAPE):
            Game.quit()
        cam_speed = 5*Game.dt
        if Input.key_down(Key.w):
            self.camera.center.y -= cam_speed
        if Input.key_down(Key.s):
            self.camera.center.y += cam_speed
        if Input.key_down(Key.a):
            self.camera.center.x -= cam_speed
        if Input.key_down(Key.d):
            self.camera.center.x += cam_speed
        self.anim.update()

    def render(self):
        self.game_surf.fill(0)
        self.tm.render(self.game_surf, self.camera)
        self.game_surf.blit(self.anim.image(), self.camera.project(self.camera.center))

        # Use for debugging to find 0, 0
        # pygame.draw.rect(self.game_surf, (255, 0, 0), (self.camera.project((0,0)), (16, 16)))

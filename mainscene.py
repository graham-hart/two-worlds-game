import pygame
from pygame.locals import *

from character import Character
from engine.graphics import Camera
from engine.input import Input, Key
from engine.state import Game, Scene
from engine.tile import TileMap


class MainScene(Scene):
    def __init__(self):
        super().__init__()
        self.player = Character((0, 0), "player")
        self.player.sprite.set_anim("run")
        self.game_surf = pygame.Surface(Game.screen_size / 3)
        self.ui_surf = pygame.Surface(Game.screen_size / 3, flags=SRCALPHA)
        self.tm = TileMap("assets/test.tmx")
        self.camera = Camera((10, 10), pygame.Vector2(self.game_surf.get_size()) / 16, (16, 16))

    def update(self):
        if Input.key_down(Key.ESCAPE):
            Game.quit()
        self.player.update(self.tm)
        self.camera.center.x += (int(self.player.pos.x) - self.camera.center.x) * 5 * Game.dt
        self.camera.center.y += (int(self.player.pos.y) - self.camera.center.y) * 5 * Game.dt

    def render(self):
        self.game_surf.fill(0)
        self.tm.render(self.game_surf, self.camera)
        self.player.render(self.game_surf, self.camera)

        # pygame.draw.circle(self.game_surf, (255, 0, 0), (self.game_surf.get_width()//2, self.game_surf.get_height()//2), 2)
        # pygame.draw.rect(self.game_surf, (0, 0, 255), (self.camera.project((self.player.rect.x, self.player.rect.y)), (self.player.rect.width*16, self.player.rect.height*16)))
        Game.display.blit(pygame.transform.scale(self.ui_surf, Game.screen_size), (0, 0))
        Game.display.blit(pygame.transform.scale(self.game_surf, Game.screen_size), (0, 0))

        pygame.display.flip()

import pygame
from pygame.locals import *

import engine.utils
from engine.graphics import animations, image
from engine.input import Input, Key
from engine.state import Game, Scene
from engine.ui import SpeechBox
from engine.tile import TileMap
IPSUM = [
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Integer eget aliquet nibh praesent tristique magna. Nullam non nisi est sit amet facilisis magna. Etiam non quam lacus suspendisse faucibus interdum. Lobortis scelerisque fermentum dui faucibus in.",
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Leo a diam sollicitudin tempor id. Ipsum consequat nisl vel pretium lectus quam. Consectetur libero id faucibus nisl tincidunt eget nullam. Quis commodo odio aenean sed.",
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Quis varius quam quisque id diam vel quam elementum. Ac turpis egestas integer eget aliquet nibh praesent. Enim diam vulputate ut pharetra sit. Non quam lacus suspendisse faucibus interdum posuere lorem ipsum.",
]


class MainScene(Scene):
    def __init__(self):
        super().__init__()
        self.anim = animations.AnimManager.new_anim("run")
        self.game_surf = pygame.Surface(Game.screen_size / 4)
        self.ui_surf = pygame.Surface(Game.screen_size / 3, flags=SRCALPHA)
        self.tm = TileMap("assets/test.tmx")

    def update(self):
        if Input.key_down(Key.ESCAPE):
            Game.quit()
        self.anim.update()

    def render(self):
        self.game_surf.fill(0)
        self.game_surf.blit(self.anim.image(), (0, 0))
        self.tm.render(self.game_surf)
        Game.display.blit(pygame.transform.scale(self.game_surf, Game.screen_size), (0, 0))
        Game.display.blit(pygame.transform.scale(self.ui_surf, Game.screen_size), (0, 0))
        pygame.display.flip()

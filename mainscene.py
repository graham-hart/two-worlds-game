import pygame

from engine.state import Game, Scene
from engine.input import Input, Key, MouseButton


class MainScene(Scene):
    def __init__(self):
        super().__init__()
        self.zombie_img = pygame.image.load()

    def update(self):
        if Input.key_down(Key.ESCAPE):
            Game.quit()

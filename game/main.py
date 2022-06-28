import pygame

from engine.graphics.animations import AnimManager
from engine.state import Game
from game.mainscene import MainScene


def run():
    Game.screen_size = pygame.Vector2((1200, 900))
    Game.init()
    AnimManager.load("assets/animations")
    Game.current_scene = MainScene()
    Game.fps = 60
    Game.tps = 60
    Game.start()

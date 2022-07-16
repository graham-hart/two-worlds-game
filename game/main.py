import pygame

from engine.graphics.animations import AnimManager
from engine.state import Game
from engine.tile import TileManager
from game.mainscene import MainScene
from tiles import ATile, LeftARampTile


def register_tiles():
    TileManager.register(ATile)
    TileManager.register(LeftARampTile)


def run():
    register_tiles()
    Game.screen_size = pygame.Vector2((1200, 900))
    Game.init()
    AnimManager.load("assets/animations")
    Game.current_scene = MainScene()
    Game.fps = 60
    Game.tps = 60
    Game.start()

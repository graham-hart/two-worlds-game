import pygame

from engine.graphics.animations import AnimManager
from engine.state import Game
from mainscene import MainScene


def main():
    Game.screen_size = pygame.Vector2((1200, 900))
    Game.init()
    AnimManager.load("assets/animations")
    Game.current_scene = MainScene()
    Game.start()


if __name__ == '__main__':
    main()

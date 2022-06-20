import pygame

from engine.graphics.animations import AnimManager
from engine.state import Game
from mainscene import MainScene


def main():
    AnimManager.load("assets/animations")
    Game.screen_size = pygame.Vector2((1000, 1000))
    Game.init()
    Game.current_scene = MainScene()
    Game.start()


if __name__ == '__main__':
    main()

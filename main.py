
import pygame
from engine.state import Game
from mainscene import MainScene


def main():
    Game.current_scene = MainScene()
    Game.screen_size = pygame.Vector2(500, 500)
    Game.start()


if __name__ == '__main__':
    main()

import sys

import pygame
from pygame.locals import *

from engine.input import Input


class Game:  # Not meant to be instantiated, gives access to global data and functionality
    current_scene = None
    fps = 0
    dt = 0
    clock = pygame.time.Clock()
    screen_size = pygame.Vector2(0)
    display = None
    events = []
    _quit = False

    @classmethod
    def title(cls, t=None):
        if t is None:
            return pygame.display.get_caption()
        pygame.display.set_caption(t)
        return t

    @classmethod
    def quit(cls):
        cls._quit = True

    @classmethod
    def set_scene(cls, scene_class, *args, **kwargs):
        cls.current_scene = scene_class(*args, **kwargs)

    @classmethod
    def start(cls):
        cls.display = pygame.display.set_mode(cls.screen_size)
        while not cls._quit:
            cls.dt = cls.clock.tick(cls.fps)
            Input.update()

            cls.events = pygame.event.get()
            for evt in cls.events:
                if evt.type == MOUSEBUTTONDOWN:
                    Input.handle_mousedown(evt.button)
                elif evt.type == MOUSEBUTTONUP:
                    Input.handle_mouseup(evt.button)
                elif evt.type == MOUSEMOTION:
                    Input.handle_mousemotion(evt.pos, evt.rel)
                elif evt.type == KEYDOWN:
                    Input.handle_keydown(evt.key)
                elif evt.type == KEYUP:
                    Input.handle_keyup(evt.key)
                elif evt.type == QUIT:
                    cls.quit()

            if cls.current_scene:
                cls.current_scene.update()
                cls.current_scene.render()
                if cls._quit:
                    cls.current_scene.quit()

            pygame.display.flip()
        pygame.quit()
        sys.exit()

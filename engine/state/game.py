import os
import sys

import pygame
from pygame.locals import *

from engine.input import Input
from engine.ui.font import Font


class Game:  # Not meant to be instantiated, gives access to global data and functionality
    current_scene = None
    fps = 60
    tps = 60
    clock = pygame.time.Clock()
    screen_size = pygame.Vector2(0)
    display = None
    events = []
    _quit = False
    _init = False
    font = None

    @classmethod
    def init(cls):
        cls._init = True
        cls.display = pygame.display.set_mode(cls.screen_size)
        cls.font = Font("assets/font.png", color=(1, 1, 1))

    @classmethod
    def resize_screen(cls, new_size):
        cls.screen_size = pygame.Vector2(new_size)
        if cls._init:
            cls.display = pygame.display.set_mode(new_size)

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
        last_update = pygame.time.get_ticks()
        mspt = 1000 // cls.tps
        if not cls._init:
            raise Exception("Game not initialized")
        while not cls._quit:
            cls.clock.tick(cls.fps)
            Input.update()
            if cls.current_scene is not None:
                current_time = pygame.time.get_ticks()
                delta = current_time - last_update
                if delta >= mspt:
                    last_update = pygame.time.get_ticks()
                    while delta >= mspt:
                        cls.current_scene.tick()
                        delta -= mspt
                        last_update = pygame.time.get_ticks()

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

            if cls.current_scene is not None:
                cls.current_scene.render()
                cls.current_scene.tick()
                cls.current_scene.update()
                if cls._quit:
                    cls.current_scene.quit()

        pygame.quit()
        sys.exit()

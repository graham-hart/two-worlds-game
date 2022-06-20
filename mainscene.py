import pygame

from engine import utils
from engine.graphics import animations
from engine.input import Input, Key
from engine.state import Game, Scene


class MainScene(Scene):
    def __init__(self):
        super().__init__()
        self.anim = animations.AnimManager.new_anim("run")
        self.anim_2 = animations.AnimManager.new_anim("run")
        self.anim_2.current_frame = 1
        self.surf = pygame.Surface(Game.screen_size / 2)

    def update(self):
        if Input.key_down(Key.ESCAPE):
            Game.quit()
        self.anim.update()
        self.anim_2.update()

    def render(self):
        self.surf.fill(0)
        self.surf.blit(self.anim.image(), (0, 0))
        self.surf.blit(pygame.transform.flip(self.anim_2.image(), True, False), (20, 20))
        Game.display.blit(pygame.transform.scale(self.surf, Game.screen_size), (0,0))
        pygame.display.flip()

import pygame

import engine.utils
from engine.graphics import animations, image
from engine.input import Input, Key
from engine.state import Game, Scene
from engine.ui import SpeechBox


class MainScene(Scene):
    def __init__(self):
        super().__init__()
        self.anim = animations.AnimManager.new_anim("run")
        self.anim_2 = animations.AnimManager.new_anim("run")
        self.anim_2.current_frame = 1
        self.game_surf = pygame.Surface(Game.screen_size / 4)
        self.ui_surf = pygame.Surface(Game.screen_size / 3)
        img = engine.utils.stretch_img_center_horiz(image.load("assets/ui/textbox.png"), 8, 397,
                                                    self.ui_surf.get_width())
        self.speechbox = SpeechBox(img, pygame.Vector2(self.ui_surf.get_size()),
                                   "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Integer eget aliquet nibh praesent tristique magna. Nullam non nisi est sit amet facilisis magna. Etiam non quam lacus suspendisse faucibus interdum. Lobortis scelerisque fermentum dui faucibus in.",
                                   Game.font, 1)

    def update(self):
        if Input.key_down(Key.ESCAPE):
            Game.quit()
        self.anim.update()
        self.anim_2.update()
        self.speechbox.update()

    def render(self):
        self.game_surf.fill(0)
        self.game_surf.blit(self.anim.image(), (0, 0))
        self.game_surf.blit(pygame.transform.flip(self.anim_2.image(), True, False), (20, 20))
        self.speechbox.render(self.ui_surf)
        Game.display.blit(pygame.transform.scale(self.game_surf, Game.screen_size), (0, 0))
        Game.display.blit(pygame.transform.scale(self.ui_surf, Game.screen_size), (0, 0))
        pygame.display.flip()

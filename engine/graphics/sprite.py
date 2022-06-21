from typing import Union

import pygame

from .animations import Animation


class Renderer:
    def __init__(self, visuals: Union[Animation, pygame.Surface], pos: pygame.Vector2):
        self.visuals = visuals
        self.pos = pos
        self.anchor = pygame.Vector2(0,0)

    @property
    def animated(self):
        return type(self.visuals) == Animation

    def render(self, surf: pygame.Surface, camera=None):
        render_pos = self.pos
        if camera is not None:  # TODO: add camera
            pass  # Project render_pos coordinate

        render_pos = render_pos - self.anchor
        if self.animated:
            surf.blit(self.visuals.image(), self.pos-self.anchor)
        else:
            surf.blit(self.visuals, self.pos-self.anchor)

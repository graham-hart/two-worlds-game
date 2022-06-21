from typing import Union

import pygame

from .animations import Animation


class Sprite:
    def __init__(self, visuals: Union[Animation, pygame.Surface], pos: pygame.Vector2, centered: bool = False):
        self.visuals = visuals
        self.pos = pos
        self.centered = centered

    @property
    def animated(self) -> bool:
        return type(self.visuals) == Animation

    def image(self) -> pygame.Surface:
        return self.visuals if not self.animated else self.visuals.image()

    def render(self, surf: pygame.Surface, camera=None):
        render_pos = self.pos
        if camera is not None:  # TODO: add camera
            pass  # Project render_pos coordinate
        img = self.image()
        anchor = pygame.Vector2(img.get_size()) / 2
        surf.blit(img, render_pos - anchor)

    def update(self):
        if self.animated:
            self.visuals.update()

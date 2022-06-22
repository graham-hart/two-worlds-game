import pygame

import pygame

import engine.utils
from .animations import AnimManager


class Sprite:
    def __init__(self, pos: pygame.Vector2, centered: bool = False, img=None):
        self.pos = pos
        self.centered = centered
        self.static_img = img or engine.utils.filled_surf(0, (1, 1))
        self.current_animation = None

    def set_anim(self, anim_id):
        self.current_animation = AnimManager.new_anim(anim_id)

    def image(self) -> pygame.Surface:
        return self.current_animation.image() if self.current_animation is not None else self.static_img

    def render(self, surf: pygame.Surface, camera=None):
        render_pos = self.pos
        if camera is not None:  # TODO: add camera
            pass  # Project render_pos coordinate
        img = self.image()
        anchor = pygame.Vector2(img.get_size()) / 2
        surf.blit(img, render_pos - anchor)

    def update(self):
        if self.current_animation is not None:
            self.current_animation.update()

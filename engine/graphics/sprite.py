import math
from typing import Optional

import pygame

import engine
import engine.utils
from .animations import AnimManager


class Sprite:
    def __init__(self, entity: "engine.Entity", centered: bool = False, img: Optional[pygame.Surface] = None):
        self.entity = entity
        self.centered = centered
        self.static_img = img or engine.utils.filled_surf(0, (1, 1))
        self.current_animation = None
        self.flip = [False, False]
        self.opacity = 255

    def set_anim(self, anim_id):
        self.current_animation = AnimManager.new_anim(anim_id) if anim_id is not None else None

    def image(self) -> pygame.Surface:
        img = self.current_animation.image() if self.current_animation is not None else self.static_img
        if any(self.flip):
            img = pygame.transform.flip(img, self.flip[0], self.flip[1])
        if self.opacity != 255:
            img.set_alpha(self.opacity)
        return img

    def render(self, surf: pygame.Surface, camera=None):
        render_pos = self.entity.rect.pos
        if camera is not None:  # TODO: add camera
            render_pos = camera.project(render_pos)
        img = self.image()
        surf.blit(img, (round(render_pos[0]), round(render_pos[1])))

    def update(self):
        if self.current_animation is not None:
            self.current_animation.update()

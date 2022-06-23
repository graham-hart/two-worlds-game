from engine.graphics import Sprite
from engine.math import Rect

from engine.graphics.animations import AnimManager

class Entity:
    def __init__(self, pos, size, t, static_img=None):
        self.rect = Rect((0,0), size)
        self.rect.center = pos
        self.type = t
        self.sprite = Sprite(self, img=static_img)
        if f"{self.type}_idle" in AnimManager.anim_data.keys():
            self.sprite.set_anim(f"{self.type}_idle")

    def render(self, surf, cam):
        self.sprite.render(surf, cam)

    @property
    def pos(self):
        return self.rect.center

    @pos.setter
    def pos(self, p):
        self.rect.center = p

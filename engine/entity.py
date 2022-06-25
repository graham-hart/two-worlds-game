from engine.graphics import Sprite
from engine.graphics.animations import AnimManager
from engine.math import Rect
from .rigidbody import RigidBody


class Entity:
    def __init__(self, pos, size, t, static_img=None):
        self.rect = Rect((0, 0), size)
        self.rect.center = pos
        self.type = t
        self.sprite = Sprite(self, img=static_img)
        if f"{self.type}_idle" in AnimManager.anim_data.keys():
            self.sprite.set_anim(f"{self.type}_idle")
        self.rigidbody = RigidBody(self)

    def render(self, surf, cam):
        self.sprite.render(surf, cam)

    def update(self, tilemap):
        self.sprite.update()
        self.rigidbody.update(tilemap)

    @property
    def pos(self):
        return self.rect.center

    @pos.setter
    def pos(self, p):
        self.rect.center = p

    def on_collision(self, collisions, collision_dirs):
        pass

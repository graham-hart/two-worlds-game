import pygame

from engine.math import Rect
import math

# Class to translate coordinates & project between pixel and world coordinates

class Camera:
    def __init__(self, center, size, unit_size: tuple[int, int]):
        self.center = pygame.Vector2(center)
        self.size = pygame.Vector2(size)
        self.unit_size = pygame.Vector2(unit_size)
        self.offset = self.size * 0.5

    @property
    def render_center(self):
        return pygame.Vector2(int(self.center.x*self.unit_size.x)/self.unit_size.x, int(self.center.y*self.unit_size.y)/self.unit_size.y)

    @property
    def viewport_rect(self):
        r = Rect((0, 0), (self.size.x, self.size.y))
        r.center = self.center
        return r

    def project_x(self, x):
        return (x - self.render_center.x + self.offset.x) * self.unit_size.x

    def project_y(self, y):
        return (y - self.render_center.y + self.offset.y) * self.unit_size.y

    def unproject_x(self, x):
        return (x / self.unit_size.x) + self.render_center.x - self.offset.x

    def unproject_y(self, y):
        return (y / self.unit_size.y) + self.render_center.y - self.offset.y

    def project(self, pos):
        x, y = self.project_x(pos[0]), self.project_y(pos[1])
        if type(pos) is list:
            return [x, y]
        return type(pos)((x, y))

    def unproject(self, pos):
        x, y = self.unproject_x(pos[0]), self.unproject_y(pos[1])
        if type(pos) is list:
            return [x, y]
        return type(pos)((x, y))

    def lerp_to(self, pos, amount):
        self.center = self.center.lerp(pos, amount)
        if self.center.distance_squared_to(pos) < 1/(self.unit_size[0]*self.unit_size[1]):
            self.center.update(pos)

from typing import Union

import pygame


class Rect:
    def __init__(self, pos, size):
        self.pos = pygame.Vector2(pos)
        self.size = pygame.Vector2(size)

    def copy(self):
        return Rect(self.pos, self.size)

    def move(self, amount: Union[tuple[float, float], pygame.Vector2]):
        return Rect((self.pos.x + amount[0], self.pos.y + amount[1]), self.size)

    def move_ip(self, amount: Union[tuple[float, float], pygame.Vector2]):
        self.pos.x += amount[0]
        self.pos.y += amount[1]

    def inflate(self, amount: Union[tuple[float, float], pygame.Vector2]):
        return Rect(self.pos, (self.size.x + amount[0], self.size.y + amount[1]))

    def inflate_ip(self, amount: Union[tuple[float, float], pygame.Vector2]):
        self.size.x += amount[0]
        self.size.y += amount[1]

    def update(self, pos, size):
        self.pos = pygame.Vector2(pos)
        self.size = pygame.Vector2(size)

    def colliderect(self, rect):
        return self.right >= rect.left and self.left <= rect.right and self.bottom >= rect.top and self.top <= rect.bottom

    def collidepoint(self, point):
        return self.left < point[0] < self.right and self.top < point[1] < self.bottom

    def collidelist(self, rectlist):
        for r in rectlist:
            if self.colliderect(r):
                return True

        return False

    def collidelistall(self, rectlist):
        for r in rectlist:
            if not self.colliderect(r):
                return False

        return True

    @property
    def width(self):
        return self.size.x

    @width.setter
    def width(self, w):
        self.size.x = w

    @property
    def height(self):
        return self.size.y

    @height.setter
    def height(self, h):
        self.size.y = h

    @property
    def x(self):
        return self.pos.x

    @x.setter
    def x(self, _x):
        self.pos.x = _x

    @property
    def y(self):
        return self.pos.y

    @y.setter
    def y(self, _y):
        self.pos.y = _y

    @property
    def top(self):
        return self.pos.y

    @top.setter
    def top(self, t):
        self.pos.y = t

    @property
    def bottom(self):
        return self.pos.y + self.size.y

    @bottom.setter
    def bottom(self, b):
        self.pos.y = b - self.size.y

    @property
    def left(self):
        return self.pos.x

    @left.setter
    def left(self, l):
        self.pos.x = l

    @property
    def right(self):
        return self.pos.x + self.size.x

    @right.setter
    def right(self, r):
        self.pos.x = r - self.size.x

    @property
    def topleft(self):
        return self.pos

    @topleft.setter
    def topleft(self, tl):
        self.pos.x = tl[0]
        self.pos.y = tl[1]

    @property
    def topright(self):
        return pygame.Vector2(self.pos.x + self.size.x, self.pos.y)

    @topright.setter
    def topright(self, tr):
        self.pos.x = tr[0] - self.size.x
        self.pos.y = tr[1]

    @property
    def bottomleft(self):
        return pygame.Vector2(self.pos.x, self.pos.y + self.size.y)

    @bottomleft.setter
    def bottomleft(self, bl):
        self.pos.x = bl[0]
        self.pos.y = bl[1] - self.size.y

    @property
    def bottomright(self):
        return self.pos + self.size

    @bottomright.setter
    def bottomright(self, br):
        self.pos.x = br[0] - self.size.x
        self.pos.y = br[1] - self.size.y

    @property
    def center(self):
        return self.pos + self.size * 0.5

    @center.setter
    def center(self, c):
        self.pos.x = c[0] - self.size.x * 0.5
        self.pos.y = c[1] - self.size.y * 0.5

    def __repr__(self):
        return f"Rect[{self.pos}, {self.size}]"

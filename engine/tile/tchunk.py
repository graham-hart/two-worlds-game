from engine.math import Rect


class Chunk:
    def __init__(self, pos, size, tiles):
        self.rect = Rect(pos, size)
        self.tiles = tiles

    def collision(self, rect):
        if not self.rect.colliderect(rect):
            return None
        return [d for d in self.tiles if d[0].colliderect(rect)]

    def get_tile(self, pos):
        return self.tiles[int(pos[0] - self.rect.pos.x), int(pos[1] - self.rect.pos.y)]

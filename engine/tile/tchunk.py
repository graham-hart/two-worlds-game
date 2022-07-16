from engine.math import Rect
from .tile import Tile


class Chunk:
    def __init__(self, pos, size, tiles):
        self.rect = Rect(pos, size)
        self.tiles: dict[int, dict[tuple[int, int], Tile]] = tiles

    def tile_collision(self, rect, collision_layers):
        tiles = {}
        for l in collision_layers:
            tiles.update(self.tiles[l])
        if not self.rect.colliderect(rect):
            return None
        return [d for d in tiles if d[0].colliderect(rect)]

    def chunk_collision(self, rect):
        return self.rect.colliderect(rect)

    def get_tile(self, pos, layer):
        return self.tiles[layer][int(pos[0] - self.rect.pos.x), int(pos[1] - self.rect.pos.y)]

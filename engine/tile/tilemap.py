import json

from engine.graphics import Camera
from .tchunk import Chunk
from .tilemanager import TileManager
from engine import utils

def parse_tiles(tiles: dict[int, dict[str, str]], chunk_size: int = 16):
    chunked = {}
    for l_id, layer in tiles.items():
        for p in layer.keys():
            pos = p.split(",")
            x, y = int(pos[0]), int(pos[1])
            cx, cy = x // chunk_size * chunk_size, y // chunk_size * chunk_size  # Floor each number by chunk size to get position of chunk
            data = layer[p].split("/")

            if (cx, cy) not in chunked:
                chunked[cx, cy] = Chunk((cx, cy), chunk_size, {})
            chunk = chunked[cx, cy]
            if l_id not in chunk.tiles:
                chunk.tiles[l_id] = {}
            chunk.tiles[l_id][x % chunk_size, y % chunk_size] = TileManager.instantiate(data[0], (x, y), data[1] if len(data) > 1 else None)
    return chunked


class TileMap:
    COLLISION_LAYERS = [0]

    def __init__(self, path):
        data = json.load(open(path))
        self.objects = data["objects"]
        self.entities = data["entities"]
        self.tiles = parse_tiles(data["tiles"], chunk_size=16)

    def collide(self, rect):
        collisions = []
        for c in self.tiles.values():
            collisions += c.tile_collision(rect, self.COLLISION_LAYERS) or []
        return collisions

    def get_tile(self, pos, layer):
        chunk = self.tiles[utils.floor_to_interval(pos[0], 16), utils.floor_to_interval(pos[1], 16)]
        return chunk.get_tile(pos, layer)

    def visible_chunks(self, camera):
        chunks = []
        for chunk in self.tiles.values():
            if chunk.rect.colliderect(camera.viewport_rect): chunks.append(chunk)
        return chunks

    def get_tiles(self):
        tiles = []
        for chunk in self.tiles.values():
            for layer in chunk.tiles.values():
                tiles += list(layer.values())
        return tiles

    def visible_tiles(self, camera):
        tiles = []
        for c in self.visible_chunks(camera):
            for layer in c.tiles.values():
                tiles += [t for t in layer.values() if t.rect.colliderect(camera.viewport_rect)]
        return tiles

import math
import os

from bs4 import BeautifulSoup

from engine.graphics import Camera
from engine.math import Rect
from .tchunk import Chunk
from .tileset import TileSet


class TileMap:  # ! Cannot use pygame.Rect for collisions, as it only uses ints
    COLLISION_LAYERS = [1]

    def __init__(self, path):
        containing_dir = os.path.split(path)[0]
        data = BeautifulSoup(open(path).read(), features="xml")
        _map = data.map
        self.tileset = TileSet(os.path.join(containing_dir, _map.tileset.get("source")))
        self.firstgid = int(_map.tileset.get("firstgid"))
        self.tiled_v = _map.get("tiledversion")
        self.size = (int(_map.get("width")), int(_map.get("height")))
        layers = _map.find_all("layer")
        self.layers = {}
        self.layer_ids = {}
        for l in layers:
            l_id = int(l.get("id"))
            self.layer_ids[l.get("name")] = l_id
            self.layers[l_id] = {}
            for chunk in l.find_all("chunk"):
                pos = int(chunk.get("x")), int(chunk.get("y"))
                size = int(chunk.get("width")), int(chunk.get("height"))
                self.chunk_size = size
                tiles = {}
                for y, row in enumerate(chunk.contents[0].split("\n")[1:-1]):
                    for x, tile in enumerate(row.split(",")[:-1]):
                        tile = int(tile) - self.firstgid
                        if tile == -1:
                            continue
                        t_size = self.tileset.get_tile_img(tile).get_size()
                        unit_size = self.tileset.unit_size
                        tiles[x, y] = Rect((pos[0] + x, pos[1] + y),
                                           (t_size[0] // unit_size[0], t_size[1] // unit_size[1])), tile
                self.layers[l_id][pos] = Chunk(pos, size, tiles)

    def collide(self, rect):
        collisions = []
        for l in TileMap.COLLISION_LAYERS:
            for c in self.layers[l]:
                collisions += c.tile_collision(rect) or []
        return collisions

    def get_tile(self, pos, layer):
        chunk = self.layers[layer][pos[0] - pos[0] % self.chunk_size[0], pos[1] - pos[1] % self.chunk_size[1]]
        return chunk.get_tile(pos)

    def render(self, surf, cam: Camera = None):
        for lid in sorted(self.layers.keys()):
            layer = self.layers[lid]
            for chunk in layer.values():
                if chunk.chunk_collision(cam.viewport_rect):
                    for t in chunk.tiles.values():
                        img = self.tileset.get_tile_img(t[1])
                        r_pos = cam.project((t[0].pos.x, t[0].pos.y))
                        surf.blit(img, (round(r_pos[0]), round(r_pos[1])))

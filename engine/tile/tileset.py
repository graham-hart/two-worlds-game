import pygame
from bs4 import BeautifulSoup
from engine.graphics import image
import os
class TileSet:
    def __init__(self, path):
        containing_dir = os.path.split(path)[0]
        data = BeautifulSoup(open(path).read(), features="xml")
        self.tiles = {}  # id:img
        self.tile_ids = {}  # name:id
        s = data.tileset
        self.tiled_v = s.get("tiledversion")
        self.name = s.get("name")
        self.unit_size = (int(s.get("tilewidth")), int(s.get("tileheight")))
        for tile in s.find_all("tile"):
            gid = int(tile.get("id"))
            img = tile.image
            fn = os.path.join(containing_dir, img.get("source"))
            self.tiles[gid] = image.load(fn)
            self.tile_ids[fn.split(".")[0]] = gid

    def get_tile_img(self, gid) -> pygame.Surface:
        return self.tiles[gid]

    def get_tile_gid(self, name):
        return self.tile_ids[name]

    def get_tile_name(self, gid):
        return {v:k for k,v in self.tile_ids.items()}[gid]

if __name__ == "__main__":
    TileSet("assets/tileset.tsx")

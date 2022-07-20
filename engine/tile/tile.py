from engine.math import Rect
from engine.graphics import image
import os

class Tile:
    tile_type = None
    img_path = None

    def __init__(self, pos: tuple[int, int], size: tuple[float, float], var:int, ramp: int):
        self.rect = Rect(pos, size)
        self.ramp = ramp  # 0 is no ramp, 1 is left, 2 is right
        self.var = var
    def render(self, surf, cam=None):
        pass

    @classmethod
    def load_imgs(cls):
        cls.images = image.load_dir(cls.img_path) if os.path.isdir(cls.img_path) else image.load(cls.img_path)

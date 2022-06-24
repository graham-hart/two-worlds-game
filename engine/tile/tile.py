from engine.math import Rect


class Tile:
    def __init__(self, pos: tuple[int, int], size: tuple[float, float], gid: int, ramp: int, layer: int):
        self.rect = Rect(pos, size)
        self.gid = gid
        self.ramp = ramp  # 0 is no ramp, 1 is left, 2 is right
        self.layer = layer

from engine.math import Rect


class Tile:
    tile_type = None

    def __init__(self, pos: tuple[int, int], size: tuple[float, float], var:int, ramp: int):
        self.rect = Rect(pos, size)
        self.ramp = ramp  # 0 is no ramp, 1 is left, 2 is right
        self.var = var
    def render(self, surf, cam=None):
        pass

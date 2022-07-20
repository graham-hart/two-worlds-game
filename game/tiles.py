from engine.tile import Tile


class ATile(Tile):
    tile_type = "a"
    img_path = "assets/images/grass"
    images = None

    def __init__(self, pos: tuple[int, int], var: int):
        super().__init__(pos, (1, 1), var, 2 if var == "ramp-r" else 1 if var == "ramp-l" else 0)

    def render(self, surf, cam=None):
        surf.blit(self.__class__.images[self.var] if type(self.images) is dict else self.__class__.images, (cam.project((self.rect.x, self.rect.y))))

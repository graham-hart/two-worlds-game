import pygame.draw

from engine.tile import Tile


class ATile(Tile):
    tile_type = "a"

    def __init__(self, pos: tuple[int, int], var: int):
        super().__init__(pos, (1, 1), var, 0)

    def render(self, surf, cam=None):
        pygame.draw.rect(surf, (255, 0, 0), (
            cam.project((self.rect.x, self.rect.y)),
            (self.rect.width * cam.unit_size.x, self.rect.height * cam.unit_size.y)))

class LeftARampTile(Tile):
    tile_type = "aramp-l"
    def __init__(self, pos: tuple[int, int], var: int):
        super().__init__(pos, (1,1), var, 1)

    def render(self, surf, cam=None):

        pygame.draw.polygon(surf, (255, 0, 0), [cam.project((self.rect.x, self.rect.y)), cam.project((self.rect.x, self.rect.y+1)), cam.project((self.rect.x+1, self.rect.y+1))])

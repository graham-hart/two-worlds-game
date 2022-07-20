from typing import Type
from .tile import Tile
class TileManager:
    types = {}
    @classmethod
    def register(cls, tile_class: Type[Tile], tile_type=None):
        tile_type = tile_type or tile_class.tile_type
        cls.types[tile_type] = tile_class
        tile_class.load_imgs()

    @classmethod
    def instantiate(cls, tile_type, pos, var, *args, **kwargs):
        """
        :param tile_type: type of tile
        :param pos: tile position
        :param var: tile variation
        :return: new tile of selected type
        """
        return cls.types[tile_type](pos, var, *args, **kwargs)

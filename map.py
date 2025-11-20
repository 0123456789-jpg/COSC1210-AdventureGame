import random
from enum import Enum


class TileType(Enum):
    GRASSLAND = 0
    MOUNTAIN = 1
    PORTAL = 2


class Tile:
    tile_type: TileType
    background: tuple[int, int]
    location: tuple[int, int]

    def __init__(
        self,
        tile_type: TileType,
        background: tuple[int, int],
        location: tuple[int, int],
    ) -> None:
        self.tile_type = tile_type
        self.background = background
        self.location = location


class Map:
    width: int
    height: int
    tiles: list[list[Tile]]

    def gen_tiles(self) -> None:
        pool: list[TileType] = (
            [TileType.GRASSLAND] * 20 + [TileType.MOUNTAIN] * 15 + [TileType.PORTAL]
        )
        self.tiles = [
            [
                Tile(
                    random.choice(pool),
                    (random.randrange(6), random.randrange(4)),
                    (x, y),
                )
                for y in range(self.height)
            ]
            for x in range(self.width)
        ]

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.gen_tiles()


class MapGrid:
    width: int
    height: int
    maps: list[list[Map]]

    def __init__(
        self, grid_width: int, grid_height: int, map_width: int, map_height: int
    ) -> None:
        self.width = grid_width
        self.height = grid_height
        self.maps = [
            [Map(map_width, map_height) for _ in range(grid_height)]
            for _ in range(grid_width)
        ]

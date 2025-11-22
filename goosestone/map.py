import random
from enum import Enum

import pygame as pg

import render


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
            [TileType.GRASSLAND] * 30 + [TileType.MOUNTAIN] * 5 + [TileType.PORTAL]
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
        pass

    def draw(self, surface: pg.Surface) -> None:
        tiles: list[Tile] = list((tile for row in self.tiles for tile in row))
        for tile in tiles:
            render.draw_tile(surface, tile.background, tile.location)
        for tile in tiles:
            if tile.tile_type == TileType.MOUNTAIN:
                render.draw_tile_2h(surface, (0, 4), tile.location)
            elif tile.tile_type == TileType.PORTAL:
                render.draw_tile(surface, (5, 21), tile.location)


class MapGrid:
    width: int
    height: int
    maps: list[list[Map]]
    focus: tuple[int, int] = (0, 0)

    def __init__(
        self, grid_width: int, grid_height: int, map_width: int, map_height: int
    ) -> None:
        self.width = grid_width
        self.height = grid_height
        self.maps = [
            [Map(map_width, map_height) for _ in range(grid_height)]
            for _ in range(grid_width)
        ]

    def jump(self, new_focus: tuple[int, int]) -> None:
        self.focus = new_focus

    def focus_map(self) -> Map:
        x, y = self.focus
        return self.maps[x][y]

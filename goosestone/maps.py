import random
from enum import Enum

import pygame as pg
import render


class TileType(Enum):
    GRASSLAND = 0
    MOUNTAIN = 1
    PORTAL = 2


class Tile:
    """
    # Tile

    The `variant` attribute is used to calculate following tile variants:
    - background
    - mountain
    """

    tile_type: TileType
    variant: tuple[int, int]
    location: tuple[int, int]

    def __init__(
        self,
        tile_type: TileType,
        background: tuple[int, int],
        location: tuple[int, int],
    ) -> None:
        self.tile_type = tile_type
        self.variant = background
        self.location = location


class Map:
    width: int
    height: int
    tiles: list[list[Tile]]
    portal_colors: dict[tuple[int, int], int]

    def gen_tiles(self) -> None:

        def choice(x: int, y: int) -> TileType:
            if (
                ret := random.sample(
                    [TileType.GRASSLAND, TileType.MOUNTAIN, TileType.PORTAL],
                    1,
                    counts=[45, 4, 1],
                )[0]
            ) == TileType.PORTAL:
                self.portal_colors[(x, y)] = -1
            return ret

        self.tiles = [
            [
                Tile(
                    choice(x, y),
                    (random.randrange(6), random.randrange(4)),
                    (x, y),
                )
                for y in range(self.height)
            ]
            for x in range(self.width)
        ]
        portals = list(self.portal_colors.keys())
        random.shuffle(portals)
        shuffled = {c: self.portal_colors[c] for c in portals}
        self.portal_colors = shuffled

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.portal_colors = {}
        self.gen_tiles()
        pass

    def draw(self, surface: pg.Surface) -> None:
        tiles: list[Tile] = list((tile for row in self.tiles for tile in row))
        for tile in tiles:
            render.draw_tile(surface, tile.variant, tile.location)
        for tile in tiles:
            if tile.tile_type == TileType.MOUNTAIN:
                a, b = tile.variant
                variant = (a * b) % 5  # Five mountain variants
                render.draw_tile_2h(surface, (variant, 4), tile.location)
            elif tile.tile_type == TileType.PORTAL:
                loc = tile.location
                color = self.portal_colors[loc]
                if color == -1:
                    color = random_portal_color()
                render.draw_tile(surface, (5, color), loc)


class MapGrid:
    width: int
    height: int
    maps: list[list[Map]]
    focus: tuple[int, int]
    pairs: dict[tuple[int, int], list[tuple[int, int]]]
    gems: dict[int, tuple[tuple[int, int], tuple[int, int]]]

    def __init__(
        self, grid_width: int, grid_height: int, map_width: int, map_height: int
    ) -> None:
        self.width = grid_width
        self.height = grid_height
        self.maps = [
            [Map(map_width, map_height) for _ in range(grid_height)]
            for _ in range(grid_width)
        ]
        for x, y in [(3, 6), (3, 9)]:
            self.maps[0][0].tiles[x][y].tile_type = TileType.GRASSLAND
            self.maps[0][0].portal_colors.pop((x, y), 0)
        self.focus = (0, 0)
        # Portal pairs gen START
        pairs: dict[tuple[int, int], list[tuple[int, int]]] = {
            (0, 0): []
        }  # (0,0) as root node
        grid_coords = [(x, y) for x in range(grid_height) for y in range(grid_width)]
        grid_coords.remove((0, 0))
        random.shuffle(grid_coords)
        remaining: dict[tuple[int, int], tuple[int, int]] = {
            (0, 0): (len(self.maps[0][0].portal_colors), 0)
        }

        def new(target: tuple[int, int]) -> None:
            x, y = target
            remaining[target] = (len(self.maps[x][y].portal_colors), 0)
            pairs[target] = []

        def check(target: tuple[int, int]) -> None:
            length, n = remaining.pop(target)
            remaining[target] = (length, n + 1)
            if remaining[target][0] == remaining[target][1]:
                del remaining[target]

        def pair(a: tuple[int, int], b: tuple[int, int]) -> None:
            color = random_portal_color()
            pairs[a].append(b)
            x, y = a
            idx = list(self.maps[x][y].portal_colors.keys())[remaining[a][1]]
            self.maps[x][y].portal_colors[idx] = color
            pairs[b].append(a)
            x, y = b
            idx = list(self.maps[x][y].portal_colors.keys())[remaining[b][1]]
            self.maps[x][y].portal_colors[idx] = color
            check(a)
            check(b)

        new((0, 0))
        for coord in grid_coords:  # Ensure full connectivity
            parent = random.sample(remaining.keys(), 1)[0]
            new(coord)
            pair(parent, coord)
        while len(remaining) > 1:  # Extra portals
            a, b = random.sample(
                remaining.keys(),
                2,
                counts=[length - n for length, n in remaining.values()],
            )
            pair(a, b)
        # Portal pairs gen END
        self.pairs = pairs
        # Gems gen START
        gems: dict[int, tuple[tuple[int, int], tuple[int, int]]] = {}
        for i in range(7):

            def gen_pos() -> tuple[tuple[int, int], tuple[int, int], bool]:
                grid_pos_x = random.randrange(grid_width)
                grid_pos_y = random.randrange(grid_height)
                map_pos_x = random.randrange(map_width)
                map_pos_y = random.randrange(map_height)
                if (
                    self.maps[grid_pos_x][grid_pos_y]
                    .tiles[map_pos_x][map_pos_y]
                    .tile_type
                    == TileType.GRASSLAND
                ) and (
                    ((grid_pos_x, grid_pos_y), (map_pos_x, map_pos_y))
                    not in gems.values()
                ):
                    return ((grid_pos_x, grid_pos_y), (map_pos_x, map_pos_y), True)
                else:
                    return ((0, 0), (0, 0), False)

            while not (result := gen_pos())[2]:
                pass
            grid_pos, map_pos, _ = result
            gems[i] = (grid_pos, map_pos)
        # Gems gen END
        self.gems = gems

    def jump(self, new_focus: tuple[int, int]) -> None:
        self.focus = new_focus

    def focus_map(self) -> Map:
        x, y = self.focus
        return self.maps[x][y]


def random_portal_color() -> int:
    return random.choice([9, 12, 15, 21])

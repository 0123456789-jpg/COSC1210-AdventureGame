import pygame as pg


def screen_to_map(screen: tuple[int, int]) -> tuple[int, int]:
    from render import TILE_HEIGHT, TILE_WIDTH

    return (screen[0] // TILE_WIDTH, screen[1] // TILE_HEIGHT)


def map_to_screen(map: tuple[int, int]) -> tuple[int, int]:
    from render import TILE_HEIGHT, TILE_WIDTH

    return (map[0] * TILE_WIDTH, map[1] * TILE_HEIGHT)


BOTTOMLESS_PIT: int = pg.event.custom_type()  # Actually an algorithm defect
GEM_COLLECTED: int = pg.event.custom_type()

from render import TILE_HEIGHT, TILE_WIDTH


def screen_to_map(screen: tuple[int, int]) -> tuple[int, int]:
    return (screen[0] // TILE_WIDTH, screen[1] // TILE_HEIGHT)


def map_to_screen(map: tuple[int, int]) -> tuple[int, int]:
    return (map[0] * TILE_WIDTH, map[1] * TILE_HEIGHT)

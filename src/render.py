"""
render.py
=========

This module provides high-level functions needed for drawing game textures. The
size of a regular texture is 32 by 16, while a double-height texture's size is
32 by 32.
"""

import os
import random

import pygame as pg

import util

TILE_WIDTH: int = 32
TILE_HEIGHT: int = 16
TYPE_WIDTH: int = 9
TYPE_HEIGHT: int = 15


def init() -> None:
    """
    Load and initialize tile and type sets into the memory.

    Parameters:
        None: Nothing to pass in.

    Returns:
        None: Nothing to return.
    """

    global TILE, TEXT
    TILE = pg.image.load(os.path.join("src", "images", "tileset.png")).convert_alpha()
    TEXT = pg.image.load(os.path.join("src", "images", "type.png")).convert_alpha()


def draw_tile(surface: pg.Surface, src: tuple[int, int], dest: tuple[int, int]) -> None:
    """
    Draws a regular texture at specified position in the tile set to a specified `Surface`.

    Parameters:
        surface (pygame.Surface): The target surface.
        src (tuple[int, int]): The texture's position in the tile set in (x, y).
        dest (tuple[int, int]): The target position in (x, y).

    Returns:
        None: Nothing to return.
    """

    draw_tile_custom(surface, src, util.map_to_screen(dest))


def draw_tile_2h(
    surface: pg.Surface, src: tuple[int, int], dest: tuple[int, int]
) -> None:
    """
    Draws a double-height texture at specified location in the tile set to a specified `Surface`.

    Parameters:
        surface (pg.Surface): The target surface.
        src (tuple[int, int]): The texture's position in the tile set in (x, y).
        dest (tuple[int, int]): The target position in (x, y).

    Returns:
        None: Nothing to return.
    """

    draw_tile_2h_custom(surface, src, util.map_to_screen((dest[0], dest[1] - 1)))


def draw_tile_custom(
    surface: pg.Surface, src: tuple[int, int], dest: tuple[int, int]
) -> None:
    origin: tuple[int, int] = util.map_to_screen(src)
    surface.blit(
        TILE,
        dest,
        area=(origin[0], origin[1], TILE_WIDTH, TILE_HEIGHT),
    )


def draw_tile_2h_custom(
    surface: pg.Surface, src: tuple[int, int], dest: tuple[int, int]
) -> None:
    origin: tuple[int, int] = util.map_to_screen(src)
    surface.blit(
        TILE,
        dest,
        area=(origin[0], origin[1], TILE_WIDTH, 2 * TILE_HEIGHT),
    )


def generate_background(
    width: int, height: int
) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    """
    Generates a random background pattern for a given size of the map.

    Parameters:
        width (int): Width of the map.
        height (int): Height of the map.

    Returns:
        list[tuple[tuple[int, int], tuple[int, int]]]: A list of source coordinates
        (position in the tile set) and destination coordinates (position in the target
        `Surface`) that can be used directly as `draw_tile()`'s parameters. Both coordinates
        are represented in (x, y).
    """
    return [
        ((random.randrange(6), random.randrange(4)), (x, y))
        for y in range(height)
        for x in range(width)
    ]

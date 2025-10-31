from random import randrange
from typing import Optional

import pygame as pg

import render
import sprite as sprite
import sprite.animation as ani
from config import FRAMERATE, MAP_HEIGHT, MAP_WIDTH


def main() -> None:
    pg.init()
    display = pg.display.set_mode(
        (MAP_WIDTH * render.TILE_WIDTH, MAP_HEIGHT * render.TILE_HEIGHT),
    )
    pg.display.set_caption("COSC 1210")
    render.init()
    timer = pg.time.Clock()
    map: list[tuple[tuple[int, int], tuple[int, int]]] = render.generate_background(
        MAP_WIDTH, MAP_HEIGHT
    )
    spawner: sprite.Spawner = sprite.Spawner()
    running: bool = True
    spawner.add_sprite("main", sprite.TextureSprite(display, (1, 19), (3, 6)))
    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
            elif e.type == pg.KEYDOWN:
                if e.dict["key"] == pg.K_SPACE:
                    map = render.generate_background(MAP_WIDTH, MAP_HEIGHT)
                elif e.dict["key"] == pg.K_m:
                    target: Optional[sprite.Sprite] = spawner.get_sprite("main")
                    if target != None:
                        spawner.add_animation(
                            "move",
                            ani.SpriteMoveTask(
                                target,
                                30,
                                (randrange(MAP_HEIGHT), randrange(MAP_WIDTH)),
                            ),
                        )
        for item in map:
            render.draw_tile(display, item[0], item[1])
        render.draw_tile_2h(display, (9, 4), (3, 6))
        spawner.tick()
        pg.display.flip()
        display.fill((0, 0, 0))
        timer.tick(FRAMERATE)


main()

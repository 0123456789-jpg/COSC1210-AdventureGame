from random import randrange
from typing import Optional

import pygame as pg

import render
import sprite
import sprite.animation as ani
import util
from config import FRAMERATE, MAP_HEIGHT, MAP_WIDTH


def main() -> None:
    pg.init()
    display = pg.display.set_mode(
        util.map_to_screen((MAP_WIDTH, MAP_HEIGHT)),
    )
    pg.display.set_caption("COSC 1210")
    render.init()
    timer = pg.time.Clock()
    map: list[tuple[tuple[int, int], tuple[int, int]]] = render.generate_background(
        MAP_WIDTH, MAP_HEIGHT
    )
    spawner: sprite.Spawner = sprite.Spawner()
    running: bool = True
    spawner.add_sprite("main", sprite.TextureSprite(display, (9, 4), (3, 6), True))
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
                            "random",
                            ani.SpriteMoveTask(
                                target,
                                30,
                                (randrange(MAP_HEIGHT), randrange(MAP_WIDTH)),
                            ),
                        )
                elif e.dict["key"] == pg.K_n:
                    target: Optional[sprite.Sprite] = spawner.get_sprite("main")
                    if target != None and isinstance(target, sprite.TextureSprite):
                        spawner.add_animation(
                            "texture",
                            ani.TextureSeqTask(
                                target, 300, [(2, x * 3) for x in range(4, 10)], (9, 4)
                            ),
                        )
            elif e.type == pg.MOUSEBUTTONUP:
                map_pos: tuple[int, int] = util.screen_to_map(e.dict["pos"])
                main_sprite: Optional[sprite.Sprite] = spawner.get_sprite("main")
                if main_sprite != None and map_pos != main_sprite.map_pos:
                    spawner.add_animation(
                        "mouse", ani.SpriteMoveTask(main_sprite, 120, (map_pos))
                    )
        for item in map:
            render.draw_tile(display, item[0], item[1])

        # Button prototype
        import time

        from render import TILE_HEIGHT, TILE_WIDTH

        btn_rect: pg.Rect = pg.Rect(
            util.map_to_screen((3, 9 - 1)), (TILE_WIDTH, TILE_HEIGHT * 2)
        )
        if btn_rect.collidepoint(pg.mouse.get_pos()):
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
            render.draw_tile_2h(display, (2, 12), (3, 9))
            text: pg.Surface = pg.font.Font(None, 24).render(
                "timestamp: " + str(time.time()), False, pg.Color(255, 255, 0)
            )
            display.blit(text, (8, 8))
        else:
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
            render.draw_tile_2h(display, (2, 15), (3, 9))

        spawner.tick()
        pg.display.flip()
        display.fill((0, 0, 0))
        timer.tick(FRAMERATE)


main()

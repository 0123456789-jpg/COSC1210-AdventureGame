from random import randrange

import pygame as pg

import map
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
    world: map.MapGrid = map.MapGrid(3, 3, MAP_WIDTH, MAP_HEIGHT)
    spawner: sprite.Spawner = sprite.Spawner()
    running: bool = True
    spawner.add_sprite("main", sprite.TextureSprite(display, (9, 4), (3, 6), True))
    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
            elif e.type == pg.KEYDOWN:
                if e.dict["key"] == pg.K_SPACE:
                    world.focus_map().gen_tiles()
                elif e.dict["key"] == pg.K_m:
                    if (target := spawner.get_sprite("main")) != None:
                        spawner.add_animation(
                            "random",
                            ani.SpriteMoveTask(
                                target,
                                30,
                                (randrange(MAP_WIDTH), randrange(MAP_HEIGHT)),
                            ),
                        )
                elif e.dict["key"] == pg.K_n:
                    if (target := spawner.get_sprite("main")) != None and isinstance(
                        target, sprite.TextureSprite
                    ):
                        spawner.add_animation(
                            "texture",
                            ani.TextureSeqTask(
                                target, 300, [(2, x * 3) for x in range(4, 10)], (9, 4)
                            ),
                        )
            elif e.type == pg.MOUSEBUTTONUP:
                map_pos: tuple[int, int] = util.screen_to_map(e.dict["pos"])
                if (
                    main_sprite := spawner.get_sprite("main")
                ) != None and map_pos != main_sprite.map_pos:
                    spawner.add_animation(
                        "mouse",
                        ani.SpriteMoveTask(main_sprite, FRAMERATE // 2, (map_pos)),
                    )
        world.focus_map().draw(display)

        # Button prototype start
        if world.focus == (0, 0):
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
        # Button prototype end

        text: pg.Surface = pg.font.Font(None, 24).render(
            f"Dimension: {world.focus}", False, pg.Color(255, 255, 0)
        )
        display.blit(text, (8, 32))

        spawner.tick()
        pg.display.flip()
        display.fill((0, 0, 0))
        timer.tick(FRAMERATE)


main()

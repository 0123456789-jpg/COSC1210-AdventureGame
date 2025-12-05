from random import randrange
from typing import Literal

import maps
import pygame as pg
import render
import sprite
import sprite.animation as ani
import util
from config import FRAMERATE, MAP_HEIGHT, MAP_WIDTH, WORLD_HEIGHT, WORLD_WIDTH


def main() -> None:
    pg.init()
    display = pg.display.set_mode(
        util.map_to_screen((MAP_WIDTH, MAP_HEIGHT + 2)),
    )
    pg.display.set_caption("GooseStone for COSC 1210")
    render.init()
    timer = pg.time.Clock()
    world: maps.MapGrid = maps.MapGrid(WORLD_WIDTH, WORLD_HEIGHT, MAP_WIDTH, MAP_HEIGHT)
    spawner: sprite.Spawner = sprite.Spawner()
    running: bool = True
    exit_reason: Literal[0, 1, 2] = 0
    spawner.add_sprite("main", sprite.TextureSprite(display, (9, 4), (3, 6), True))
    spawner.add_sprite(
        "timer", sprite.TimerSprite(display, (2, 15), (3, 9), (2, 12), world)
    )
    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
            elif e.type == pg.KEYDOWN:
                if e.dict["key"] == pg.K_m:
                    if (target := spawner.get_sprite("main")) != None:
                        spawner.add_animation(
                            "random",
                            ani.SpriteMoveTask(
                                target,
                                30,
                                (randrange(MAP_WIDTH), randrange(MAP_HEIGHT)),
                            ),
                        )
                elif e.dict["key"] == pg.K_ESCAPE:
                    exit_reason = 0
                    running = False
            elif e.type == pg.MOUSEBUTTONUP:
                map_pos: tuple[int, int] = util.screen_to_map(e.dict["pos"])
                if (
                    main_sprite := spawner.get_sprite("main")
                ) != None and map_pos != main_sprite.map_pos:
                    spawner.add_animation(
                        "mouse",
                        ani.MainMoveTask(main_sprite, FRAMERATE // 2, map_pos, world),
                    )
            elif e.type == util.BOTTOMLESS_PIT:
                exit_reason = 1
                running = False
        world.focus_map().draw(display)
        text: pg.Surface = pg.font.Font(None, 24).render(
            f"Dimension: {world.focus}", False, pg.Color(255, 255, 0)
        )
        display.blit(text, (8, 32))

        spawner.tick()
        pg.display.flip()
        display.fill((0, 0, 0))
        timer.tick(FRAMERATE)

    placeholder = "0h0m0s"
    prompts: list[str] = [
        "Game will quit in 3 seconds...",
        "You fall into a bottomless pit and lose :(",
        f"You found all gems in {placeholder} and win!",
    ]
    text: pg.Surface = pg.font.Font(None, 48).render(
        prompts[exit_reason], False, pg.Color(255, 255, 0)
    )
    display.blit(
        text,
        (
            (MAP_WIDTH * render.TILE_WIDTH - text.get_width()) // 2,
            (MAP_HEIGHT * render.TILE_HEIGHT - text.get_height()) // 2,
        ),
    )
    pg.display.flip()
    pg.time.delay(3000)


main()

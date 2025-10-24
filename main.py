import pygame as pg
import render


def main() -> None:
    window_width: int = 20
    window_height: int = 20

    pg.init()
    display = pg.display.set_mode(
        (window_width * render.TILE_WIDTH, window_height * render.TILE_HEIGHT),
    )
    pg.display.set_caption("COSC 1210")
    render.init()
    timer = pg.time.Clock()
    map: list[tuple[tuple[int, int], tuple[int, int]]] = render.generate_background(
        window_width, window_height
    )
    running: bool = True
    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
            elif e.type == pg.KEYDOWN and e.dict["key"] == pg.K_SPACE:
                map = render.generate_background(window_width, window_height)
        for item in map:
            render.draw_tile(display, item[0], item[1])
        render.draw_tile_2h(display, (9, 4), (3, 6))
        pg.draw.line(display, (255, 0, 0), (0, 0), (100, 0), 10)
        pg.display.flip()
        timer.tick(10)


main()

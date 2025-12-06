from abc import ABC, abstractmethod
from typing import Callable, Optional

import config
import maps
import pygame as pg
import render
import util


class Sprite(ABC):
    map_pos: tuple[int, int]
    screen_pos: tuple[int, int]
    animations: list[str]

    @abstractmethod
    def draw(self) -> None:
        """Draw the sprite to the screen."""
        pass

    def align_map_pos(self) -> None:
        """
        Align `map_pos` with the current `screen_pos`.
        """
        self.map_pos = util.screen_to_map(self.screen_pos)

    def align_screen_pos(self) -> None:
        """
        Align `screen_pos` with the current `map_pos`.
        """
        self.screen_pos = util.map_to_screen(self.map_pos)


class TextureSprite(Sprite):
    surface: pg.Surface
    texture: tuple[int, int]
    double_height: bool

    def __init__(
        self,
        surface: pg.Surface,
        texture: tuple[int, int],
        position: tuple[int, int],
        double_height: bool,
    ) -> None:
        self.map_pos = position
        self.screen_pos = util.map_to_screen(position)
        self.animations = []
        self.surface = surface
        self.texture = texture
        self.double_height = double_height

    def draw(self) -> None:
        if self.double_height:
            from render import TILE_HEIGHT

            render.draw_tile_2h_custom(
                self.surface,
                self.texture,
                (self.screen_pos[0], self.screen_pos[1] - TILE_HEIGHT),
            )
        else:
            render.draw_tile_custom(self.surface, self.texture, self.screen_pos)


class TimerSprite(TextureSprite):
    hover: tuple[int, int]  # Texture when mouse hovering
    normal: tuple[int, int]
    world: maps.MapGrid
    time: int  # Played time in frames

    def __init__(
        self,
        surface: pg.Surface,
        texture: tuple[int, int],
        position: tuple[int, int],
        hover: tuple[int, int],
        world: maps.MapGrid,
    ) -> None:
        super().__init__(surface, texture, position, True)
        self.hover = hover
        self.normal = texture
        self.world = world
        self.time = 0

    def draw(self) -> None:
        self.time += 1  # Tick time here
        if self.world.focus == (0, 0):
            btn_rect: pg.Rect = pg.Rect(
                util.map_to_screen((self.map_pos[0], self.map_pos[1] - 1)),
                (render.TILE_WIDTH, render.TILE_HEIGHT * 2),
            )
            if btn_rect.collidepoint(pg.mouse.get_pos()):
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
                self.texture = self.hover
                super().draw()
                hour, minute, second = self.get_time()
                text: pg.Surface = pg.font.Font(None, 24).render(
                    "Time played: " + f"{hour}h{minute}m{second}s",
                    config.TEXT_ANTIALIASING,
                    pg.Color(255, 255, 0),
                )
                self.surface.blit(text, (8, 8))
            else:
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
                self.texture = self.normal
                super().draw()

    def get_time(self) -> tuple[int, int, int]:
        second = self.time // config.FRAMERATE
        minute = second // 60
        second = second % 60
        hour = minute // 60
        minute = minute % 60
        return (hour, minute, second)


class CustomSprite(Sprite):
    user_data: dict[str, object]
    draw_func: Callable[[tuple[int, int], dict[str, object]], None]

    def __init__(
        self,
        position: tuple[int, int],
        user_data: dict[str, object],
        draw_func: Callable[[tuple[int, int], dict[str, object]], None],
    ) -> None:
        self.map_pos = position
        self.animations = []
        self.user_data = user_data
        self.draw_func = draw_func

    def draw(self) -> None:
        self.draw_func(self.map_pos, self.user_data)


class Spawner:
    import sprite.animation as ani

    sprite_pool: dict[str, Sprite]
    animation_exec: ani.Executor

    def __init__(self) -> None:
        import sprite.animation as ani

        self.sprite_pool = {}
        self.animation_exec = ani.Executor()

    def add_sprite(self, name: str, sprite: Sprite) -> None:
        self.sprite_pool[name] = sprite

    def remove_sprite(self, name: str) -> tuple[Sprite, list[ani.Task]]:
        import sprite.animation as ani

        sprite: Sprite = self.sprite_pool.pop(name)
        tasks: list[ani.Task] = [
            result
            for task in sprite.animations.copy()
            if (result := self.animation_exec.remove(task)) != None
        ]
        return (sprite, tasks)

    def get_sprite(self, name: str) -> Optional[Sprite]:
        return self.sprite_pool.get(name)

    def add_animation(self, name: str, task: ani.Task) -> Optional[ani.Task]:
        if task.target in self.sprite_pool.values():
            self.animation_exec.add(name, task)
            return None
        else:
            return task

    def remove_animation(self, name: str) -> Optional[ani.Task]:
        return self.animation_exec.remove(name)

    def tick(self) -> None:
        self.animation_exec.tick()
        for sprite in self.sprite_pool.values():
            sprite.draw()

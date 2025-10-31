from abc import ABC, abstractmethod
from typing import Callable, Optional

import pygame as pg

import render
from render import TILE_HEIGHT, TILE_WIDTH


class Sprite(ABC):
    map_pos: tuple[int, int]
    screen_pos: tuple[int, int]
    animations: list[str] = []

    @abstractmethod
    def draw(self) -> None:
        """Draw the sprite to the screen."""
        pass

    def align_map_pos(self) -> None:
        """
        Align `map_pos` with the current `screen_pos`.
        """
        self.map_pos = (
            self.screen_pos[0] // TILE_WIDTH,
            self.screen_pos[1] // TILE_HEIGHT,
        )

    def align_screen_pos(self) -> None:
        """
        Align `screen_pos` with the current `map_pos`.
        """
        self.screen_pos = (self.map_pos[0] * TILE_WIDTH, self.map_pos[1] * TILE_WIDTH)


class TextureSprite(Sprite):
    surface: pg.Surface
    texture: tuple[int, int]

    def __init__(
        self, surface: pg.Surface, texture: tuple[int, int], position: tuple[int, int]
    ) -> None:
        self.map_pos = position
        self.screen_pos = (position[0] * TILE_WIDTH, position[1] * TILE_HEIGHT)
        self.surface = surface
        self.texture = texture

    def draw(self) -> None:
        render.draw_tile_custom(self.surface, self.texture, self.screen_pos)


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
        self.user_data = user_data
        self.draw_func = draw_func

    def draw(self) -> None:
        self.draw_func(self.map_pos, self.user_data)


class Spawner:
    import sprite.animation as ani

    sprite_pool: dict[str, Sprite] = {}
    animation_exec: ani.Executor = ani.Executor()

    def add_sprite(self, name: str, sprite: Sprite) -> None:
        self.sprite_pool[name] = sprite

    def remove_sprite(self, name: str) -> tuple[Sprite, list[ani.Task]]:
        import sprite.animation as ani

        sprite: Sprite = self.sprite_pool.pop(name)
        tasks: list[ani.Task] = [
            task
            for task in [
                self.animation_exec.remove(task) for task in sprite.animations.copy()
            ]
            if task != None
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

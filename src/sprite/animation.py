from abc import ABC, abstractmethod
from collections.abc import Iterable, Iterator
from typing import Optional, cast

import util
from sprite import Sprite


class Task(Iterator[None], ABC):
    duration: int = 0
    progress: int = 0
    target: Sprite

    def __init__(self, target: Sprite, duration: int) -> None:
        super().__init__()
        self.target = target
        self.duration = duration

    @abstractmethod
    def __iter__(self) -> Iterator[None]:
        pass

    def __next__(self) -> None:
        if self.progress >= self.duration:
            raise StopIteration
        else:
            self.progress += 1

    @abstractmethod
    def reset(self) -> None:
        pass

    def active(self) -> bool:
        return self.progress < self.duration


class SpriteMoveTask(Task):
    start: tuple[int, int]
    stop: tuple[int, int]

    def __init__(
        self,
        target: Sprite,
        duration: int,
        stop: tuple[int, int],
        start: Optional[tuple[int, int]] = None,
    ) -> None:
        super().__init__(target, duration)
        if start != None:
            self.start = util.map_to_screen(start)
        else:
            self.start = util.map_to_screen(target.map_pos)
        self.stop = util.map_to_screen(stop)

    def __iter__(self) -> Iterator[None]:
        return self

    def reset(self) -> None:
        self.progress = 0
        self.target.screen_pos = self.start
        self.target.align_map_pos()

    def __next__(self) -> None:
        delta_x: int = self.stop[0] - self.start[0]
        delta_y: int = self.stop[1] - self.start[1]
        if self.active():
            move_x: int = delta_x * (self.progress + 1) // self.duration
            move_y: int = delta_y * (self.progress + 1) // self.duration
            self.target.screen_pos = (self.start[0] + move_x, self.start[1] + move_y)
            self.target.align_map_pos()
            self.progress += 1
            return None
        else:
            raise StopIteration


class TextureSeqTask(Task):
    from sprite import TextureSprite

    sequence: Iterable[tuple[int, int]]
    start: tuple[int, int]
    end: tuple[int, int]
    iterator: Iterator[tuple[int, int]]

    def get_target(self) -> TextureSprite:
        from sprite import TextureSprite

        return cast(TextureSprite, self.target)

    def __init__(
        self,
        target: TextureSprite,
        duration: int,
        sequence: Iterable[tuple[int, int]],
        end: tuple[int, int],
    ) -> None:
        super().__init__(target, duration)
        self.sequence = sequence
        self.end = end
        self.setup_iter()
        self.start = target.texture

    def setup_iter(self) -> None:
        self.iterator = iter(self.sequence)

    def __iter__(self) -> Iterator[None]:
        return self

    def __next__(self) -> None:
        if self.active():
            try:
                texture: tuple[int, int] = next(self.iterator)
            except StopIteration:
                self.setup_iter()
                texture: tuple[int, int] = next(self.iterator)
            self.get_target().texture = texture
            self.progress += 1
            return None
        else:
            self.get_target().texture = self.end
            raise StopIteration

    def reset(self) -> None:
        self.progress = 0
        self.get_target().texture = self.start


class Executor:
    pool: dict[str, Task] = {}

    def add(self, name: str, task: Task) -> None:
        self.pool[name] = task
        task.target.animations.append(name)

    def remove(self, name: str) -> Optional[Task]:
        try:
            task: Task = self.pool.pop(name)
        except KeyError:
            return None
        task.target.animations.remove(name)
        return task

    def tick(self) -> None:
        drained: list[str] = []
        for name, task in self.pool.items():
            try:
                next(task)
            except StopIteration:
                drained.append(name)
        for name in drained:
            self.remove(name)

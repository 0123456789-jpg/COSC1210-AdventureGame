from abc import ABC, abstractmethod
from collections.abc import Iterator
from typing import Optional

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
        if self.progress < self.duration:
            move_x: int = delta_x * (self.progress + 1) // self.duration
            move_y: int = delta_y * (self.progress + 1) // self.duration
            self.target.screen_pos = (self.start[0] + move_x, self.start[1] + move_y)
            self.target.align_map_pos()
            self.progress += 1
            return None
        else:
            raise StopIteration


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

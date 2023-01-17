import time
from dataclasses import InitVar, dataclass, field
from datetime import timedelta

from client.delayed_auto_repeat import DelayedAutoRepeat
from common.enum import Action


@dataclass
class Timer:
    das: InitVar[timedelta]
    arr: InitVar[timedelta]

    latest: timedelta = field(init=False)
    autorepeat: DelayedAutoRepeat = field(init=False)

    def __post_init__(self, das: timedelta, arr: timedelta) -> None:
        self.latest = self._now()
        self.autorepeat = DelayedAutoRepeat(das, arr)

    def start_autorepeat(self, action: Action) -> bool:
        return self.autorepeat.start(self.latest, action)

    def stop_autorepeat(self, action: Action) -> None:
        self.autorepeat.stop(action)

    def poll(self) -> Action | None:
        return self.autorepeat.trigger(self.latest)

    def update(self) -> None:
        self.latest = self._now()

    @staticmethod
    def _now() -> timedelta:
        return timedelta(microseconds=time.perf_counter_ns() // 1000)

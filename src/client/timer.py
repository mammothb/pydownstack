"""Timer class to handle DAS."""

import time
from dataclasses import InitVar, dataclass, field
from datetime import timedelta
from typing import TYPE_CHECKING

from client.delayed_auto_repeat import DelayedAutoRepeat

if TYPE_CHECKING:
    from common.enum import Action


@dataclass
class Timer:
    """Timer class to handle DAS."""

    das: InitVar[timedelta]
    arr: InitVar[timedelta]

    latest: timedelta = field(init=False)
    _autorepeat: DelayedAutoRepeat = field(init=False)

    def __post_init__(self, das: timedelta, arr: timedelta) -> None:
        self.latest = self._now()
        self._autorepeat = DelayedAutoRepeat(das, arr)

    def start_autorepeat(self, action: "Action") -> bool:
        """Starts DAS timer."""
        return self._autorepeat.start(self.latest, action)

    def stop_autorepeat(self, action: "Action") -> None:
        """Stops DAS timer."""
        self._autorepeat.stop(action)

    def poll(self) -> "Action | None":
        """Triggers any loaded actions."""
        return self._autorepeat.trigger(self.latest)

    def update(self) -> None:
        """Updates internal clock."""
        self.latest = self._now()

    @staticmethod
    def _now() -> timedelta:
        return timedelta(microseconds=time.perf_counter_ns() // 1000)

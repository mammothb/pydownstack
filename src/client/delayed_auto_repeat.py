from dataclasses import dataclass, field
from datetime import timedelta

from common.enum import Action


@dataclass
class DelayedAutoRepeat:
    delay: timedelta
    period: timedelta
    load: Action | None = field(default=None, init=False)
    trigger_time: timedelta | None = field(default=None, init=False)

    def is_loaded(self, action: Action) -> bool:
        """Indicates if an action has been loaded."""
        return self.load == action

    def start(self, now: timedelta, action: Action) -> bool:
        if self.is_loaded(action):
            return False
        self.load = action
        self.trigger_time = now + self.delay
        return True

    def stop(self, action: Action) -> None:
        if self.is_loaded(action):
            self.load = None
            self.trigger_time = None

    def trigger(self, now: timedelta) -> Action | None:
        if self.load is None or (
            self.trigger_time is not None and self.trigger_time > now
        ):
            return None
        assert self.trigger_time is not None
        self.trigger_time += self.period
        return self.load

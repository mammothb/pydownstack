"""Class which repeats loaded action after a delay."""

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import timedelta

    from common.enum import Action


@dataclass
class DelayedAutoRepeat:
    """Class which repeats loaded action after a delay."""

    delay: "timedelta"
    period: "timedelta"
    load: "Action | None" = field(default=None, init=False)
    trigger_time: "timedelta | None" = field(default=None, init=False)

    def is_loaded(self, action: "Action") -> bool:
        """Indicates if an action has been loaded."""
        return self.load == action

    def start(self, now: "timedelta", action: "Action") -> bool:
        """Loads a different action to be repeated."""
        if self.is_loaded(action):
            return False
        self.load = action
        self.trigger_time = now + self.delay
        return True

    def stop(self, action: "Action") -> None:
        """Removes currently loaded action."""
        if self.is_loaded(action):
            self.load = None
            self.trigger_time = None

    def trigger(self, now: "timedelta") -> "Action | None":
        """Triggers loaded action if available and if sufficient time has
        passed.
        """
        if self.load is None or (
            self.trigger_time is not None and self.trigger_time > now
        ):
            return None
        assert self.trigger_time is not None
        self.trigger_time += self.period
        return self.load

"""Class which repeats loaded action after a delay."""

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import timedelta

    from common.enum import Action


@dataclass
class DelayedAutoRepeat:
    """Class which repeats loaded action after a delay."""

    _delay: "timedelta"
    _period: "timedelta"
    _load: "Action | None" = field(default=None, init=False)
    _trigger_time: "timedelta | None" = field(default=None, init=False)

    def start(self, now: "timedelta", action: "Action") -> bool:
        """Loads a different action to be repeated."""
        if self._is_loaded(action):
            return False
        self._load = action
        self._trigger_time = now + self._delay
        return True

    def stop(self, action: "Action") -> None:
        """Removes currently loaded action."""
        if self._is_loaded(action):
            self._load = None
            self._trigger_time = None

    def trigger(self, now: "timedelta") -> "Action | None":
        """Triggers loaded action if available and if sufficient time has
        passed.
        """
        if self._load is None or (
            self._trigger_time is not None and self._trigger_time > now
        ):
            return None
        assert self._trigger_time is not None
        self._trigger_time += self._period
        return self._load

    def _is_loaded(self, action: "Action") -> bool:
        """Indicates if an action has been loaded."""
        return self._load == action

"""Keystroke to game op bindings."""

from dataclasses import InitVar, dataclass, field
from datetime import timedelta
from pathlib import Path

import pygame
import yaml

from common.enum import Action


@dataclass
class Controls:
    """Keystroke to game op bindings."""

    keybinding: InitVar[dict[str, str]]
    handling: InitVar[dict[str, int]]

    das: timedelta = field(init=False)
    arr: timedelta = field(init=False)
    _action_to_key: dict[Action, int] = field(default_factory=lambda: {}, init=False)
    _key_to_action: dict[int, Action] = field(default_factory=lambda: {}, init=False)

    def __post_init__(
        self, keybinding: dict[str, str], handling: dict[str, int]
    ) -> None:
        for action, keystroke in keybinding.items():
            action = action.upper()
            key = pygame.key.key_code(keystroke)
            self._action_to_key[Action[action]] = key
            self._key_to_action[key] = Action[action]

        self.das = timedelta(milliseconds=handling["das"])
        self.arr = timedelta(milliseconds=handling["arr"])

    def get_key_name(self, action: Action) -> str:
        """Returns the key name for the specified action."""
        return pygame.key.name(self._action_to_key[action])

    def parse(self, keycode: int) -> Action | None:
        """Parses input keystroke to game action."""
        return self._key_to_action.get(keycode, None)

    @classmethod
    def from_config(cls, config_path: Path) -> "Controls":
        """Constructs Controls from config file."""
        with open(config_path, encoding="utf8") as infile:
            cfg = yaml.safe_load(infile.read())
        return cls(**cfg)

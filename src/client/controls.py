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

    action_to_key: dict[Action, int] = field(default_factory=lambda: {}, init=False)
    key_to_action: dict[int, Action] = field(default_factory=lambda: {}, init=False)
    das: timedelta = field(init=False)
    arr: timedelta = field(init=False)

    def __post_init__(
        self, keybinding: dict[str, str], handling: dict[str, int]
    ) -> None:
        for action, keystroke in keybinding.items():
            action = action.upper()
            key = pygame.key.key_code(keystroke)
            self.action_to_key[Action[action]] = key
            self.key_to_action[key] = Action[action]

        self.das = timedelta(milliseconds=handling["das"])
        self.arr = timedelta(milliseconds=handling["arr"])

    def parse(self, keycode: int) -> Action | None:
        """Parses input keystroke to game action."""
        return self.key_to_action.get(keycode, None)

    @classmethod
    def from_config(cls, config_path: Path) -> "Controls":
        """Constructs Controls from config file."""
        with open(config_path, encoding="utf8") as infile:
            cfg = yaml.safe_load(infile.read())
        return cls(**cfg)

"""Game launch script."""

import sys
from pathlib import Path

import pygame

from client.controls import Controls
from client.presenter import Presenter
from client.timer import Timer
from client.view import DEFAULT_SIZE, View
from model.ruleset import Ruleset
from model.stacker import Stacker


def get_resource_path(*path: str) -> Path:
    """Constructs resources path. Uses sys._MEIPASS if running from .exe built by
    pyinstaller.
    """
    try:
        # pylint: disable=protected-access
        root_dir = Path(sys._MEIPASS)  # type: ignore[attr-defined]
    except AttributeError:
        root_dir = Path(__file__).resolve().parents[1]

    return root_dir.joinpath(*path)


def main():
    """Main loop."""
    pygame.init()
    screen = pygame.display.set_mode(DEFAULT_SIZE)
    font = pygame.font.Font(get_resource_path("resource", "FiraCode-Regular.ttf"), 16)

    controls = Controls.from_config(get_resource_path("resource", "controls.yml"))
    ruleset = Ruleset.from_config(
        Path.cwd() / "settings.yml", get_resource_path("resource", "guideline.yml")
    )

    stacker = Stacker(ruleset)
    view = View(ruleset.num_cols, ruleset.num_visible_rows, controls, font)
    presenter = Presenter(stacker, view)
    timer = Timer(controls.das, controls.arr)

    while True:
        timer.update()
        for event in pygame.event.get():
            try:
                presenter.handle(event, timer)
            except SystemExit:
                pygame.quit()
                sys.exit()

        while (action := timer.poll()) is not None:
            presenter.handle_action(action)

        presenter.paint(screen)
        pygame.display.update()


if __name__ == "__main__":
    main()

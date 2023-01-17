import sys
from pathlib import Path

import pygame

from client.controller import Controller
from client.controls import Controls
from client.timer import Timer
from client.view import DEFAULT_SIZE, View
from model.debug import debug_board, debug_pieces
from model.ruleset import Ruleset
from model.stacker import Stacker

ROOT_DIR = Path(__file__).resolve().parents[1]


def main():
    pygame.init()
    screen = pygame.display.set_mode(DEFAULT_SIZE)

    resource_dir = ROOT_DIR / "resource"
    controls_path = resource_dir / "controls.yml"
    ruleset_path = resource_dir / "guideline.yml"

    controls = Controls.from_config(controls_path)
    ruleset = Ruleset.from_config(ruleset_path)

    stacker = Stacker(ruleset)
    view = View(ruleset, controls)
    controller = Controller(view, stacker)
    timer = Timer(controls.das, controls.arr)
    # debug_board(stacker.board, stacker.current, True)

    # stacker.hard_drop()
    # stacker.soft_drop()
    # stacker.move_horizontal(1)
    # debug_board(stacker.board, stacker.current, True)

    while True:
        timer.update()
        for event in pygame.event.get():
            try:
                controller.handle(event, timer)
            except SystemExit:
                pygame.quit()
                sys.exit()

        while (action := timer.poll()) is not None:
            controller.handle_action(action)

        controller.paint(screen)
        pygame.display.update()


if __name__ == "__main__":
    main()

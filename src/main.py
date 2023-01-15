from pathlib import Path

import pygame

from client.controller import Controller
from client.view import DEFAULT_SIZE, View
from model.debug import debug_board, debug_pieces
from model.ruleset import Ruleset
from model.stacker import Stacker

ROOT_DIR = Path(__file__).resolve().parents[1]


def main():
    pygame.init()
    screen = pygame.display.set_mode(DEFAULT_SIZE)

    config_path = ROOT_DIR / "resource" / "guideline.yml"
    ruleset = Ruleset.from_config(config_path)
    stacker = Stacker(ruleset)

    view = View(ruleset)
    controller = Controller(view, stacker)
    debug_board(stacker.board, stacker.current, True)

    # stacker.hard_drop()
    # stacker.soft_drop()
    # stacker.move_horizontal(1)
    # stacker.hold()
    debug_board(stacker.board, stacker.current, True)

    print(view.piece.rects)
    print(view.ghost.rects)

    while True:
        controller.paint(screen)
        pygame.display.update()


if __name__ == "__main__":
    main()

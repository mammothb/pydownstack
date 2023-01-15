from pathlib import Path

import pygame

from model.debug import debug_board, debug_pieces
from model.ruleset import Ruleset
from model.stacker import Stacker

ROOT_DIR = Path(__file__).resolve().parents[1]


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    config_path = ROOT_DIR / "resource" / "guideline.yml"
    ruleset = Ruleset.from_config(config_path)
    stacker = Stacker(ruleset)
    debug_board(stacker.board, stacker.current, True)

    # stacker.hard_drop()
    # stacker.soft_drop()
    stacker.move_horizontal(1)
    debug_board(stacker.board, stacker.current, True)
    # print(ruleset)

    # debug_pieces(ruleset.polyminos)
    # while True:


if __name__ == "__main__":
    main()

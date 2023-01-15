from pathlib import Path

import pygame

from bag import Bag
from debug import debug_pieces
from ruleset import Ruleset
from stacker import Stacker

ROOT_DIR = Path(__file__).resolve().parents[1]


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    config_path = ROOT_DIR / "resource" / "guideline.yml"
    ruleset = Ruleset.from_config(config_path)
    stacker = Stacker(ruleset)
    stacker.board.print_debug()

    stacker.spawn_from_bag()
    # debug_pieces(ruleset.polyminos)


if __name__ == "__main__":
    main()

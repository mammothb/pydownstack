import copy

from common.enum import Mino
from model.ruleset import rotate


def debug_board(board, current, try_finalize=False) -> None:
    tmp = copy.deepcopy(board)
    if try_finalize:
        for coord in current.coords:
            tmp[coord] = current.mino
    print(f"    {' '.join(map(str, range(tmp.num_cols)))}")
    for i, line in enumerate(reversed(tmp.lines)):
        print(
            f"{tmp.num_rows - i - 1:2}| "
            f"{' '.join(map(lambda x: str(x.value) if x != Mino.EMPTY else '_', line.cells))}"
        )


def debug_pieces(polyminos) -> None:
    for mino, poly in polyminos.items():
        width = poly.width
        print(mino)
        for rot in range(4):
            print(rot)
            cells = [[0] * width for _ in range(width)]
            for coord in poly.coords:
                coord = rotate(coord, width, rot)
                cells[coord[1]][coord[0]] = 1

            for row in reversed(cells):
                print(f"{' '.join(map(str, row))}")

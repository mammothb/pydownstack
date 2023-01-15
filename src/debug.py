from ruleset import rotate


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

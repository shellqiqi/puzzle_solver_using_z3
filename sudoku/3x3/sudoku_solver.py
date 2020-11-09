from z3 import *

r_cnt = 9
c_cnt = 9


def read_puzzle(path):
    puzzle = []

    with open(path, mode='r') as f:
        for _ in range(r_cnt):
            row = []
            for c in f.readline().strip():
                row.append(int(c) if
                           c >= '1' and c <= '9'
                           else -1)
            puzzle.append(row)

    return puzzle


def solve_sudoku(puzzle):
    s = Solver()

    lattices = [[Int('(%d,%d)' % (r, c)) for c in range(c_cnt)]
                for r in range(r_cnt)]

    for r in range(r_cnt):
        for c in range(c_cnt):
            if puzzle[r][c] != -1:
                s.add(lattices[r][c] == puzzle[r][c])
            else:
                s.add(Or(lattices[r][c] == 1,
                         lattices[r][c] == 2,
                         lattices[r][c] == 3,
                         lattices[r][c] == 4,
                         lattices[r][c] == 5,
                         lattices[r][c] == 6,
                         lattices[r][c] == 7,
                         lattices[r][c] == 8,
                         lattices[r][c] == 9))

    def exclude_row_from(er, ec):
        for c in range(c_cnt):
            if c != ec:
                s.add(lattices[er][ec] != lattices[er][c])

    def exclude_col_from(er, ec):
        for r in range(r_cnt):
            if r != er:
                s.add(lattices[er][ec] != lattices[r][ec])

    def exclude_group_from(er, ec):
        mr = er // 3
        mc = ec // 3
        for r in range(3):
            for c in range(3):
                rr = 3 * mr + r
                cc = 3 * mc + c
                if not (rr == er and cc == ec):
                    s.add(lattices[er][ec] != lattices[rr][cc])

    for r in range(r_cnt):
        for c in range(c_cnt):
            exclude_row_from(r, c)
            exclude_col_from(r, c)
            exclude_group_from(r, c)

    if s.check() == unsat:
        return []

    m = s.model()
    color_map = []

    for r in range(r_cnt):
        row = []
        for c in range(c_cnt):
            row.append(m[lattices[r][c]].as_long())
        color_map.append(row)

    return color_map


def print_answer(color_map):
    if color_map == []:
        print('Invalid puzzle')
        return
    for r in range(r_cnt):
        for c in range(c_cnt):
            print(color_map[r][c], end='')
        print('')


puzzle = read_puzzle('sudoku/3x3/puzzle.txt')

color_map = solve_sudoku(puzzle)

print_answer(color_map)

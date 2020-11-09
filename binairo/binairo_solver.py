from z3 import *


def read_puzzle(path):
    puzzle = []
    r_cnt = 0
    c_cnt = 0

    with open(path, mode='r') as f:
        r_cnt, c_cnt = f.readline().split()
        r_cnt = int(r_cnt)
        c_cnt = int(c_cnt)
        for _ in range(r_cnt):
            row = []
            for c in f.readline().strip():
                row.append(int(c) if
                           c == '0' or
                           c == '1'
                           else -1)
            puzzle.append(row)

    return puzzle, r_cnt, c_cnt


def solve_puzzle(puzzle, r_cnt, c_cnt):
    s = Solver()

    lattices = [[Int('(%d,%d)' % (r, c)) for c in range(c_cnt)]
                for r in range(r_cnt)]

    for r in range(r_cnt):
        for c in range(c_cnt):
            if puzzle[r][c] == 0:
                s.add(lattices[r][c] == 0)
            elif puzzle[r][c] == 1:
                s.add(lattices[r][c] == 1)
            else:
                s.add(Or(lattices[r][c] == 0, lattices[r][c] == 1))

    for r in range(r_cnt):
        expr = 0
        for c in range(c_cnt):
            expr = expr + lattices[r][c]
        s.add(expr == c_cnt // 2)

    for c in range(c_cnt):
        expr = 0
        for r in range(r_cnt):
            expr = expr + lattices[r][c]
        s.add(expr == r_cnt // 2)

    for r in range(r_cnt):
        for c in range(c_cnt-2):
            s.add(Not(And(lattices[r][c] == lattices[r][c+1],
                          lattices[r][c+1] == lattices[r][c+2])))
            s.add(Implies(And(lattices[r][c] == 0, lattices[r][c+1] == 0),
                          lattices[r][c+2] == 1))
            s.add(Implies(And(lattices[r][c] == 1, lattices[r][c+1] == 1),
                          lattices[r][c+2] == 0))
            s.add(Implies(And(lattices[r][c+2] == 0, lattices[r][c+1] == 0),
                          lattices[r][c] == 1))
            s.add(Implies(And(lattices[r][c+2] == 1, lattices[r][c+1] == 1),
                          lattices[r][c] == 0))
            s.add(Implies(And(lattices[r][c] == 0, lattices[r][c+2] == 0),
                          lattices[r][c+1] == 1))
            s.add(Implies(And(lattices[r][c] == 1, lattices[r][c+2] == 1),
                          lattices[r][c+1] == 0))

    for c in range(c_cnt):
        for r in range(r_cnt-2):
            s.add(Not(And(lattices[r][c] == lattices[r+1][c],
                          lattices[r+1][c] == lattices[r+2][c])))
            s.add(Implies(And(lattices[r][c] == 0, lattices[r+1][c] == 0),
                          lattices[r+2][c] == 1))
            s.add(Implies(And(lattices[r][c] == 1, lattices[r+1][c] == 1),
                          lattices[r+2][c] == 0))
            s.add(Implies(And(lattices[r+2][c] == 0, lattices[r+1][c] == 0),
                          lattices[r][c] == 1))
            s.add(Implies(And(lattices[r+2][c] == 1, lattices[r+1][c] == 1),
                          lattices[r][c] == 0))
            s.add(Implies(And(lattices[r][c] == 0, lattices[r+2][c] == 0),
                          lattices[r+1][c] == 1))
            s.add(Implies(And(lattices[r][c] == 1, lattices[r+2][c] == 1),
                          lattices[r+1][c] == 0))

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


def print_answer(color_map, r_cnt, c_cnt):
    if color_map == []:
        print('Invalid puzzle')
        return
    for r in range(r_cnt):
        for c in range(c_cnt):
            print('▉' if color_map[r][c] == 1 else ' ', end='')
        print('')


puzzle, r_cnt, c_cnt = read_puzzle('binairo/puzzle.txt')

color_map = solve_puzzle(puzzle, r_cnt, c_cnt)

print_answer(color_map, r_cnt, c_cnt)

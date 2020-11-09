from z3 import *


def read_puzzle(path):
    r_cnt = 0
    c_cnt = 0
    row_sums = []
    col_sums = []

    with open(path, mode='r') as f:
        r_cnt, c_cnt = f.readline().split()
        r_cnt = int(r_cnt)
        c_cnt = int(c_cnt)
        row_sum_split = f.readline().split(' ')
        col_sum_split = f.readline().split(' ')
        for e in row_sum_split:
            row_sums.append(int(e))
        for e in col_sum_split:
            col_sums.append(int(e))

    return r_cnt, c_cnt, row_sums, col_sums


def solve_kakurasu(r_cnt, c_cnt, row_sums, col_sums):
    s = Solver()

    lattices = [[Bool('(%d,%d)' % (r, c)) for c in range(c_cnt)]
                for r in range(r_cnt)]

    row_value = [[Int('r(%d,%d)' % (r, c)) for c in range(c_cnt)]
                 for r in range(r_cnt)]

    col_value = [[Int('c(%d,%d)' % (r, c)) for c in range(c_cnt)]
                 for r in range(r_cnt)]

    for r in range(r_cnt):
        for c in range(c_cnt):
            rv = r + 1
            cv = c + 1
            s.add(Implies(lattices[r][c] == True,
                          And(row_value[r][c] == cv,
                              col_value[r][c] == rv)))
            s.add(Implies(lattices[r][c] == False,
                          And(row_value[r][c] == 0,
                              col_value[r][c] == 0)))

    for r in range(r_cnt):
        expr = 0
        for c in range(c_cnt):
            expr = expr + row_value[r][c]
        s.add(expr == row_sums[r])

    for c in range(c_cnt):
        expr = 0
        for r in range(r_cnt):
            expr = expr + col_value[r][c]
        s.add(expr == col_sums[c])

    if s.check() == unsat:
        return []

    m = s.model()
    color_map = []

    for r in range(r_cnt):
        row = []
        for c in range(c_cnt):
            row.append(m[lattices[r][c]])
        color_map.append(row)

    return color_map


def print_answer(color_map):
    if color_map == []:
        print('Invalid puzzle')
        return
    for r in range(r_cnt):
        for c in range(c_cnt):
            print('▉' if color_map[r][c] else '·', end='')
        print('')


r_cnt, c_cnt, row_sums, col_sums = read_puzzle('kakurasu/puzzle.txt')

color_map = solve_kakurasu(r_cnt, c_cnt, row_sums, col_sums)

print_answer(color_map)

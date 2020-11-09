from z3 import *


def read_puzzle(path):
    width = 0
    numbers = []
    hrz_cmp = []
    vtc_cmp = []

    with open(path, mode='r') as f:
        width = int(f.readline())

        for r in range(width * 2 - 1):
            line = f.readline().strip('\n')
            row_of_numbers = []
            row_of_hrz_cmp = []
            row_of_vtc_cmp = []

            for c in range(width * 2 - 1):
                ch = line[c]
                if r % 2 == 0:
                    # with numbers
                    if c % 2 == 0:
                        # numbers
                        row_of_numbers.append(-1 if ch == '?' else int(ch, 16))
                    else:
                        # compares
                        row_of_hrz_cmp.append(ch)
                else:
                    # without numbers
                    if c % 2 == 0:
                        # compares
                        row_of_vtc_cmp.append(ch)

            if r % 2 == 0:
                numbers.append(row_of_numbers)
                hrz_cmp.append(row_of_hrz_cmp)
            else:
                vtc_cmp.append(row_of_vtc_cmp)

    return width, numbers, hrz_cmp, vtc_cmp


def solve_puzzle(width, numbers, hrz_cmp, vtc_cmp):
    s = Solver()

    lattices = [[Int('(%d,%d)' % (r, c)) for c in range(width)]
                for r in range(width)]

    for r in range(width):
        for c in range(width):
            if numbers[r][c] != -1:
                s.add(lattices[r][c] == numbers[r][c])
            else:
                expr = False
                for i in range(width):
                    expr = Or(expr, lattices[r][c] == i+1)
                s.add(expr)

    def exclude_row_from(er, ec):
        for c in range(width):
            if c != ec:
                s.add(lattices[er][ec] != lattices[er][c])

    def exclude_col_from(er, ec):
        for r in range(width):
            if r != er:
                s.add(lattices[er][ec] != lattices[r][ec])

    for r in range(width):
        for c in range(width):
            exclude_row_from(r, c)
            exclude_col_from(r, c)

    # For hrz_cmp
    for r in range(width):
        for c in range(width-1):
            if hrz_cmp[r][c] == '<':
                s.add(lattices[r][c] < lattices[r][c+1])
            elif hrz_cmp[r][c] == '>':
                s.add(lattices[r][c] > lattices[r][c+1])

    # For vtc_cmp
    for c in range(width):
        for r in range(width-1):
            if vtc_cmp[r][c] == '^':
                s.add(lattices[r][c] < lattices[r+1][c])
            elif vtc_cmp[r][c] == 'v':
                s.add(lattices[r][c] > lattices[r+1][c])

    if s.check() == unsat:
        return []

    m = s.model()
    answer_map = []

    for r in range(width):
        row = []
        for c in range(width):
            row.append(m[lattices[r][c]].as_long())
        answer_map.append(row)

    return answer_map


def print_answer(width, answer_map):
    if answer_map == []:
        print('Invalid puzzle')
        return
    for r in range(width):
        for c in range(width):
            print('{:X}'.format(answer_map[r][c]), end='')
        print('')


width, numbers, hrz_cmp, vtc_cmp = read_puzzle('futoshiki/puzzle.txt')

answer_map = solve_puzzle(width, numbers, hrz_cmp, vtc_cmp)

print_answer(width, answer_map)

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
                           c == '1' or
                           c == '2' or
                           c == '3'
                           else -1)
            puzzle.append(row)

    return puzzle, r_cnt, c_cnt


def color_puzzle(puzzle, r_cnt, c_cnt, color_map=[]):
    s = Solver()

    lattices = [[Bool('(%d,%d)' % (r, c)) for c in range(c_cnt)]
                for r in range(r_cnt)]

    if len(color_map) > 0:
        for r in range(r_cnt):
            for c in range(c_cnt):
                if color_map[r][c] == 1:
                    s.add(lattices[r][c] == True)
                elif color_map[r][c] == 0:
                    s.add(lattices[r][c] == False)

    def get_N_color(r, c):
        return False if r == 0 else lattices[r-1][c]

    def get_S_color(r, c):
        return False if r == r_cnt-1 else lattices[r+1][c]

    def get_W_color(r, c):
        return False if c == 0 else lattices[r][c-1]

    def get_E_color(r, c):
        return False if c == c_cnt-1 else lattices[r][c+1]

    for r in range(r_cnt):
        for c in range(c_cnt):
            if puzzle[r][c] == 0:
                s.add(And(
                    lattices[r][c] == get_N_color(r, c),
                    lattices[r][c] == get_S_color(r, c),
                    lattices[r][c] == get_W_color(r, c),
                    lattices[r][c] == get_E_color(r, c)
                ))
            elif puzzle[r][c] == 1:
                s.add(Or(
                    And(
                        lattices[r][c] == get_N_color(r, c),
                        lattices[r][c] == get_S_color(r, c),
                        lattices[r][c] == get_W_color(r, c),
                        lattices[r][c] != get_E_color(r, c)
                    ),
                    And(
                        lattices[r][c] == get_N_color(r, c),
                        lattices[r][c] == get_S_color(r, c),
                        lattices[r][c] != get_W_color(r, c),
                        lattices[r][c] == get_E_color(r, c)
                    ),
                    And(
                        lattices[r][c] == get_N_color(r, c),
                        lattices[r][c] != get_S_color(r, c),
                        lattices[r][c] == get_W_color(r, c),
                        lattices[r][c] == get_E_color(r, c)
                    ),
                    And(
                        lattices[r][c] != get_N_color(r, c),
                        lattices[r][c] == get_S_color(r, c),
                        lattices[r][c] == get_W_color(r, c),
                        lattices[r][c] == get_E_color(r, c)
                    )
                ))
            elif puzzle[r][c] == 2:
                s.add(Or(
                    And(
                        lattices[r][c] == get_N_color(r, c),
                        lattices[r][c] == get_S_color(r, c),
                        lattices[r][c] != get_W_color(r, c),
                        lattices[r][c] != get_E_color(r, c)
                    ),
                    And(
                        lattices[r][c] == get_N_color(r, c),
                        lattices[r][c] != get_S_color(r, c),
                        lattices[r][c] == get_W_color(r, c),
                        lattices[r][c] != get_E_color(r, c)
                    ),
                    And(
                        lattices[r][c] != get_N_color(r, c),
                        lattices[r][c] == get_S_color(r, c),
                        lattices[r][c] == get_W_color(r, c),
                        lattices[r][c] != get_E_color(r, c)
                    ),
                    And(
                        lattices[r][c] == get_N_color(r, c),
                        lattices[r][c] != get_S_color(r, c),
                        lattices[r][c] != get_W_color(r, c),
                        lattices[r][c] == get_E_color(r, c)
                    ),
                    And(
                        lattices[r][c] != get_N_color(r, c),
                        lattices[r][c] == get_S_color(r, c),
                        lattices[r][c] != get_W_color(r, c),
                        lattices[r][c] == get_E_color(r, c)
                    ),
                    And(
                        lattices[r][c] != get_N_color(r, c),
                        lattices[r][c] != get_S_color(r, c),
                        lattices[r][c] == get_W_color(r, c),
                        lattices[r][c] == get_E_color(r, c)
                    )
                ))
            elif puzzle[r][c] == 3:
                s.add(Or(
                    And(
                        lattices[r][c] == get_N_color(r, c),
                        lattices[r][c] != get_S_color(r, c),
                        lattices[r][c] != get_W_color(r, c),
                        lattices[r][c] != get_E_color(r, c)
                    ),
                    And(
                        lattices[r][c] != get_N_color(r, c),
                        lattices[r][c] == get_S_color(r, c),
                        lattices[r][c] != get_W_color(r, c),
                        lattices[r][c] != get_E_color(r, c)
                    ),
                    And(
                        lattices[r][c] != get_N_color(r, c),
                        lattices[r][c] != get_S_color(r, c),
                        lattices[r][c] == get_W_color(r, c),
                        lattices[r][c] != get_E_color(r, c)
                    ),
                    And(
                        lattices[r][c] != get_N_color(r, c),
                        lattices[r][c] != get_S_color(r, c),
                        lattices[r][c] != get_W_color(r, c),
                        lattices[r][c] == get_E_color(r, c)
                    )
                ))
            else:
                pass

    for r in range(r_cnt-1):
        for c in range(c_cnt-1):
            s.add(Not(And(
                lattices[r][c] == lattices[r+1][c+1],
                lattices[r+1][c] == lattices[r][c+1],
                lattices[r][c] != lattices[r+1][c]
            )))

    for r in range(r_cnt):
        for c in range(c_cnt):
            s.add(Not(And(
                lattices[r][c] != get_N_color(r, c),
                lattices[r][c] != get_S_color(r, c),
                lattices[r][c] != get_W_color(r, c),
                lattices[r][c] != get_E_color(r, c)
            )))

    if s.check() == unsat:
        return None

    color_map = []

    for r in range(r_cnt):
        row = []
        for c in range(c_cnt):
            s.push()
            s.add(Bool('(%d,%d)' % (r, c)) == True)
            if s.check() == unsat:
                row.append(0)
                s.pop()
                s.add(Bool('(%d,%d)' % (r, c)) == False)
            else:
                s.pop()
                s.push()
                s.add(Bool('(%d,%d)' % (r, c)) == False)
                if s.check() == unsat:
                    row.append(1)
                    s.pop()
                    s.add(Bool('(%d,%d)' % (r, c)) == True)
                else:
                    row.append(-1)
                    s.pop()
        color_map.append(row)

    return color_map


def print_color_map(color_map):
    for r in color_map:
        for c in r:
            if c == 1:
                print('▉', end='')
            elif c == 0:
                print(' ', end='')
            else:
                print('?', end='')
        print('')


def print_puzzle(puzzle, color_map, r_cnt, c_cnt):
    for r in range(r_cnt+1):
        for c in range(c_cnt+1):
            # point
            if r == 0:
                if c == 0:
                    print('▉' if color_map[r][c] == True else '·', end='')
                elif c == c_cnt:
                    print('▉' if color_map[r][c-1] == True else '·', end='')
                else:
                    print('▉' if color_map[r][c] == True or
                          color_map[r][c-1] == True else '·', end='')
            elif r == r_cnt:
                if c == 0:
                    print('▉' if color_map[r-1][c] == True else '·', end='')
                elif c == c_cnt:
                    print('▉' if color_map[r-1][c-1] == True else '·', end='')
                else:
                    print('▉' if color_map[r-1][c] == True or
                          color_map[r-1][c-1] == True else '·', end='')
            else:
                if c == 0:
                    print('▉' if color_map[r][c] == True or
                          color_map[r-1][c] == True else '·', end='')
                elif c == c_cnt:
                    print('▉' if color_map[r][c-1] == True or
                          color_map[r-1][c-1] == True else '·', end='')
                else:
                    if (color_map[r-1][c-1] == True and
                        color_map[r-1][c] == True and
                        color_map[r][c-1] == True and
                        color_map[r][c] == True
                        ) or (
                        color_map[r-1][c-1] == False and
                        color_map[r-1][c] == False and
                        color_map[r][c-1] == False and
                        color_map[r][c] == False
                    ):
                        print('·', end='')
                    else:
                        print('▉', end='')
            # rows
            if c < c_cnt:
                if r == 0:
                    print('▉' if color_map[r][c] == True else '×', end='')
                elif r == r_cnt:
                    print('▉' if color_map[r-1][c] == True else '×', end='')
                else:
                    print('▉' if color_map[r-1][c] != color_map[r][c] else
                          '×', end='')
        print('')
        if r < r_cnt:
            for c in range(c_cnt+1):
                # cols
                if c == 0:
                    print('▉' if color_map[r][c] == True else '×', end='')
                elif c == c_cnt:
                    print('▉' if color_map[r][c-1] == True else '×', end='')
                else:
                    print('▉' if color_map[r][c-1] !=
                          color_map[r][c] else '×', end='')
                # cells
                if c < c_cnt:
                    print(puzzle[r][c] if puzzle[r][c] != -1 else ' ', end='')
            print('')


def check_connectivity(color_map, r_cnt, c_cnt):
    s = Solver()
    lattices = [[Bool('(%d,%d)' % (r, c)) for c in range(c_cnt)]
                for r in range(r_cnt)]

    def get_first_island():
        for r in range(r_cnt):
            for c in range(c_cnt):
                if color_map[r][c] == 1:
                    return lattices[r][c]

    border = Bool('border')
    first_island = get_first_island()

    def connect_from_lake(r, c):
        if r > 0:
            if color_map[r-1][c] == 0:
                s.add(lattices[r][c] == lattices[r-1][c])
        else:
            s.add(lattices[r][c] == border)
        if r < r_cnt-1:
            if color_map[r+1][c] == 0:
                s.add(lattices[r][c] == lattices[r+1][c])
        else:
            s.add(lattices[r][c] == border)
        if c > 0:
            if color_map[r][c-1] == 0:
                s.add(lattices[r][c] == lattices[r][c-1])
        else:
            s.add(lattices[r][c] == border)
        if c < c_cnt-1:
            if color_map[r][c+1] == 0:
                s.add(lattices[r][c] == lattices[r][c+1])
        else:
            s.add(lattices[r][c] == border)

    def connect_from_island(r, c):
        if r > 0:
            if color_map[r-1][c] == 1:
                s.add(lattices[r][c] == lattices[r-1][c])
        if r < r_cnt-1:
            if color_map[r+1][c] == 1:
                s.add(lattices[r][c] == lattices[r+1][c])
        if c > 0:
            if color_map[r][c-1] == 1:
                s.add(lattices[r][c] == lattices[r][c-1])
        if c < c_cnt-1:
            if color_map[r][c+1] == 1:
                s.add(lattices[r][c] == lattices[r][c+1])

    # Add connectivities
    for r in range(r_cnt):
        for c in range(c_cnt):
            if color_map[r][c] == 0:
                connect_from_lake(r, c)
            elif color_map[r][c] == 1:
                connect_from_island(r, c)

    def is_mul_islands():
        for r in range(r_cnt):
            for c in range(c_cnt):
                if color_map[r][c] == 1:
                    s.push()
                    s.add(first_island == True)
                    s.add(lattices[r][c] == False)
                    if s.check() == sat:
                        s.pop()
                        return True
                    else:
                        s.pop()
        return False

    def is_mul_lakes():
        for r in range(r_cnt):
            for c in range(c_cnt):
                if color_map[r][c] == 0:
                    s.push()
                    s.add(border == True)
                    s.add(lattices[r][c] == False)
                    if s.check() == sat:
                        s.pop()
                        return True
                    else:
                        s.pop()
        return False

    def try_block_islands(br, bc):
        for r in range(r_cnt):
            for c in range(c_cnt):
                if color_map[r][c] == -1 and (not (r == br and c == bc)):
                    if r > 0:
                        if (color_map[r-1][c] == 1 or color_map[r-1][c] == -1) and (not (r-1 == br and c == bc)):
                            s.add(lattices[r][c] == lattices[r-1][c])
                    if r < r_cnt-1:
                        if (color_map[r+1][c] == 1 or color_map[r+1][c] == -1) and (not (r+1 == br and c == bc)):
                            s.add(lattices[r][c] == lattices[r+1][c])
                    if c > 0:
                        if (color_map[r][c-1] == 1 or color_map[r][c-1] == -1) and (not (r == br and c == bc-1)):
                            s.add(lattices[r][c] == lattices[r][c-1])
                    if c < c_cnt-1:
                        if (color_map[r][c+1] == 1 or color_map[r][c+1] == 1) and (not (r == br and c == bc+1)):
                            s.add(lattices[r][c] == lattices[r][c+1])

    def try_block_lakes(br, bc):
        for r in range(r_cnt):
            for c in range(c_cnt):
                if color_map[r][c] == -1 and (not (r == br and c == bc)):
                    if r > 0:
                        if (color_map[r-1][c] == 0 or color_map[r-1][c] == -1) and (not (r-1 == br and c == bc)):
                            s.add(lattices[r][c] == lattices[r-1][c])
                    else:
                        s.add(lattices[r][c] == border)
                    if r < r_cnt-1:
                        if (color_map[r+1][c] == 0 or color_map[r+1][c] == -1) and (not (r+1 == br and c == bc)):
                            s.add(lattices[r][c] == lattices[r+1][c])
                    else:
                        s.add(lattices[r][c] == border)
                    if c > 0:
                        if (color_map[r][c-1] == 0 or color_map[r][c-1] == -1) and (not (r == br and c == bc-1)):
                            s.add(lattices[r][c] == lattices[r][c-1])
                    else:
                        s.add(lattices[r][c] == border)
                    if c < c_cnt-1:
                        if (color_map[r][c+1] == 0 or color_map[r][c+1] == -1) and (not (r == br and c == bc+1)):
                            s.add(lattices[r][c] == lattices[r][c+1])
                    else:
                        s.add(lattices[r][c] == border)

    # try block ? for islands
    for r in range(r_cnt):
        for c in range(c_cnt):
            if color_map[r][c] == -1:
                s.push()
                try_block_islands(r, c)
                result = is_mul_islands()
                s.pop()
                if result:
                    color_map[r][c] = 1
                    connect_from_island(r, c)

    # try block ? for lakes
    for r in range(r_cnt):
        for c in range(c_cnt):
            if color_map[r][c] == -1:
                s.push()
                try_block_lakes(r, c)
                result = is_mul_lakes()
                s.pop()
                if result:
                    color_map[r][c] = 0
                    connect_from_lake(r, c)

    return color_map


def is_invalid(color_map):
    if color_map == None:
        return True
    return False


def is_complete(color_map):
    if color_map == None:
        return True
    for r in color_map:
        for c in r:
            if c == -1:
                return False
    return True


puzzle, r_cnt, c_cnt = read_puzzle('slitherlink/puzzle.txt')

color_map = []
i = 0

while True:
    i = i + 1
    print('pass %d' % i)

    color_map = color_puzzle(puzzle, r_cnt, c_cnt, color_map)
    if is_invalid(color_map):
        print('Invalid puzzle')
        break
    if is_complete(color_map):
        print_puzzle(puzzle, color_map, r_cnt, c_cnt)
        break

    color_map = check_connectivity(color_map, r_cnt, c_cnt)
    if is_complete(color_map):
        print_puzzle(puzzle, color_map, r_cnt, c_cnt)
        break


# This was originally written in C++
# Rewritten in Python

def read(loc: str) -> list[list[str]]:
    with open(loc) as f:
        r = f.readlines()
        return [list(row.strip()) for row in r]


def step_row(row: list[str], val: str) -> list[str]:
    Z = '.'
    k = 0
    new_row = [x for x in row] # Creating a copy of my list. Otherwise: Side-effect hell
    first_spot = row[0]
    last_spot = row[-1]
    while k < len(row) - 1:
        if row[k] == val and row[k+1] == Z:
            new_row[k] = Z
            new_row[k+1] = val
            k += 1
        k += 1
    if last_spot == val and first_spot == Z:
        new_row[0] = val
        new_row[-1] = Z

    return new_row


def step(grid: list[list[str]]) -> list[list[str]]:
    len_y = len(grid)
    len_x = len(grid[0])
    new_grid_rows: list[list[str]] = [ step_row(row, '>') for row in grid ]

    transposed_rows = [ [new_grid_rows[y][x] for y in range(len_y)] for x in range(len_x) ]

    new_grid_transposed = [ step_row(row, 'v') for row in transposed_rows ]

    new_grid = [ [new_grid_transposed[x][y] for x in range(len_x)] for y in range(len_y) ]

    return new_grid


def stringify_grid(grid: list[list[str]]) -> str:
    return ''.join("".join(row) + '\n' for row in grid)


def first(loc: str = './data/25.csv') -> int:
    grid = read(loc)
    new_grid = step(grid)
    counter = 1

    # print("Starting grid:")
    # print(stringify_grid(grid))

    while grid != new_grid:
        # print(f"Grid after {counter} iterations:")
        # print(stringify_grid(new_grid))
        grid = new_grid
        new_grid = step(grid)
        counter += 1


    print(counter)
    return counter


if __name__ == '__main__':
    first()

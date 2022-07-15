class Octopuses: 
    def __init__(self, loc: str):
        with open(loc) as f:
            r = f.readlines()
            grid = [ [int(x) for x in row[:-1]] for row in r ]

        self.grid = grid
        self.len_x = len(grid)
        self.len_y = len(grid[0])
        self.flashes = 0
        self.number_steps = 0


    def step(self):
        self.number_steps += 1
        for x in range(self.len_x):
            for y in range(self.len_y):
                self.grid[x][y] += 1

        flashed = True
        flashed_positions: set[tuple[int, int]] = set()
        while flashed:
            flashed = False
            for x in range(self.len_x):
                for y in range(self.len_y):
                    if self.grid[x][y] <= 9:
                        continue
                    assert (x, y) not in flashed_positions # Unnecessary, this is impossible.
                    flashed_positions.add((x, y))
                    flashed = True
                    self.flashes += 1
                    self.grid[x][y] = 0
                    for a, b in self._neighbours(x, y):
                        self.grid[a][b] += 1

        for x, y in flashed_positions:
            self.grid[x][y] = 0


    def _neighbours(self, x: int, y: int) -> list[tuple[int, int]]:
        adj = [
                (x-1, y-1),
                (x-1, y  ),
                (x-1, y+1),
                (x  , y-1),
                (x  , y+1),
                (x+1, y-1),
                (x+1, y  ),
                (x+1, y+1),
                ]
        adj = filter(lambda l: 0 <= l[0] < self.len_x and 0 <= l[1] < self.len_y, adj)
        return list(adj)


def first(loc: str = "./data/11.csv") -> int:
    octopi = Octopuses(loc)
    for _ in range(100):
        octopi.step()

    print(octopi.flashes)
    return octopi.flashes


def second(loc: str = "./data/11.csv") -> int:
    octopi = Octopuses(loc)
    previous_flashes = octopi.flashes
    grid_size = octopi.len_x * octopi.len_y

    # Maximal number of flashes = grid_size. Check until the number of flashes incremented that much in a single turn
    while octopi.flashes != previous_flashes + grid_size:
        previous_flashes = octopi.flashes
        octopi.step()

    print(octopi.number_steps)
    return octopi.number_steps


first()
second()


import math
import heapq


class Node:
    def __init__(self, x: int, y: int, risk: int):
        self.x: int = x
        self.y: int = y
        self.dist: int = math.inf
        self.risk: int = risk
        self.seen: bool = False
        self.nbrs: list[Node] = []

    def __len__(self):
        return self.dist

    def __lt__(self, other):
        return self.dist < other.dist

    def __repr__(self):
        return f"({self.x},{self.y}): {self.risk} , {self.dist}"


def read(loc: str, times_5: bool = False) -> list[list[Node]]:
    def wrap_nines(x: int):
        if 1 <= x <= 9:
            return x
        else:
            return x-9

    with open(loc) as f:
        r = f.readlines()
        rows = []
        for row in r:
            row = row.strip()
            row = list(map(int, row))

            if times_5:
                new_row = []
                for k in range(5):
                    new_row.extend([wrap_nines(x + k) for x in row])
                row = new_row

            rows.append(row)

        if times_5:
            new_rows: list[list[int]] = []
            for k in range(5):
                for row in rows:
                    new_rows.append([wrap_nines(x + k) for x in row])
            rows = new_rows

    grid = [[Node(i, j, risk) for j, risk in enumerate(row)] for i, row in enumerate(rows)]
    for i, row in enumerate(grid):
        for j, node in enumerate(row):
            node.nbrs += [grid[x][y] for x, y in getNghbrs(grid, i, j)]
    return grid


def getNghbrs(grid: list[list], i: int, j: int) -> list[tuple[int,int]]:
    n = len(grid)
    m = len(grid[0])
    cnds = [
        (i - 1, j),
        (i + 1, j),
        (i, j - 1),
        (i, j + 1)
    ]
    return list(filter(lambda l: 0 <= l[0] < n and 0 <= l[1] < m, cnds))


def solve(grid: list[list[Node]]) -> int:
    start = grid[0][0]
    start.dist = 0
    heap = [start]
    while heap:
        # heapq.heapify(heap) # Unnecessary
        visiting = heapq.heappop(heap)
        if visiting.x == len(grid)-1 and visiting.y == len(grid[0])-1:
            return visiting.dist
        if visiting.seen:
            continue
        visiting.seen = True
        for candidate in filter(lambda l: not l.seen, visiting.nbrs):
            if candidate.dist == math.inf:
                candidate.dist = visiting.dist + candidate.risk
                heapq.heappush(heap, candidate)
            else:
                candidate.dist = min(candidate.dist, visiting.dist + candidate.risk)
    return -1 # Unreachable.


def first(loc: str = "./data/15.csv"):
    grid = read(loc)
    res = solve(grid)
    print(res)
    return res


def second(loc: str = "./data/15.csv"):
    grid = read(loc, True)
    res = solve(grid)
    print(res)
    return res

first()
second()


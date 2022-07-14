import csv
import math
import heapq
from pprint import pp



class Node:
    def __init__(self, x: int, y: int, risk: int):
        self.x = x
        self.y = y
        self.dist = math.inf
        self.risk = risk
        self.seen = False
        self.nbrs = []

    def __len__(self):
        return self.dist

    def __lt__(self, other):
        return self.dist < other.dist

    def __repr__(self):
        return f"({self.x},{self.y}): {self.risk} , {self.dist}"


def read(file: str):
    with open(file) as f:
        r = csv.reader(f)
        # return [[risk for risk in row] for row in r]

        # heap = []
        # for i, row in enumerate(r):
        #     for j, risk in enumerate(row):
        #         heap.append(Node(i, j, risk))
        # return heap

        # d = {}
        # for i, row in enumerate(r):
        #     for j, risk in enumerate(row):
        #         d[(i, j)] = Node(i, j, risk)
        # return d

        grid = [[Node(i, j, int(risk)) for j, risk in enumerate(row)] for i, row in enumerate(r)]
        for i, row in enumerate(grid):
            for j, node in enumerate(row):
                node.nbrs += [grid[x][y] for x, y in getNghbrs(grid, i, j)]
        return grid


def wrap_nines(x: int):
    if 1 <= x <= 9:
        return x
    else:
        return x-9



def write(test: bool = False):
    file = "./data/15"
    if test:
        file += "test"
    file += ".csv"

    with open(file) as fi:
        r = csv.reader(fi)
        new_rows = []
        for row in r:
            new_row = []
            for k in range(5):
                new_row += [wrap_nines(int(x) + k) for x in row]
            new_rows.append(new_row)

        new_grid = []
        for k in range(5):
            for row in new_rows:
                new_grid.append([wrap_nines(x + k) for x in row])

    with open("./data/15b.csv", 'w') as fo:
        w = csv.writer(fo)
        w.writerows(new_grid)





def getNghbrs(grid: list[list[...]], i: int, j: int):
    """n, m dimensions of grid, i, j position"""
    n = len(grid)
    m = len(grid[0])
    cnds = [
        (i - 1, j),
        (i + 1, j),
        (i, j - 1),
        (i, j + 1)
    ]
    return ((x, y) for (x, y) in cnds if 0 <= x < n and 0 <= y < m)


def first(grid: list[list[Node, ...]]):
    start = grid[0][0]
    start.dist = 0
    heap = [start]
    while heap:
        # heapq.heapify(heap)
        visiting = heapq.heappop(heap)
        if visiting.x == len(grid)-1 and visiting.y == len(grid[0])-1:
            print(f"Hue: {visiting.dist=}")
            break
        if visiting.seen:
            continue
        visiting.seen = True
        # Alternative: Just do an if instead of a filter! Is this filter truly better/worth it? Benchmark?
        for candidate in filter(lambda l: not l.seen, visiting.nbrs):
            print(candidate.dist, visiting.dist, candidate.risk)
            if candidate.dist == math.inf:
                candidate.dist = visiting.dist + candidate.risk
                heapq.heappush(heap, candidate)
            else:
                candidate.dist = min(candidate.dist, visiting.dist + candidate.risk)




def second(grid: list[list[Node, ...]], heapify: bool):
    start = grid[0][0]
    start.dist = 0
    heap = [start]
    results = [[None for _ in range(len(grid[0]))] for _ in range(len(grid))]
    count_updates = 0
    while heap:
        if heapify:
            heapq.heapify(heap)
        visiting = heapq.heappop(heap)
        if visiting.seen:
            continue
        visiting.seen = True
        results[visiting.x][visiting.y] = visiting.dist
        # Alternative: Just do an if instead of a filter! Is this filter truly better/worth it? Benchmark?
        for candidate in filter(lambda l: not l.seen, visiting.nbrs):
            if candidate.dist == math.inf:
                candidate.dist = visiting.dist + candidate.risk
                heapq.heappush(heap, candidate)
            else:
                if candidate.dist > visiting.dist + candidate.risk:
                    count_updates += 1
                candidate.dist = min(candidate.dist, visiting.dist + candidate.risk)
    return results, count_updates


data_names = ["", "test", "b", "testb"]
files = ["./data/15" + x + ".csv" for x in data_names]
n = 3
print(len(read(files[n]))**2)
resulta = second(read(files[n]), False)
resultb = second(read(files[n]), True)
pp(resulta[1])
pp(resultb[1])
assert resulta == resultb
# 249001
# write()
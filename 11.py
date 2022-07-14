import csv
import numpy as np

def read():
    return np.loadtxt(f'./data/11.csv', int, delimiter=',')


def getNghbrs(n: int, m: int, i: int, j: int):
    """n, m dimensions of grid, i, j position"""
    cnds = [
        (i - 1, j),
        (i + 1, j),
        (i, j - 1),
        (i, j + 1),
        (i - 1, j - 1),
        (i - 1, j + 1),
        (i + 1, j - 1),
        (i + 1, j + 1),

    ]
    return [(x, y) for (x, y) in cnds if inGrid(n, m, x, y)]


def inGrid(n: int, m: int, i: int, j: int):
    return 0 <= i < n and 0 <= j < m


def turn():
    pass


def second(data: np.ndarray, runtime: int = 100):
    n, m = data.shape
    total_flashes = 0
    for k in range(runtime):
        data = np.add(data, np.ones((n,m), dtype=int))
        print(data)
        flashedCords = []
        flashed = True
        while flashed:
            flashed = False
            for i in range(n):
                for j in range(m):
                    if data[i, j] > 9:
                        assert (i, j) not in flashedCords
                        total_flashes += 1
                        flashed = True
                        data[i, j] = 0
                        flashedCords.append((i, j))
                        for x, y in getNghbrs(n, m, i, j):
                            data[x, y] += 1
        for x, y in flashedCords:
            data[x, y] = 0
        if len(flashedCords) == data.size:
            return k


print(second(read(), 1000))



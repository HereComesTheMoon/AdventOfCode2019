import numpy as np


def read(loc: str):
    with open(loc) as f:
        r = f.readlines()
        data = [ [ int(x) for x in row[:-1]] for row in r ] # row[:-1] because of newline character
        return np.asarray(data)


def getNghbrsOld(n: int, m: int, i: int, j: int) -> list:
    """n, m dimensions of grid, i, j position"""
    if i not in range(n) or j not in range(m):
        return []
    nghbrs = []
    if 0 < i:
        nghbrs.append((i - 1, j))
    if i < n - 1:
        nghbrs.append((i + 1, j))
    if 0 < j:
        nghbrs.append((i, j - 1))
    if j < m - 1:
        nghbrs.append((i, j + 1))
    return nghbrs


def getNghbrs(n: int, m: int, i: int, j: int) -> list[tuple[int, int]]:
    """n, m dimensions of grid, i, j position"""
    cnds = [
        (i - 1, j),
        (i + 1, j),
        (i, j - 1),
        (i, j + 1)
    ]
    return [(x, y) for (x, y) in cnds if inGrid(n, m, x, y)]


def inGrid(n: int, m: int, i: int, j: int) -> bool:
    return 0 <= i < n and 0 <= j < m


def lowPoints(data: np.ndarray) -> list[tuple[int, int]]:
    n, m = data.shape
    lowPoints = []
    for i in range(n):
        for j in range(m):
            if data[i, j] < min([data[x, y] for x, y in getNghbrs(n, m, i, j)]):
                lowPoints.append((i, j))
    return lowPoints


def findBasin(data: np.ndarray, i: int, j: int) -> set[tuple[int, int]]:
    n, m = data.shape
    basin = {(i, j)}
    seen = np.zeros((n, m))
    stack = [(i, j)]

    for x, y in stack:
        if seen[x, y]:
            continue
        seen[x, y] = 1
        for a, b in getNghbrs(n, m, x, y):
            if data[a, b] == 9 or seen[a, b]:
                continue
            stack.append((a, b))
            basin.add((a, b))
    return basin



def first(loc: str = './data/9.txt') -> int:
    data = read(loc)
    results = lowPoints(data)
    # print(len(results), lowPoints)
    res = sum( data[x,y] + 1 for x, y in results )
    print(res)
    return res


def second(loc: str = './data/9.txt') -> int:
    data = read(loc)
    lPts = lowPoints(data)
    basins = []
    for x, y in lPts:
        basins.append(findBasin(data, x, y))

    basins.sort(key=len)

    # for x in basins:
        # print(f"Length basin: {len(x)}")
        # print(x)
    # print(sum(len(x) for x in basins))
    # print( np.count_nonzero(data == 9))

    res = len(basins[-1])*(len(basins[-2]))*(len(basins[-3]))
    print(res)
    return res

if __name__ == '__main__':
    first()
    second()

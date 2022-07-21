def read(loc: str = "./data/2.csv") -> list[tuple[str, int]]:
    with open(loc) as f:
        r = f.readlines()
        rows = [row.split() for row in r]
        return [(row[0], int(row[1])) for row in rows]


def first() -> int:
    horizontalPos = 0
    depth = 0
    data = read()
    for x, k in data:
        if x == 'forward':
            horizontalPos += k
        if x == 'up':
            depth -= k
        if x == 'down':
            depth += k
    res = horizontalPos*depth
    print(res)
    return res


def second() -> int:
    horizontalPos = 0
    depth = 0
    aim = 0
    data = read()
    for x, k in data:
        if x == 'forward':
            horizontalPos += k
            depth += aim*k
        if x == 'up':
            aim -= k
        if x == 'down':
            aim += k
    res = horizontalPos*depth
    print(res)
    return res


if __name__ == '__main__':
    first()
    second()


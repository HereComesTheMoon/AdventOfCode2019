from collections import namedtuple

Point = namedtuple('Point', 'x y')

def read(loc: str):
    with open(loc) as f:
        r = f.readlines()
        rows = [row.replace(" -> ", ",") for row in r]
        rows = [row.split(",") for row in rows]
        data: list[tuple[Point, Point]] = [(Point(int(x[0]), int(x[1])), Point(int(x[2]), int(x[3]))) for x in rows]
    return data

def line(p: Point, q: Point) -> list[tuple[int, int]]:
    if p.x == q.x:
        return [(p.x, z) for z in range(min(p.y, q.y), max(p.y, q.y)+1)]
    if p.y == q.y:
        return [(z, p.y) for z in range(min(p.x, q.x), max(p.x, q.x)+1)]
    return []

def line2(p: Point, q: Point) -> list[tuple[int, int]]:
    if p.x == q.x:
        return [(p.x, z) for z in range(min(p.y, q.y), max(p.y, q.y)+1)]
    if p.y == q.y:
        return [(z, p.y) for z in range(min(p.x, q.x), max(p.x, q.x)+1)]
    d = (p.x-q.x, p.y-q.y)
    d = Point(d[0] // abs(d[0]), d[1] // abs(d[0]))
    if abs(d.x) == abs(d.y):
        return [(p.x - k*d.x, p.y - k*d.y) for k in range(0, abs(p.x - q.x) + 1)]

    return []

def first(loc: str = './data/5.csv') -> int:
    karte = [[0 for _ in range(1000)] for _ in range(1000)] # 1000 ~ bound for highest appearing value.
    for x, y in read(loc):
        for a, b in line(x, y):
            karte[a][b] += 1

    count = 0
    for row in karte:
        for column in row:
           count += (column >= 2)

    print(count)
    return count

def second(loc: str = './data/5.csv') -> int:
    karte = [[0 for _ in range(1000)] for _ in range(1000)]
    for x, y in read(loc):
        for a, b in line2(x, y):
            karte[a][b] += 1

    count = 0
    for row in karte:
        for column in row:
            count += (column >= 2)

    print(count)
    return count

first()
second()


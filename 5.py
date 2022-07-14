import csv
from collections import namedtuple

Point = namedtuple('Point', 'x y')

def read():
    with open('./data/5.csv') as f:
        r = csv.reader(f)
        data = [(Point(int(x[0]), int(x[1])), Point(int(x[2]), int(x[3]))) for x in r]
    return data

def line(p, q):
    if p.x == q.x:
        return [(p.x, z) for z in range(min(p.y, q.y), max(p.y, q.y)+1)]
    if p.y == q.y:
        return [(z, p.y) for z in range(min(p.x, q.x), max(p.x, q.x)+1)]
    return []

def line2(p, q):
    if p.x == q.x:
        return [(p.x, z) for z in range(min(p.y, q.y), max(p.y, q.y)+1)]
    if p.y == q.y:
        return [(z, p.y) for z in range(min(p.x, q.x), max(p.x, q.x)+1)]
    d = (p.x-q.x, p.y-q.y)
    d = Point(d[0] // abs(d[0]), d[1] // abs(d[0]))
    if abs(d.x) == abs(d.y):
        return [(p.x - k*d.x, p.y - k*d.y) for k in range(0, abs(p.x - q.x) + 1)]

    return []
def first():
    karte = [[0 for _ in range(1000)] for _ in range(1000)]
    for x, y in read():
        for a, b in line(x, y):
            karte[a][b] += 1

    count = 0
    for row in karte:
        for column in row:
           count += column >= 2

    return count

def second():
    karte = [[0 for _ in range(1000)] for _ in range(1000)]
    for x, y in read():
        for a, b in line2(x, y):
            karte[a][b] += 1

    count = 0
    for row in karte:
        for column in row:
            count += column >= 2

    return count

print(second())
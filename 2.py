import csv

def first():
    horizontalPos = 0
    depth = 0
    with open("./data/2.csv") as f:
        reader = csv.reader(f, delimiter=' ')
        data = [(x[0], int(x[1])) for x in reader]
    for x, k in data:
        if x == 'forward':
            horizontalPos += k
        if x == 'up':
            depth -= k
        if x == 'down':
            depth += k
    print(f"{horizontalPos=}, {depth=}, {horizontalPos*depth=}")

def second():
    horizontalPos = 0
    depth = 0
    aim = 0
    with open("./data/2.csv") as f:
        reader = csv.reader(f, delimiter=' ')
        data = [(x[0], int(x[1])) for x in reader]
    for x, k in data:
        if x == 'forward':
            horizontalPos += k
            depth += aim*k
        if x == 'up':
            aim -= k
        if x == 'down':
            aim += k
    print(f"{horizontalPos=}, {depth=}, {horizontalPos*depth=}")


second()
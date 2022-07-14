import csv
from collections import Counter


def read():
    with open('./data/6.csv') as f:
        r = csv.reader(f).__next__()
        count = Counter(r)
        data = [0 for _ in range(9)]
        for k, v in count.items():
            data[int(k)] = v
        return data


def first(n: int):
    initial = read()
    for k in range(n):
        print(initial)
        current = initial[1:7] + [initial[0] + initial[7]] + [initial[8]] + [initial[0]]
        initial = current
    print(sum(initial))


def first2(initial: list[int, ...], n: int):
    for k in range(n):
        print(initial)
        current = initial[1:7] + [initial[0] + initial[7]] + [initial[8]] + [initial[0]]
        initial = current
        print(sum(initial))


a = [0, 1, 1, 2, 1, 0, 0, 0, 0]
b = [1, 0, 0, 0, 0, 0, 0, 0, 0]
first2(b, 100)

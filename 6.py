from collections import Counter


def read(loc: str):
    with open(loc) as f:
        r = f.readline().split(',')
        r = list(map(int, r))
        count = Counter(r)
        data = [0 for _ in range(9)]
        for k, v in count.items():
            data[int(k)] = v
        return data


def first(loc: str, n: int):
    initial = read(loc)
    for _ in range(n):
        initial = initial[1:7] + [initial[0] + initial[7]] + [initial[8]] + [initial[0]]
    print(sum(initial))
    return(sum(initial))


def second(loc: str, n: int):
    return first(loc, n)


if __name__ == '__main__':
    first('./data/6.txt', 80)
    second('./data/6.txt', 256)


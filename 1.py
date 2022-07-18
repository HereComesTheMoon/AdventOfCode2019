def read(loc: str) -> list[int]:
    with open(loc) as f:
        r = f.readlines()
        return [int(row) for row in r]

def first(loc: str = "./data/1.csv") -> int:
    vals = read(loc)
    res = sum(vals[k+1] > vals[k] for k in range(len(vals) - 1))
    print(res)
    return res


def second(loc: str = "./data/1.csv") -> int:
    vals = read(loc)
    res = sum(vals[k+3] > vals[k] for k in range(len(vals) - 3))
    print(res)
    return res


first()
second()

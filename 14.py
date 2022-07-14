import csv
from collections import Counter


def read(test: bool = False):
    if test:
        with open('./data/14test.csv') as f:
            r = csv.reader(f, delimiter=' ')
            return "NNCB", {k: v for k, v in r}
    start = "CKFFSCFSCBCKBPBCSPKP"
    with open('./data/14.csv') as f:
        r = csv.reader(f, delimiter=' ')
        return start, {k: v for k, v in r}


def step(start: str, d: dict[str, str]) -> str:
    result = []
    for k in range(1, len(start)):
        a = start[k - 1:k + 1]
        new = d.get(a, "")
        result.append(f"{a[0]}{new}")
    result.append(start[-1])
    return "".join(result)


def step2(start: dict[str, int], d: dict[str, str]) -> dict[str, int]:
    result = {k: 0 for k in start}
    for k, v in start.items():
        a, b = d[k]
        result[a] += v
        result[b] += v
    return result


def tuples_to_elements(d: dict[str, int], start: str):
    # dict with all elements, zero-initialized
    elements = {k[0]: 0 for k in d} | {k[1]: 0 for k in d}
    for k, v in d.items():
        elements[k[0]] += v
        elements[k[1]] += v
    elements[start[0]] += 1
    elements[start[-1]] += 1
    print(elements)
    for k, v in elements.items():
        elements[k] = v //2 # elements[k] always even!
    elements = list(elements.items())
    elements.sort(reverse=True, key=lambda x: x[1])
    return elements


def first(start: str, d: dict[str, str], n: int) -> int:
    for k in range(n):
        print(f"{k} — length: {len(start)}:", start)
        start = step(start, d)
    print(f"{n} — length: {len(start)}:", start)
    cnt = Counter(start)
    print(cnt)
    return cnt.most_common()[0][1] - cnt.most_common()[-1][1]


def second(start: str, d: dict[str, str], n: int) -> int:
    # Format input
    dd = {
        k: (k[0] + v, v + k[1]) for k, v in d.items()
    }
    starts = [start[k - 1:k + 1] for k in range(1, len(start))]
    counts = {}
    for k, v in dd.items():
        counts[k] = 0
        counts[v[0]] = 0
        counts[v[1]] = 0
    for x in starts:
        if x in counts:
            counts[x] += 1
        else:
            counts[x] = 1

    # Iterate process, compute number of tuples after n generations
    for k in range(n):
        print(counts)
        counts = step2(counts, dd)

    # Turn tuples back into elements
    elements = tuples_to_elements(counts, start)
    print(elements)
    return elements[0][1] - elements[-1][1]


# start, d = read()
init, rules = read()

# print(first(start, d, 10))
print(second(init, rules, 40))

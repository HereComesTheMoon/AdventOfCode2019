from collections import Counter


def read(loc: str):
    with open(loc) as f:
        r = f.readlines()
        start = r[0].strip()
        rows = r[2:]
        rows = { row[:2]: row[5:].strip() for row in rows }
    return start, rows


def step(start: str, d: dict[str, str]) -> str:
    """Basically, update the start string to the next string."""
    result = []
    for k in range(1, len(start)):
        a = start[k - 1:k + 1]
        new = d.get(a, "")
        result.append(f"{a[0]}{new}")
    result.append(start[-1])
    return "".join(result)


def step2(start: dict[str, int], d: dict[str, tuple[str, str]]) -> dict[str, int]:
    """Basically, update the start dict to the next dict."""
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
    # print(elements)
    for k, v in elements.items():
        elements[k] = v // 2 # elements[k] always even!
    elements = list(elements.items())
    elements.sort(reverse=True, key=lambda x: x[1])
    return elements


def first(loc: str = "./data/14.csv", n: int = 10) -> int:
    start, d = read(loc)
    for k in range(n):
        print(f"{k} — length: {len(start)}:", start)
        start = step(start, d)
    print(f"{n} — length: {len(start)}:", start)
    cnt = Counter(start)
    print(cnt)
    res = cnt.most_common()[0][1] - cnt.most_common()[-1][1]
    print(res)
    return res


def second(loc: str = "./data/14.csv", n: int = 40) -> int:
    start, d = read(loc)
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
    res = elements[0][1] - elements[-1][1]
    print(res)
    return res


first()
second()


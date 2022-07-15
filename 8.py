def read(loc: str) -> tuple[list, list]:
    """Important: Sort all strings lexicographically. In the input strings, sort the tuples according to the lengths of their elements. In the output data, don't do this, wrong."""
    data_in: list[tuple[str]] = []
    data_out: list[tuple[str]] = []
    with open(loc) as f:
        r = f.readlines()
        for row in r:
            row = row.split()
            assert row[10] == "|"
            a = tuple(sorted(["".join(sorted(x)) for x in row[:10]], key=len))
            b = tuple(["".join(sorted(x)) for x in row[11:]])
            assert len(a) == 10
            assert len(b) == 4
            data_in.append(a)
            data_out.append(b)
    return (data_in, data_out)


def crack(a: tuple[str]) -> tuple[dict[str, str], dict[str, str]]:
    dec: dict[str, str] = dict()
    enc: dict[str, str] = dict()
    aa = tuple(map(set, a))
    assert len(aa[0]) == 2
    assert len(aa[1]) == 3
    assert len(aa[2]) == 4
    assert len(aa[3]) == len(aa[4]) == len(aa[5]) == 5
    assert len(aa[6]) == len(aa[7]) == len(aa[8]) == 6
    assert len(aa[9]) == 7

    # a
    inter: set[str] = aa[1].symmetric_difference(aa[0])
    assert len(inter) == 1
    val = inter.pop()
    dec[val] = 'a'
    enc['a'] = val

    # d 
    inter: set[str] = aa[2] & aa[3] & aa[4] & aa[5] 
    assert len(inter) == 1
    val = inter.pop()
    dec[val] = 'd'
    enc['d'] = val

    # f 
    inter: set[str] = aa[0] & aa[6] & aa[7] & aa[8] 
    assert len(inter) == 1
    val = inter.pop()
    dec[val] = 'f'
    enc['f'] = val

    # c 
    inter: set[str] = aa[0].symmetric_difference({ val })
    assert len(inter) == 1
    val = inter.pop()
    dec[val] = 'c'
    enc['c'] = val

    # g 
    inter: set[str] = aa[3] & aa[4] & aa[5] 
    inter = inter.difference(aa[2], aa[1])
    assert len(inter) == 1
    val = inter.pop()
    dec[val] = 'g'
    enc['g'] = val

    # b 
    inter: set[str] = aa[2].difference({ enc['d'], enc['c'], enc['f'] })
    assert len(inter) == 1
    val = inter.pop()
    dec[val] = 'b'
    enc['b'] = val

    # e 
    inter: set[str] = aa[-1].difference({ x for x in dec })
    assert len(inter) == 1
    val = inter.pop()
    dec[val] = 'e'
    enc['e'] = val

    assert len(dec) == len(enc) == 7
    return enc, dec


def decode(cypher: dict[str, str], vals: tuple[str, str, str, str]) -> int:
    val = 0
    for exp, num in enumerate(vals):
        base = -1
        match len(num):
            case 2:
                base = 1
            case 3:
                base = 7
            case 4:
                base = 4
            case 7:
                base = 8
            case 5:
                if cypher['c'] not in num:
                    base = 5
                elif cypher['f'] in num:
                    base = 3
                else:
                    assert cypher ['e'] in num
                    base = 2
            case 6:
                if cypher['d'] not in num:
                    base = 0
                elif cypher['e'] not in num:
                    base = 9
                else:
                    assert cypher['c'] not in num
                    base = 6
        assert base != -1
        val += base*10**(3-exp)
    return val


def first(loc: str) -> int:
    _, out = read(loc)
    appearances = 0
    for row in out:
        for val in row:
            if len(val) in {2, 3, 4, 7}:
                appearances += 1

    print(appearances)
    return(appearances)


def second(loc: str) -> int:
    a, b = read(loc)

    val = 0
    for aa, bb in zip(a, b):
        enc, _ = crack(aa)
        val += decode(enc, bb)

    print(val)
    return val

first("./data/8.csv")
second("./data/8.csv")


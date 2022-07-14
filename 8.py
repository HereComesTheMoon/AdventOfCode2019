import csv
import random
"""Not solved. You dumbass"""

def readIn():
    with open('./data/8a.csv') as f:
        r = list(csv.reader(f, delimiter=' '))
    # data = []
    # for x in r:
    #     ctr = {
    #         2: [],
    #         3: [],
    #         4: [],
    #         5: [],
    #         6: [],
    #         7: []
    #     }
    #     for y in x:
    #         ctr[len(y)].append(y)
    #     data.append(ctr)
    return r


def readOut():
    with open('./data/8b.csv') as f:
        r = csv.reader(f, delimiter=' ')
        dataOut = list(r)
    return dataOut


def strCont(smol: str, yuge: str):
    for x in smol:
        if x in yuge:
            continue
        else:
            return False
    return True


def whichNumber(row: list[[str, ...]]):
    """Takes a row, and matches each input to its corresponding number."""
    numbers = ["" for _ in range(10)]
    row.sort(key=len)
    numbers[1] = row[0]  # Shortest 7-segment-code is 1
    numbers[7] = row[1]  # second shortest 7-segment-code is 7 etc
    numbers[4] = row[2]
    numbers[8] = row[9]
    # These are the only ones with a unique length
    # It gets weird from here
    # jesus. find the 6 by checking which number doesn't contain the 1
    numbers[6] = next(filter(lambda x: not strCont(numbers[1], x), row[6:9]))
    # 9 only num of length 6 which contains the 4
    numbers[9] = next(filter(lambda x: strCont(numbers[4], x), row[6:9]))
    numbers[0] = [x for x in row[6:9] if x not in [numbers[6], numbers[9]]][0]
    numbers[3] = next(filter(lambda x: strCont(numbers[7], x), row[3:6]))
    temp = [x for x in row[3:6] if x != numbers[3]]
    if len(set(numbers[4]).intersection(temp[0])) == 1:
        numbers[5] = temp[0]
        numbers[2] = temp[1]
    else:
        numbers[5] = temp[1]
        numbers[2] = temp[0]
    assert len(temp) == 2 # Sanity check
    assert len(numbers) == len(set(numbers)) # Unique matches, sanity check
    return numbers


def whichNumber2(row: list[[str, ...]]):
    """Braden's attempt at refactoring whichNumber()"""
    nocontain1 = lambda x: not strCont(numbers[1], x)
    fn_containsrow = lambda idx: lambda row: strCont(numbers[idx], row)
    fn_getrow = lambda x: lambda _: row[x]
    fn_nextfilter = lambda fn, rngs, rnge: lambda _: next(filter(fn, row[rngs:rnge]))
    whateverthehellishappeningfor0 = lambda _: [x for x in row[6:9] if x not in [numbers[6], numbers[9]]][0]
    fn_wthihf52 = lambda t, f: lambda _: temp[t if (len(set(numbers[4]).intersection(temp[0])) == 1) else f]
    nextfilter3 = fn_nextfilter(fn_containsrow(7), 3, 6)
    numbers = ["" for _ in range(10)]

    getters = [
        whateverthehellishappeningfor0,
        fn_getrow(0),
        fn_wthihf52(1, 0),
        nextfilter3,
        fn_getrow(2),
        fn_wthihf52(0, 1),
        fn_nextfilter(nocontain1, 6, 9),
        fn_getrow(1),
        fn_getrow(9),
        fn_nextfilter(fn_containsrow(4), 6, 9)
    ]

    row.sort(key=len)
    temp = [x for x in row[3:6] if x != nextfilter3(None)]
    assert len(temp) == 2 # Sanity check

    for i in range(len(getters)):
        numbers[i] = getters[i](None)

    assert len(numbers) == len(set(numbers)) # Unique matches, sanity check
    return numbers

def primSolver(row: list[str, ...]):
    candidates = {k: {'a', 'b', 'c', 'd', 'e', 'f', 'g'} for k in {'a', 'b', 'c', 'd', 'e', 'f', 'g'}}
    numReal = {
        0: {'a', 'b', 'c', 'e', 'f', 'g'},
        1: {'c', 'f'},
        2: {'a', 'c', 'd', 'e', 'g'},
        3: {'a', 'c', 'd', 'f', 'g'},
        4: {'b', 'c', 'd', 'f'},
        5: {'a', 'b', 'd', 'f', 'g'},
        6: {'a', 'b', 'd', 'e', 'f', 'g'},
        7: {'a', 'c', 'f'},
        8: {'a', 'b', 'c', 'd', 'e', 'f', 'g'},
        9: {'a', 'b', 'c', 'd', 'f', 'g'}
    }
    while any(len(x) > 1 for x in candidates.values()):
        x = y = z = {'a', 'b', 'c', 'd', 'e', 'f', 'g'}
        orderNums = random.shuffle(list(range(10)))
        while min(len(x), len(y), len(z)) > 0:
            pass


def retInter(nums: list):
    candidates = {'a', 'b', 'c', 'd', 'e', 'f', 'g'}
    for x in nums:
        candidates = candidates.intersection(x)
    return candidates


def stupidSolver(nums: list[set, ...]):
    sol = dict()


    a = nums[7].difference(nums[1])
    b = nums[4].difference(nums[3])
    c = nums[1].difference(nums[6])
    d = nums[8].difference(nums[0])
    e = nums[2].difference(nums[3])
    f = nums[1].difference(nums[2])
    g = nums[5].difference(nums[4], nums[7])
    print(f"{g=}")
    sol[a.pop()] = 'a'
    sol[b.pop()] = 'b'
    sol[c.pop()] = 'c'
    sol[d.pop()] = 'd'
    sol[e.pop()] = 'e'
    sol[f.pop()] = 'f'
    sol[g.pop()] = 'g'
    return sol


def first(nums: list[[str, str, str, str], ...]):
    count = 0
    for panel in nums:
        for num in panel:
            if len(num) in {2, 3, 4, 7}:
                count += 1
    return count


def second(nums: list[[str, ...]]):
    count = 0
    for x in nums:
        numbers = whichNumber(x)
        print(numbers)
        a = [{z for z in y} for y in numbers]
        print(a)
        sol = stupidSolver(a)
        print(sol)



print(first(readOut()))
print(second(readIn()))

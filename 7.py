import csv
import functools
from math import inf
from typing import Callable


def read(loc: str) -> list[int]:
    """Returns list of ints, positions of crab subs."""
    with open(loc) as f:
        data = list(map(int, f.readline().split(",")))
        # data = list(map(int, csv.reader(f).__next__()))
    return data


def weightOfCurrentPosSecond(initPos: list[int], targetPos: int) -> int:
    """Returns fuel required for all subs to move to position targetPos. This is part two, with different fuel calculations."""
    temp = map(lambda x: abs(x - targetPos), initPos) # Generator of the distances to the target spot
    return sum([x*(x+1)//2 for x in temp]) # Put the individual fuel requirements in a list (binomial formula), then take sum


def weightOfCurrentPos(initPos: list[int], targetPos: int) -> int:
    """Returns fuel required for all subs to move to position targetPos."""
    return sum(map(lambda x: abs(x - targetPos), initPos))


# Just for fun. Check unimodality. Knowing that a function is unimodal can in principle be used to vastly reduce the computations in
# problems like these, where finding a minimum is required.
# These two functions are not used
def _isUnimodal(func: Callable[[int], int], lower: int, upper: int):
    """Takes a function taking an int, and returning an int, and checks if it is unimodal for integer values a <= k <= b.
    Only enter function that always returns the same values for same inputs, of course. Ideally: Use @functools.cache"""
    while lower < upper and func(lower) == func(lower + 1):
        lower += 1
    if lower == upper:
        return True  # function is constant

    incr = func(lower + 1) - func(lower) > 0  # True iff increasing, false iff decreasing
    while lower < upper and (func(lower) == func(lower + 1) or func(lower + 1) - func(lower > 0 == incr)):
        lower += 1
    if lower == upper:
        return True  # function is (possibly non-strictly) increasing/decreasing

    incr = not incr
    while lower < upper and (func(lower) == func(lower + 1) or func(lower + 1) - func(lower > 0 == incr)):
        lower += 1
    if lower == upper:
        return True  # function is unimodal
    return False


def _isUnimodalList(nums: list[int]):
    """Checks if list is unimodal."""
    finDiff = [nums[k + 1] - nums[k] for k in range(len(nums) - 1)]
    print(finDiff)
    k = -1
    while k < len(finDiff):
        k += 1
        if finDiff[k] == 0:
            continue
        if finDiff[k] > 0:
            while finDiff[k] >= 0:
                k += 1
            return all([x <= 0 for x in finDiff[k:]])
        if finDiff[k] < 0:
            while finDiff[k] <= 0:
                k += 1
            return all([x >= 0 for x in finDiff[k:]])
    if k == len(finDiff):
        return True
    print("This should not happen.")
    return False


def first(loc: str) -> int:
    data = read(loc)
    smallest = weightOfCurrentPos(data, 0) # Arbitrary value which is guaranteed to be high enough
    for k in range(min(data), max(data) + 1):
        smallest = min(smallest, weightOfCurrentPos(data, k))
    print(smallest)
    return smallest


def second(loc: str) -> int:
    data = read(loc)
    smallest = weightOfCurrentPosSecond(data, 0) # Arbitrary value which is guaranteed to be high enough
    for k in range(min(data), max(data) + 1):
        smallest = min(smallest, weightOfCurrentPosSecond(data, k))
    print(smallest)
    return smallest

first('./data/7.csv')
second('./data/7.csv')


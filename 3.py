import csv
import numpy as np


def first():
    with open("./data/3.csv") as f:
        data = [[int(x) for x in row[0]] for row in csv.reader(f)]
    sums = [0] * len(data[0])
    for x in data:
        for k, y in enumerate(x):
            sums[k] += y

    gamma = "".join([str(int(k > len(data) // 2)) for k in sums])
    epsilon = "".join('1' if x == '0' else '0' for x in gamma)

    print(gamma)
    print(epsilon)
    print(int(gamma, 2) * int(epsilon, 2))
    print(len(data))
    print(data)
    print(sums)


def second():
    with open("./data/3.csv") as f:
        data = [[int(x) for x in row[0]] for row in csv.reader(f)]

    nums = data
    for k in range(len(data[0])):
        # filt = filterGood(nums, k, (1, 0))
        # nums = max(filt.values(), key=len)
        nums0, nums1 = filte(nums, k)
        if len(nums0) > len(nums1):
            nums = nums0
        else:
            nums = nums1
    gamma = int("".join(str(x) for x in nums[0]), 2)

    nums = data
    for k in range(len(data[0])):
        if len(nums) == 1:
            break
        nums0, nums1 = filte(nums, k)
        if len(nums0) <= len(nums1):
            nums = nums0
        else:
            nums = nums1
    epsilon = int("".join(str(x) for x in nums[0]), 2)

    print(f"{gamma=}, {epsilon=}, {gamma*epsilon=}")


def filte(nums: [[int, ...]], pos: int, flip: bool = False):
    nums0 = [x for x in nums if x[pos] == 0]
    nums1 = [x for x in nums if x[pos] == 1]

    return nums0, nums1


def filterGood(nums: [[...]], pos: int, sieve: ()):
    results = {
        k: [] for k in sieve
    }
    for x in nums:
        try:
            results[x[pos]].append(x)
        except KeyError:
            pass
    return results


second()

import copy
import random

import numpy as np


def get_matrices():
    R = np.matrix([[1, 0, 0], [0, 0, -1], [0, 1, 0]])
    S = np.matrix([[0, 0, 1], [0, 1, 0], [-1, 0, 0]])
    mtrcs = []
    for i in range(4):
        for j in range(4):
            A = R ** j * S ** i
            mtrcs.append(A)
        A = R ** i * S * R
        mtrcs.append(A)
        A = R ** i * S * R ** 3
        mtrcs.append(A)
    return np.asarray(mtrcs)


def read():
    scanners = []
    with open('./data/19test.csv') as f:
        scanner = []
        while line := f.readline():
            if len(line) <= 3:
                scanners.append(np.asarray(scanner))
                scanner = []
            elif line[0:2] == '--':
                continue
            else:
                a = tuple(map(int, line.rstrip().split(sep=',')))
                scanner.append(a)
        scanners.append(np.asarray(scanner))
    return scanners


def check_matches(beacons_a: np.ndarray, beacons_b: np.ndarray, pos_a: np.ndarray, pos_b: np.ndarray):
    shift = beacons_a[pos_a] - beacons_b[pos_b]
    # shift = pos_a - pos_b
    beacons_shifted = beacons_b + np.full(beacons_b.shape, shift)
    # print(beacons_a)
    tmp = {tuple(x) for x in beacons_a}
    # print(tmp)
    # print({tuple(x) for x in beacons_shifted})
    matches = {tuple(x) for x in beacons_shifted}.intersection(tmp)
    assert len(matches) >= 1
    return matches, tmp.difference(matches)


def find_match(beacon_a: np.ndarray, beacon_b: np.ndarray):
    matrices = get_matrices()
    coordinates = [beacon_b @ t for t in matrices]
    for i, x in enumerate(beacon_a):
        for j, bcn in enumerate(coordinates):
            for k in range(len(bcn)):
                matches, new_beacons = check_matches(beacon_a, bcn, i, k)
                if len(matches) >= 12:
                    return list(new_beacons)
    return []

def try_align(aligned: np.ndarray,  candidate: np.ndarray):
    pass



def first():
    scanners = read()

    total_beacons = copy.deepcopy(scanners[0])
    not_done = scanners[1:]
    previous = total_beacons
    bbb = False

    while not_done:
        random.shuffle(not_done)
        b = not_done[-1]
        results = find_match(total_beacons, b)
        if results:
            total_beacons = np.append(total_beacons, np.asarray(results), axis=0)
            previous = not_done[-1]
            print("Benis")
            if bbb:
                break
            else:
                bbb = True
            not_done.pop()

    return total_beacons


import cProfile, pstats, resource

profiler = cProfile.Profile()
b = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
profiler.enable()
first()
profiler.disable()
stats = pstats.Stats(profiler)
stats.strip_dirs()
stats.sort_stats('cumtime')
stats.print_stats(10)
print(b)
# scanners = read()
# # print(scanners)
# a, b = scanners[:2]
# print(find_match(a, b))


#
# scanners = read()
# # print(scanners)
# a, b = scanners[:2]
# # print(a)
# # print(b)
# i = 9
# j = 0
# print(a[i])
# print(b[j])
# print(check_matches(a, b, i, j))
# for t in matrices:
#     matches = check_matches(a, b @ t, i, j)
#     if len(matches) >= 12:
#         print(len(matches))
#         print(matches)

# for i in range(len(a)):
#     for j in range(len(b)):
#         matches = check_matches(a, b, i, j)
#         if len(matches) >= 12:
#             print(matches)

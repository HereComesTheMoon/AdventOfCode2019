import collections
import copy
import itertools
import math

import numpy as np

POSS = []


class Scanner:
    def __init__(self, points: np.ndarray):
        self.points = points
        self.distances = []

    def calculate_distances(self):
        """Associate to each point a sorted list of its distances to all other points of the scanner. Non-reversible."""
        self.distances = []
        for x in self.points:
            dists = [dist(x, y) for y in self.points]
            dists.sort()
            self.distances.append(dists)

    def cull_overlap(self, other):
        """SELF and OTHER will detect the same distances between all points in the overlap. In other words, for each
        point X in the overlap, there need to be a detected point X1 and X2 in (SELF and OTHER respectively) so that
        X1 and X2's distance lists share at least 12 elements."""
        matches = []
        for i, x in enumerate(self.points):
            for j, y in enumerate(other.points):
                counter = 0  # Since we'll always get one match, each point is dist 0 to itself
                m = 0
                for k in range(len(self.distances[i])):
                    while m < len(other.distances[j]) and self.distances[i][k] > other.distances[j][m]:
                        m += 1
                    if m >= len(other.distances[j]):
                        break
                    if self.distances[i][k] == other.distances[j][m]:
                        counter += 1
                        # print(self.distances[k][i])
                        # print(self.distances[k][i])
                        # print(counter)
                        if counter >= 12:
                            matches.append((i, j))
                            break
        return matches


def dist(x, y):
    return sum((x[i] - y[i]) ** 2 for i in range(len(x)))


def manhattan(x, y):
    return sum((abs(x[i] - y[i]) for i in range(len(x))))


def check_matches(beacons_a: Scanner, beacons_b: Scanner, pos_a: int, pos_b: int):
    shift = beacons_a.points[pos_a] - beacons_b.points[pos_b]
    # shift = pos_a - pos_b
    beacons_shifted = beacons_b.points + np.full(beacons_b.points.shape, shift)
    # print(beacons_a)
    tmp = {tuple(x) for x in beacons_a.points}
    # print(tmp)
    # print({tuple(x) for x in beacons_shifted})
    matches = {tuple(x) for x in beacons_shifted}.intersection(tmp)
    assert len(matches) >= 1
    return matches, tmp.difference(matches)


def get_matrices():
    R = np.matrix([[1, 0, 0], [0, 0, -1], [0, 1, 0]])
    S = np.matrix([[0, 0, 1], [0, 1, 0], [-1, 0, 0]])
    mtrcs = []
    for i in range(4):
        for j in range(4):
            A = R ** j * S ** i
            mtrcs.append(A)
            mtrcs.append(-A)
        A = R ** i * S * R
        mtrcs.append(A)
        mtrcs.append(-A)
        A = R ** i * S * R ** 3
        mtrcs.append(A)
        mtrcs.append(-A)
    return np.asarray(mtrcs)


def read():
    scanner_points = []
    with open('./data/19.csv') as f:
        scanner = []
        while line := f.readline():
            if len(line) <= 3:
                scanner_points.append(np.asarray(scanner))
                scanner = []
            elif line[0:2] == '--':
                continue
            else:
                a = tuple(map(int, line.rstrip().split(sep=',')))
                scanner.append(a)
        scanner_points.append(np.asarray(scanner))
    scanners = []
    for points in scanner_points:
        scanner = Scanner(points)
        scanner.calculate_distances()
        scanners.append(scanner)
    return scanners


def matches(aligned: Scanner, scanner: Scanner, candidates: list):
    rots = get_matrices()
    for i, j in candidates:
        shift = np.full(scanner.points.shape, aligned.points[j] - scanner.points[i])
        # print(shift)
        # assert False
        for t in rots:
            shifted = aligned.points - ((scanner.points @ t))
            print(shifted)
            counter = collections.Counter((tuple(x) for x in shifted))
            print(counter)
            if counter.most_common()[0][1] >= 10:
                assert False

            # counter = 0
            # for point in shifted:
            #     if point[0] == 0 and point[1] == 0 and point[2] == 0:
            #         counter += 1
            # if counter >= 11:
            #     print(shifted)
            #     assert False


def match(aligned: Scanner, scanner: Scanner, candidates: list):
    rots = get_matrices()
    al_pts = {tuple(x) for x in aligned.points}
    for i, j in candidates:
        for t in rots:
            tilt = scanner.points @ t
            shift = np.full(scanner.points.shape, aligned.points[i] - tilt[j])
            shifted = tilt + shift
            sc_pts = {tuple(x) for x in shifted}
            leen = len(sc_pts.intersection(al_pts))
            if leen >= 12:
                POSS.append(aligned.points[i] - scanner.points[j] @ t)
                new_scanner = Scanner(shifted)
                new_scanner.calculate_distances()
                scanner.points = shifted
                return True
    return False


def main():
    scanners = read()
    done = [scanners[0]]
    scanners = scanners[1:]
    # scanners.reverse()

    while scanners:
        scanner = scanners.pop(0)
        temp_done = copy.deepcopy(done)
        bll = True
        for aligned in temp_done:
            assert scanner != aligned
            print("Searching!", scanner, aligned.points[0])
            print(done)
            candidates = aligned.cull_overlap(scanner)
            print(candidates)
            scn = match(aligned, scanner, candidates)
            if scn:
                print("Nice!")
                print(aligned.points)
                done.append(scanner)
                print(scanners)
                bll = False
                break
        if bll:
            scanners.append(scanner)
    pts = set()
    for x in done:
        for y in x.points:
            pts.add(tuple(y))
    print(pts)

    print(len(pts))
    print(POSS)
    return max(manhattan(x, y) for x, y in itertools.product(POSS, POSS))


print(main())

#
# scanners = read()
# print(len(scanners))
#
# first = scanners[0]
# second = scanners[1]
# print(first.distances[0])
# print(second.distances[0])
# print(first.cull_overlap(scanners[1]))

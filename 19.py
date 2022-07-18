from typing import Union, Iterable
import itertools
from collections import deque

import numpy as np


class Scanner:
    def __init__(self, points: np.ndarray[int, np.dtype], scanner_position: np.ndarray[int, np.dtype] = np.zeros(3)):
        self.points: np.ndarray[int, np.dtype] = points
        self.distances: list[list[int]] = self.calculate_distances(self.points)
        self.scanner_position = scanner_position

    def calculate_distances(self, points: np.ndarray[int, np.dtype]) -> list[list[int]]:
        """Associate to each point a sorted list of its distances to all other points of the scanner. Non-reversible."""
        distances = []
        for x in points:
            dists = [dist(x, y) for y in points]
            dists.sort()
            distances.append(dists)
        return distances

    def cull_overlap(self, other: "Scanner") -> tuple[tuple[int, int],...]:
        """SELF and OTHER will detect the same distances between all points in the overlap. In other words, for each
        point X in the overlap, there need to be a detected point X1 and X2 in (SELF and OTHER respectively) so that
        X1 and X2's distance lists share at least 12 elements."""
        matches: list[tuple[int, int]] = []
        for i, _ in enumerate(self.points):
            for j, _ in enumerate(other.points):
                counter = 0
                m = 0
                for k in range(len(self.distances[i])):
                    while m < len(other.distances[j]) and self.distances[i][k] > other.distances[j][m]:
                        m += 1
                    if m >= len(other.distances[j]):
                        break
                    if self.distances[i][k] == other.distances[j][m]:
                        counter += 1
                        if counter >= 12:
                            matches.append((i, j))
                            break
        return tuple(matches)


class Scanner_Data:
    def __init__(self, loc: str) -> None:
        self.raw_scanners: tuple[Scanner] = tuple(self.read(loc))
        self.rots = self.get_matrices()
        self.aligned_scanners: list[Scanner] = self.build_map(self.raw_scanners)


    def read(self, loc: str) -> list[Scanner]:
        """Only call once, at initialisation."""
        scanner_points = []
        with open(loc) as f:
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
            scanners.append(scanner)
        return scanners


    def get_matrices(self) -> np.ndarray[np.matrix, np.dtype]:
        """Only call once, at initialisation. This is a complete set of representatives of those 3d-rotation matrices, which either turn by 90 degrees. No reflections. There are 24 = 4*6 of these rotations."""
        R = np.matrix(np.asarray([[1, 0, 0], [0, 0, -1], [0, 1, 0]]))
        S = np.matrix(np.asarray([[0, 0, 1], [0, 1, 0], [-1, 0, 0]]))
        mtrcs = []
        for i in range(4):
            for j in range(4):
                A = R ** j * S ** i
                mtrcs.append(A)
            A = R ** i * S * R
            mtrcs.append(A)
            A = R ** i * S * R ** 3
            mtrcs.append(A)

        assert len(mtrcs) == 24
        # No duplicates
        for k, A in enumerate(mtrcs):
            for B in mtrcs[k+1:]:
                # print((A - B))
                assert np.any(A - B)

        return np.asarray(mtrcs)


    def match(self, aligned: Scanner, scanner: Scanner, candidates: tuple[tuple[int, int],...]) -> Union[Scanner, None]:
        """Given an aligned, and a not-yet-aligned scanner, and a few promising beacons, try to align their respective maps by transforming the coordinate systems, and seeing if they match up at at least 12 points."""
        aligned_points = {tuple(x) for x in aligned.points}
        for i, j in candidates:
            for t in self.rots:
                tilt = scanner.points @ t
                shift = np.full(scanner.points.shape, aligned.points[i] - tilt[j])
                shifted = tilt + shift
                scanner_points = {tuple(x) for x in shifted}
                if len(scanner_points.intersection(aligned_points)) >= 12:
                    scanner_aligned_position: np.ndarray[int, np.dtype] = aligned.points[i] - scanner.points[j] @ t
                    new_aligned_scanner = Scanner(shifted, scanner_aligned_position)
                    return new_aligned_scanner
        return None


    def build_map(self, to_be_aligned: Iterable[Scanner]) -> list[Scanner]:
        """Uses to_be_aligned to create a new list of scanners, which are all in the same coordinate system."""
        to_be_aligned = deque(to_be_aligned) # Queue of scanners that need to be aligned
        done = [to_be_aligned.popleft()] # List of scanners that have been aligned

        while to_be_aligned:
            now_aligning = to_be_aligned.popleft()
            try_again = True
            for aligned in done:
                assert now_aligning != aligned
                candidates = aligned.cull_overlap(now_aligning)
                new_aligned_scanner = self.match(aligned, now_aligning, candidates)
                if new_aligned_scanner is not None:
                    done.append(new_aligned_scanner)
                    try_again = False
                    break

            if try_again:
                to_be_aligned.append(now_aligning)

        return done


def dist(x: np.ndarray[int, np.dtype], y: np.ndarray[int, np.dtype]) -> int:
    """Euclidean distance"""
    return sum((x[i] - y[i]) ** 2 for i in range(len(x)))


def manhattan(x: np.ndarray[int, np.dtype], y: np.ndarray[int, np.dtype]) -> int:
    """L1 distance."""
    return sum((abs(x[i] - y[i]) for i in range(len(x))))


def first() -> int:
    data = Scanner_Data("./data/19.csv")
    beacons = set()
    for x in data.aligned_scanners:
        for y in x.points:
            beacons.add(tuple(y))

    res = len(beacons)
    print(res)
    return res


def second() -> int:
    data = Scanner_Data("./data/19.csv")

    scanner_positions = [scanner.scanner_position for scanner in data.aligned_scanners]
    res = max(manhattan(x, y) for x, y in itertools.product(scanner_positions, scanner_positions))
    print(res)
    return res



second()


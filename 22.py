from typing import NamedTuple, Final
from itertools import chain

Pt = NamedTuple('Pt', [('x', int), ('y', int), ('z', int)])


# Two ways of approaching this problem:
# 1. Chop each cube into several (up 26) smaller ones as intersections happen
# 2. As intersections happen, add a cube with the volume of the intersection. Its volume is signed, and compensates for the "double counting" the intersection
# This problem was quite difficult, since I opted for the first approach at first, which is vastly fiddlier.


class Cube:
    def __init__(self, on: bool, small: Pt, large: Pt):
        self.on: Final[bool] = on
        self.small: Pt = small
        self.large: Pt = large

        assert self.small.x <= self.large.x
        assert self.small.y <= self.large.y
        assert self.small.z <= self.large.z


    def volume(self) -> int:
        vol = (1 + self.large[2] - self.small[2]) * (1 + self.large[1] - self.small[1]) * (1 + self.large[0] - self.small[0])
        if self.on:
            return vol
        else:
            return -vol


    def __repr__(self):
        return f"Cube: {self.small}, {self.large}, with volume: {self.volume()}"


    def intersects(self, cube: "Cube") -> bool:
        for k in range(3):
            if self.small[k] > cube.large[k] or self.large[k] < cube.small[k]:
                return False
        return True


    def get_intersection(self, b: "Cube", on: bool) -> "Cube":
        small = (max(aa, bb) for aa, bb in zip(self.small, b.small))
        big = (min(aa, bb) for aa, bb in zip(self.large, b.large))
        return Cube(on, Pt(*small), Pt(*big))


def read(loc: str) -> list[Cube]:
    state_key = {
            'on': True,
            'off': False,
            }

    def parse_range(string: str) -> tuple[int, int]:
        a, b = string[2:].split("..")
        return int(a), int(b)

    with open(loc) as f:
        r = list(f.readlines())
        states = [state_key[row.split(" ")[0]] for row in r]
        corners = [row.split(" ")[1].split(",") for row in r]
        cubes = []
        for state, row in zip(states, corners):
            x0, x1 = parse_range(row[0])
            y0, y1 = parse_range(row[1])
            z0, z1 = parse_range(row[2])
            cubes.append(Cube(state, Pt(x0, y0, z0), Pt(x1, y1, z1)))

        cubes.reverse() # This is necessary, the cubes are turned on/off in order.
        return cubes


def solve(cubes: list[Cube]) -> int:
    added_cubes: list[Cube] = []
    while cubes:
        temp_cubes: list[Cube] = []
        nxt: Cube = cubes.pop()

        # For each new cube, intersect with every added cube, and save their intersections as new cubes
        for cube in added_cubes:
            if cube.intersects(nxt):
                temp_cubes.append(cube.get_intersection(nxt, not cube.on))

        added_cubes.extend(temp_cubes)

        if nxt.on:
            added_cubes.append(nxt)

    # Compute volume:
    vol = sum(cube.volume() for cube in added_cubes)

    return vol


def first(loc: str = './data/22.csv') -> int:
    cubes = read(loc)

    filt = lambda cube: all(p in range(-50, 51) for p in chain(cube.small, cube.large))
    vol = solve(list(filter(filt, cubes)))

    print(vol)
    assert vol == 577205
    return vol


def second(loc: str = './data/22.csv') -> int:
    cubes: list[Cube] = read(loc) # Reversed, treat as stack and pop
    vol = solve(cubes)

    print(vol)
    assert vol == 1197308251666843
    return vol


first()
second()

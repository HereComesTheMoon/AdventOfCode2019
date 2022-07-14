import csv
import itertools
from collections import namedtuple
import numpy as np

Pt = namedtuple('Pt', 'x, y, z')


def hamming(a: str, b: str) -> int:
    assert len(a) == len(b)
    return len([a[k] == b[k] for k in range(len(a))])

edges = [
    ('000', '001'),
    ('000', '010'),
    ('000', '100'),
    ('100', '110'),
    ('100', '101'),
    ('010', '110'),
    ('010', '011'),
    ('001', '011'),
    ('001', '101'),
    ('110', '111'),
    ('011', '111'),
    ('101', '111')
]

faces = [
    ('000', '011', '010', '001'),
    ('000', '101', '100', '001'),
    ('000', '110', '100', '010'),
    ('111', '001', '011', '101'),
    ('111', '100', '101', '110'),
    ('111', '010', '011', '011'),
]
# faces = [
#     ('000', '011'),
#     ('000', '101'),
#     ('000', '110'),
#     ('111', '001'),
#     ('111', '100'),
#     ('111', '010'),
# ]

class Cube:
    def __init__(self, on: bool, vertices: list[tuple[int,int,int],...]):
        self.on = on
        self.small = Pt(min(x[0] for x in vertices), min(x[1] for x in vertices), min(x[2] for x in vertices))
        self.big = Pt(max(x[0] for x in vertices), max(x[1] for x in vertices), max(x[2] for x in vertices))
        # self.small = Pt(small[1], small[1], small[2])  # 000
        # self.big = Pt(*big)  # 111
        self.vertices = {
            '000': tuple(self.small),
            '100': (self.big.x, self.small.y, self.small.z),
            '010': (self.small.x, self.big.y, self.small.z),
            '001': (self.small.x, self.small.y, self.big.z),
            '110': (self.big.x, self.big.y, self.small.z),
            '011': (self.small.x, self.big.y, self.big.z),
            '101': (self.big.x, self.small.y, self.big.z),
            '111': tuple(self.big)
        }
        # self.edges = {
        #     {d1, d2 if hamming(d1, d2) <= 1} for d1, d2 in itertools.product(self.vertices, 2)
        # }

    def volume(self):
        vol = (1 + self.big[2] - self.small[2]) * (1 + self.big[1] - self.small[1]) * (1 + self.big[0] - self.small[0])
        if self.on:
            return vol
        else:
            return -vol

    def __repr__(self):
        return f"Cube: {self.small}, {self.big}, with volume: {self.volume()}"


    def __contains__(self, item):
        x, y, z = item  # tuple unpacking, idk
        sm = self.small
        bg = self.big
        if sm.x <= x <= bg.x and sm.y <= y <= bg.y and sm.z <= z <= bg.z:
            return True
        return False

    def intersects(self, cube: "Cube"):
        for k in range(3):
            if self.small[k] > cube.big[k] or self.big[k] < cube.small[k]:
                return False
        return True

    def chop(self, victim: "Cube") -> list["Cube",...]:
        # Victim is the cube that gets chopped, so in my diagram the bigger cube.
        distx = {
            '0': min(victim.small.x - self.small.x, 0),
            '1': max(victim.big.x - self.big.x, 0)
        }
        disty = {
            '0': min(victim.small.y - self.small.y, 0),
            '1': max(victim.big.y - self.big.y, 0)
        }
        distz = {
            '0': min(victim.small.z - self.small.z, 0),
            '1': max(victim.big.z - self.big.z, 0)
        }
        chopped = []
        for vertex, coordinates in self.vertices.items():
            vtx = Pt(distx[vertex[0]], disty[vertex[1]], distz[vertex[2]])
            if vtx.x and vtx.y and vtx.z:
                new_cube = Cube(victim.on, [coordinates, (distx[vertex[0]], disty[vertex[1]], distz[vertex[2]])])
                print(new_cube)
                chopped.append(new_cube)

        for tail, head in edges:
            vtx_head = Pt(distx[head[0]], disty[head[1]], distz[head[2]])
            vtx_tail = Pt(distx[tail[0]], disty[tail[1]], distz[tail[2]])
            if vtx_head.x and vtx_head.y and vtx_head.z and vtx_tail.x and vtx_tail.y and vtx_tail.z:
                new_cube = Cube(victim.on, [self.vertices[tail], self.vertices[head], vtx_head, vtx_tail])
                chopped.append(new_cube)

        for face in faces:
            fece = [Pt(distx[a], disty[b], distz[c]) for a, b, c in face]


        return chopped


class Region:
    def __init__(self, small: tuple[int, int, int], big: tuple[int, int, int]):
        self.small = Pt(*small)
        self.big = Pt(*big)
        self.shape = (self.big.x - self.small.x + 1, self.big.y - self.small.y + 1, self.big.z - self.small.z + 1)
        self.arr: np.ndarray = np.zeros(self.shape, dtype=bool)

    def flip(self, cube: Cube):
        if self.intersects(cube):
            # cube_small_shifted = Pt(*[cube.small[k]])
            axis_x = range(max(0, cube.small.x - self.small.x),
                           min(cube.big.x - self.small.x + 1, self.big.x - self.small.x + 1))
            axis_y = range(max(0, cube.small.y - self.small.y),
                           min(cube.big.y - self.small.y + 1, self.big.y - self.small.y + 1))
            axis_z = range(max(0, cube.small.z - self.small.z),
                           min(cube.big.z - self.small.z + 1, self.big.z - self.small.z + 1))
            for x, y, z in itertools.product(axis_x, axis_y, axis_z):
                # print(x,y,z)
                self.arr[x, y, z] = cube.on

    def intersects(self, cube: Cube):
        for k in range(3):
            if self.small[k] > cube.big[k] or self.big[k] < cube.small[k]:
                return False
        return True


def read():
    with open('./data/22.csv') as f:
        re = [list(map(int, x)) for x in csv.reader(f)]
        cubes = [Cube(bool(r[0]), [(r[1], r[3], r[5]), (r[2], r[4], r[6])]) for r in re]
        cubes.reverse()
        return cubes


#
# a = Cube(True, (10, 10, 10), (12, 12, 12))
#
# print(a)
# print(a.small)
# print(a.big)
#
# print((10,12,12) in a)
#
# init_proc_region = Region((-50, -50, -50), (50, 50, 50))
#
# print(init_proc_region.small)
# print(init_proc_region.big)
# print(init_proc_region.shape)
# print(init_proc_region.arr)
# print(init_proc_region.arr.shape)
#
# init_proc_region.flip(a)
#
# print(read())

#
# def first():
#     reg = Region((-50, -50, -50), (50, 50, 50))
#     cubes = read()
#     for cube in cubes:
#         reg.flip(cube)
#     print(np.count_nonzero(reg.arr))


def intersect(a: Cube, b: Cube) -> tuple:
    small = tuple((max(aa, bb) for aa, bb in zip(a.small, b.small)))
    big = tuple((min(aa, bb) for aa, bb in zip(a.big, b.big)))
    return (small, big)

def second():
    cubes = read() # Reversed, treat as stack and pop
    added_cubes = []
    while cubes:
        temp_cubes = []
        nxt = cubes.pop()
        for cube in added_cubes:
            if cube.intersects(nxt):
                s, b = intersect(cube, nxt)
                if cube.on:
                    new_cube = Cube(False, [s, b])
                    temp_cubes.append(new_cube)
                else:
                    new_cube = Cube(True, [s, b])
                    temp_cubes.append(new_cube)
        added_cubes.extend(temp_cubes)
        if nxt.on:
            added_cubes.append(nxt)

    # Compute volume:
    vol = 0
    for cube in added_cubes:
        vol += cube.volume()

    return vol






import cProfile, pstats
profiler = cProfile.Profile()
profiler.enable()
print(second())
profiler.disable()
stats = pstats.Stats(profiler)
stats.strip_dirs()
stats.sort_stats('cumtime')
stats.print_stats(20)


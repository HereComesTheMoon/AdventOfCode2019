import cProfile
import functools
import pstats
import resource
import time

starting_pos1 = 4
starting_pos2 = 7

DIRAC_DIE = [(3, 1), (4, 3), (5, 6), (6, 7), (7, 6), (8, 3), (9, 1)]


def det_dice():
    while True:
        for k in range(1,101):
            yield k



def first():
    cp1 = starting_pos1
    cp2 = starting_pos2
    points1, points2 = 0, 0
    rolls = 0
    dice = det_dice()

    while True:
        a, b, c = dice.__next__(),dice.__next__(), dice.__next__()
        cp1 = (cp1 + a + b + c) % 10
        if cp1 == 0:
            cp1 = 10
        points1 += cp1
        rolls += 3
        if points1 >= 1000:
            return points2 * rolls

        a, b, c = dice.__next__(),dice.__next__(), dice.__next__()
        cp2 = (cp2 + a + b + c) % 10
        if cp2 == 0:
            cp2 = 10
        points2 += cp2
        rolls += 3
        if points2 >= 1000:
            return points1 * rolls

# All sums of 3d3.
# dirac_die = [4] + [5]*3 + [6]*6 + [7]*7 + [8]*6 + [9]*3 + [10]


@functools.cache
def dirac(pos1: int, pos2: int, pts1: int, pts2: int, player1s_turn: bool):
    if player1s_turn:
        pos1 = pos1 % 10
        if pos1 == 0:
            pos1 = 10
        pts1 += pos1
        if pts1 >= 21:
            return 1, 0
        else:
            wins1, wins2 = 0, 0
            for roll, occurrences in DIRAC_DIE:
                a, b = dirac(pos1, pos2 + roll, pts1, pts2, False)
                wins1 += a*occurrences
                wins2 += b*occurrences
            return wins1, wins2
    else:
        pos2 = pos2 % 10
        if pos2 == 0:
            pos2 = 10
        pts2 += pos2
        if pts2 >= 21:
            return 0, 1
        else:
            wins1, wins2 = 0, 0
            for roll, occurrences in DIRAC_DIE:
                a, b = dirac(pos1 + roll, pos2, pts1, pts2, True)
                wins1 += a*occurrences
                wins2 += b*occurrences
            return wins1, wins2


def dirac_first_turn(pos1: int, pos2: int, pts1: int, pts2: int):
    wins1, wins2 = 0, 0
    for roll, occurrences in DIRAC_DIE:
        a, b = dirac(pos1 + roll, pos2, pts1, pts2, True)
        wins1 += a * occurrences
        wins2 += b * occurrences
    return wins1, wins2


CACHE = {}


def dirac_cache(pos1: int, pos2: int, pts1: int, pts2: int, player1s_turn: bool):
    # if (pos1, pos2, pts1, pts2, player1s_turn) in CACHE:
    if v := CACHE.get((pos1, pos2, pts1, pts2, player1s_turn)):
        return v
    if player1s_turn:
        pos1 = pos1 % 10
        if pos1 == 0:
            pos1 = 10
        pts1 += pos1
        if pts1 >= 21:
            return 1, 0
        else:
            # dirac_die = [4] + [5]*3 + [6]*6 + [7]*7 + [8]*6 + [9]*3 + [10]
            # (Resulting Sum , Number of occurrences)
            wins1, wins2 = 0, 0
            for roll, occurrences in DIRAC_DIE:
                a, b = dirac_cache(pos1, pos2 + roll, pts1, pts2, False)
                CACHE[(pos1, pos2 + roll, pts1, pts2, False)] = a, b
                wins1 += a*occurrences
                wins2 += b*occurrences
            return wins1, wins2
    else:
        pos2 = pos2 % 10
        if pos2 == 0:
            pos2 = 10
        pts2 += pos2
        if pts2 >= 21:
            return 0, 1
        else:
            # dirac_die = [4] + [5]*3 + [6]*6 + [7]*7 + [8]*6 + [9]*3 + [10]
            # (Resulting Sum , Number of occurrences)
            wins1, wins2 = 0, 0
            for roll, occurrences in DIRAC_DIE:
                a, b = dirac_cache(pos1 + roll, pos2, pts1, pts2, True)
                CACHE[(pos1 + roll, pos2, pts1, pts2, True)] = a, b
                wins1 += a*occurrences
                wins2 += b*occurrences
            return wins1, wins2


def dirac_first_turn_cache(pos1: int, pos2: int, pts1: int, pts2: int):
    wins1, wins2 = 0, 0
    for roll, occurrences in DIRAC_DIE:
        a, b = dirac_cache(pos1 + roll, pos2, pts1, pts2, True)
        CACHE[(pos1 + roll, pos2, pts1, pts2, True)] = a, b
        wins1 += a * occurrences
        wins2 += b * occurrences
    return wins1, wins2



profiler = cProfile.Profile()
b = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
profiler.enable()
print(dirac_first_turn(starting_pos1, starting_pos2, 0, 0))
profiler.disable()
stats = pstats.Stats(profiler)
stats.strip_dirs()
stats.sort_stats('cumtime')
stats.print_stats(10)
#
# start_time = time.time()
# print("--- %s seconds ---" % (time.time() - start_time))
#
# start_time = time.time()
# print(dirac_first_turn_cache(starting_pos1, starting_pos2, 0, 0))
# print("--- %s seconds ---" % (time.time() - start_time))
import functools
from typing import Generator

starting_pos1 = 4
starting_pos2 = 7

# All sums of 3d3.
# dirac_die = [4] + [5]*3 + [6]*6 + [7]*7 + [8]*6 + [9]*3 + [10]
# This is essentially a discrete probability distribution.
# (SUM_OF_DICE, NUMBER_OF_DICE_ROLL_OUTCOMES_WITH_THIS_SUM)
DIRAC_DIE: tuple[tuple[int, int],...] = ((3, 1), (4, 3), (5, 6), (6, 7), (7, 6), (8, 3), (9, 1))


def det_dice() -> Generator[int, None, None]:
    while True:
        for k in range(1,101):
            yield k


@functools.cache
def dirac(pos1: int, pos2: int, pts1: int, pts2: int, player1s_turn: bool) -> tuple[int, int]:
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


def first(pos1: int, pos2: int) -> int:
    points1, points2 = 0, 0
    rolls = 0
    dice = det_dice()

    while True:
        a, b, c = dice.__next__(),dice.__next__(), dice.__next__()
        pos1 = (pos1 + a + b + c) % 10
        if pos1 == 0:
            pos1 = 10
        points1 += pos1
        rolls += 3
        if points1 >= 1000:
            res =  points2 * rolls
            break

        a, b, c = dice.__next__(),dice.__next__(), dice.__next__()
        pos2 = (pos2 + a + b + c) % 10
        if pos2 == 0:
            pos2 = 10
        points2 += pos2
        rolls += 3
        if points2 >= 1000:
            res = points1 * rolls
            break
    
    print(res)
    return res


def second(pos1: int, pos2: int) -> int:
    wins1, wins2 = 0, 0
    for roll, occurrences in DIRAC_DIE:
        a, b = dirac(pos1 + roll, pos2, 0, 0, True)
        wins1 += a * occurrences
        wins2 += b * occurrences
    res = max(wins1, wins2)
    print(res)
    return res


if __name__ == '__main__':
    first(4, 7)
    second(4, 7)

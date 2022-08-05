import math
from typing import NamedTuple

target = NamedTuple('Target', [('x_min', int), ('x_max', int), ('y_min', int), ('y_max', int)])

t: tuple[int, int, int, int] = target(0,1,2,3)


# This was way more work than it should have been. Trying to be clever was a bad idea. This here was severely cleaned up, and it is still not pretty.


def read(loc: str) -> target:
    with open(loc) as f:
        r = f.readline()[15:-1]
        x_part, y_part = r.split(", y=")
        x_min, x_max = map(int, x_part.split(".."))
        y_min, y_max = map(int, y_part.split(".."))
        t: target = target(x_min, x_max, y_min, y_max)
        return t


def peak_y(dy: int):
    if dy <= 0:
        return 0
    return dy * (dy + 1) // 2


def x_after_k_steps(dx:  int, steps: int):
    assert dx >= 0
    if dx == 0:
        return 0
    # sign = 1 if dx > 0 else -1
    if steps >= dx:
        return dx * (dx + 1) // 2
    else:
        return dx * (dx + 1) // 2 - (dx - steps) * (dx - steps + 1) // 2


def upd_vel(dx: int, dy: int):
    return min(abs(dx-1), abs(dx+1), abs(dx)), dy-1


def is_sol(t: target, dx: int, dy: int) -> bool:
    pos_x, pos_y = 0, 0
    while pos_y > t.y_min and pos_x <= t.x_max:
        pos_x += dx
        pos_y += dy
        dx, dy = upd_vel(dx, dy)
        if dx == 0 and pos_x < t.x_min:
            return False
        if t.x_min <= pos_x <= t.x_max and t.y_min <= pos_y <= t.y_max:
            return True
    return False


def find_all_solutions(t: target) -> list[tuple[int,int]]:
    solutions = []

    # These bounds for x and y are tight
    for y in range(t.y_min, -t.y_min):
        for x in range(math.isqrt(2 * t.x_min), t.x_max + 1):
            if is_sol(t, x, y):
                solutions.append((x,y))

    return solutions


def first(t: target) -> int:
    """This is overly convoluted, and unnecessary. Keeping it here for authenticity. To explain why this works. Starting values are (x,y), where y > 0. We also assume that y_max is negative. After y steps the probe (following a parabolic arc) will have reached its peak, after 2y steps it will be at height 0, with a downwards velocity of -y. At the next step it will be at y-position -y, which has to be contained in our target area. In other words, y = abs(y_min) - 1 is the best possible starting y-velocity which we can achieve. We now need to check whether we can find an x, such that x_after_k_steps is within the target bounds for x after exactly 2y+1 steps. If this is possible at all, then we are done. This is the case for my example. This task does not specify much about the type of area. Changing or moving the area drastically changes how this problem has to be approached.

    Our assumptions: y_max < 0. It is possible to find a solution such that the probe is in the area after exactly 2y+1 steps.

    Side note: A higher value of y is impossible, it will always overshoot."""
    for y in range(abs(t.y_min) - 1, abs(t.y_max) - 1, -1):
        for x in range(math.isqrt(2*t.x_min), math.isqrt(2*t.x_max)): # Approximations. Culls unnecessary cases
            if t.x_min <= x_after_k_steps(x, 2*y+1) <= t.x_max:
                return peak_y(y)

    assert False


def first2(t: target) -> int:
    sols = find_all_solutions(t)
    maxi = 0
    for _, y in sols:
        maxi = max(maxi, peak_y(y))

    print(maxi)
    return maxi


def second(t: target) -> int:
    sols = find_all_solutions(t)
    res = len(sols)
    print(res)
    return res




if __name__ == '__main__':
    t = read("./data/17.txt")
    first2(t)
    second(t)


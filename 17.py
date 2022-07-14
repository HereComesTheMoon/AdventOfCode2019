import math

X_MIN = 124
X_MAX = 174
Y_MIN = -123
Y_MAX = -86
#
# X_MIN = 20
# X_MAX = 30
# Y_MIN = -10
# Y_MAX = -5

# Important/obvious:
# Init velocity (x, y), at starting position (0, 0)
# Assuming y > 0 : The probe will be at height 0 after 2y steps
# After 2Y steps the probe will be exactly on height 0.
# This leaves two questions:
# 1. What's the biggest downwards trajectory at 0 so that we're still in the target?
# 2. For which value of X are we going to hit the target?

def upd_vel(dx: int, dy: int):
    # Technically dx always positive in part 1, so this could be optimised.
    if dx == 0:
        return 0, dy-1
    return min(abs(dx-1), abs(dx+1)), dy-1


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

def trajectory(x: int, y: int):
    pos_x, pos_y = x, y
    k = 1
    while pos_y > Y_MIN - 2*abs(Y_MIN - Y_MAX):
        x, y = upd_vel(x, y)
        print(f"Step: {k}. Position: ({pos_x}, {pos_y}) Target: {X_MIN <= pos_x <= X_MAX and Y_MIN <= pos_y <= Y_MAX}. Trajectory: ({x}, {y})")
        pos_x += x
        pos_y += y
        k += 1

    print(f"Step: {k}. Position: ({pos_x}, {pos_y}). Trajectory: ({x}, {y})")


def x_min_steps(x: int):
    # for x in range(math.isqrt(2 * x_min), math.isqrt(2 * x_max)):  # Approximations. Culls unnecessary cases
    pos = 0
    dx = x
    for k in range(1, x+1):
        pos += dx
        dx = max(dx - 1, 0)
        if pos < X_MIN:
            continue
        if X_MAX < pos:
            return None
        else:
            return k

def y_range(y: int):
    k = 0
    dy = y
    pos = 0
    if y > 0:
        k = 2*y +1
        dy = - y - 1

    while pos > Y_MAX:
        print(f"{pos=}")
        pos += dy
        dy -= 1
        k += 1

    k_min = k
    print(f"{k_min=}")

    while pos >= Y_MIN:
        print(f"{pos=}")
        pos += dy
        dy -= 1
        k += 1

    k_max = k

    return range(k_min, k_max+1)


def x_vals(x_min: int, x_max: int):
    # math.isqrt(2*x_max) + 1 approximation, always picks a starting value high enough that probe overshoots
    # idea: Lower x and compute all possible x values, and their respective step ranges
    for x in range(math.isqrt(2*x_max)+1, 0, -1):
        for k in range(x, 0, -1):
            if x_min <= x_after_k_steps(x, k) <= x_max:
                pass




def first(x_min: int, x_max: int, y_min: int, y_max: int):
    """I am super tired today, so this is really bad. But hey, it works."""
    y = abs(y_min) -1
    while True:
        for x in range(math.isqrt(2*x_min), math.isqrt(2*x_max)): # Approximations. Culls unnecessary cases
            if x_min <= x_after_k_steps(x, 2*y+1) <= x_max:
                return x, y
        y += 1


def second():
    """I am super tired today, so this is really bad. But hey, it works."""
    solutions = []
    for y in range(Y_MIN, -Y_MIN):
        for y_now in y_range(y):
            for x in range(math.isqrt(2 * X_MIN)-6, math.isqrt(2 * X_MAX)+200):
                if X_MIN <= x_after_k_steps(x, y_now) <= X_MAX:
                    solutions.append((x, y_now))
    return solutions

def second2():
    solutions = []
    for y in range(Y_MIN, -Y_MIN):
        for x in range(X_MAX+1):
            if is_sol(x, y):
                solutions.append((x,y))

    return solutions


def is_sol(dx: int, dy: int):
    pos_x, pos_y = 0, 0
    while pos_y > Y_MIN:
        pos_x += dx
        pos_y += dy
        dx, dy = upd_vel(dx, dy)
        if X_MIN <= pos_x <= X_MAX and Y_MIN <= pos_y <= Y_MAX:
            return True
    return False



#
# x, y = first(X_MIN, X_MAX, Y_MIN, Y_MAX)
#
# print(peak_y(y))
#
# trajectory(x, y)
#
#
#
# test = [(7,2), (6,3), (9,0 ), (17, -4)]
# for x, y in test:
#     print(list(y_range(y)))
#     trajectory(x, y)

sec = second2()
print(len(sec))

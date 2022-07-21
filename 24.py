from math import trunc
from typing import Generator


# By close inspection of the input file, we see that there are 14 chunks, each with the same structure across 17 lines.
# These chunks are separate by an input command.
# The chunks are exactly the same, except at three locations, where different integer literals are given
# This means that we can interpret each chunk as a function f() with three parameters (p0, p1, p2).
# This function f acts on the existing variables (w,x,y,z).
# By closer inspection we see that x and y can be eliminated completely.
# w exists purely to read in input data.
# z is the variable storing the internal state of the machine. 
# We extract a list of parameters (p0, p1, p2): list[tuple[int, int, int]], and have a starting value of z = 0.
# Now f can be interpreted as acting on (ie. modifying) z based on its parameters, and a single int value w which we provide as an argument.
# Each chunk is either of type p0 == 1, or of type p0 == 26, and there's an equal number of chunks of each type.
# If p0 == 1: f(z) is going to grow slightly bigger, or grow by a factor of 26.
# If p0 == 26: f(z) is either going to stay at roughly the same size, or shrink by a factor of 26.
# Heuristic: To ensure that z == 0, we want to ensure that f(z) shrinks by a factor of 26 whenever we have a p0 == 26 case
# This is more of an educated guess, but it works in this case.
# Aiming to fulfill this heuristic restricts our input space to a point that it's easy to do an exhaustive search
# We either start at the highest value, or at the lowest possible value, and move in the other direction until we find the first solution

def chunk(z: int, c0: int, c1: int, c2: int, input: int) -> int:
    if ((z % 26) + c1 == input):
        z = trunc(z / c0)
    else:
        z = trunc(z / c0)
        z = 26*z + input + c2

    return z


def solver(pars: list[tuple[int, int, int]], z: int, smallest: bool = False) -> tuple[int, ...]:
    if not pars:
        if z == 0:
            return ()
        else:
            return None
    
    for w in get_w(pars[0], z, smallest):
        next_z = chunk(z, *pars[0], w)
        res = solver(pars[1:], next_z, smallest)
        if res is not None:
            return (w,) + res

    return None


def get_w(par: tuple[int, int, int], z: int, smallest: bool = False) -> Generator[int, None, None]:
    if par[0] == 1:
        nums = range(9, 0, -1)
        if smallest: # Smallest numbers first, ie. count up
            nums = reversed(nums)
        for w in nums:
            yield w
    if par[0] == 26:
        w = (z % 26) + par[1]
        if 1 <= w <= 9:
            yield w

    return None


def verify(pars: list[tuple[int, int, int]], inputs: tuple[int, ...]) -> int:
    assert len(pars) == len(inputs)
    z = 0
    zs = [z := chunk(z, *p, w) for p, w in zip(pars, inputs)]

    return zs[-1] # This should be 0


def read_parameters(loc: str) -> list[tuple[int, int, int]]:
    parameters: list[tuple[int, int, int]] = []
    with open(loc) as f:
        r = list(f.readlines())
        chunks = [r[k:k+18] for k in range(0, len(r), 18)]
        for chunk in chunks:
            parameters.append((int(chunk[4][6:]), int(chunk[5][6:]), int(chunk[15][6:]),))
    return parameters


def check_parameter_predictions(pars: list[tuple[int, int, int]]) -> bool:
    """Check some conditions of our parameters."""
    count_p0 = 0
    for p in pars:
        assert p[0] == 1 or p[0] == 26
        if p[0] == 1:
            assert p[1] > 0
            count_p0 += 1
        if p[0] == 26:
            assert p[1] < 0
            count_p0 -= 1
        assert 1 < p[2] <= 13
    assert count_p0 == 0 # Same amount of occurences of p[0] == 26, as of p[0] == 1

    return True


def first(loc: str = './data/24.csv') -> int:
    pars = read_parameters(loc)
    check_parameter_predictions(pars)

    print("Parameters:")
    for p in pars:
        print(f"({p[0]:2d},{p[1]:3d},{p[2]:3d})")

    result = solver(pars, 0)
    res = int(''.join(map(str, result)))

    print(res)
    assert verify(pars, result) == 0
    return res


def second(loc: str = './data/24.csv') -> int:
    pars = read_parameters(loc)

    result = solver(pars, 0, True)
    res = int(''.join(map(str, result)))

    print(res)
    assert verify(pars, result) == 0
    return res


first()
second()

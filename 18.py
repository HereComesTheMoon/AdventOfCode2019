import typing

# I made one rather severe mistake here:
# I had to implement a binary tree, but instead of having my 'leaves' be objects of type SnailfishNumber without
# children, I instead had them be integers. This is bad since I had to do a lot of 'isinstance(self.l, int)'
# if statements to handle different cases. If I'd made them SnailfishNumbers, then this would've been easier
# This code is kind of am ess in general

def read(loc: str = './data/18.txt'):
    with open(loc) as f:
        return [x[:-1] for x in f.readlines()]


class SnailfishNumber:
    def __init__(self):
        self.l: typing.Union[int, SnailfishNumber] = 0
        self.r: typing.Union[int, SnailfishNumber] = 0
        self.p: typing.Union[None, SnailfishNumber] = None


    def _find_subnumbers(self, input: str) -> tuple[str, str]:
        assert len(input) >= 5
        assert self.l == 0 and self.r == 0
        assert input[0] == '['
        assert input[-1] == ']'

        count_opening_braces = 0
        input = input[1:-1]

        left, right = None, None

        for k, x in enumerate(input):
            if x == '[':
                count_opening_braces += 1
            elif x == ']':
                count_opening_braces -= 1
                assert count_opening_braces >= 0
            elif x == ',':
                if count_opening_braces == 0:
                    left = input[:k]
                    right = input[k + 1:]
                    break

        assert left is not None
        assert right is not None
        return left, right

    def build_from_string(self, input: str):
        left, right = self._find_subnumbers(input)

        # assert len(input) >= 5 at the beginning means that len(left)+left(right) >= 2
        if len(left) <= 2:
            self.l = int(left)
        else:
            self.l = SnailfishNumber()
            self.l.p = self
            self.l.build_from_string(left)
        if len(right) <= 2:
            self.r = int(right)
        else:
            self.r = SnailfishNumber()
            self.r.p = self
            self.r.build_from_string(right)


    def __add__(self, other: "SnailfishNumber") -> "SnailfishNumber":
        a = SnailfishNumber()
        a.l = self
        a.r = other
        self.p = a
        other.p = a
        a.reduce()
        return a

    def __repr__(self) -> str:
        return f"[{self.l},{self.r}]"

    def find_nested(self, depth: int = 0) -> bool:
        assert depth <= 4
        if depth == 4:
            assert isinstance(self.l, int)
            assert isinstance(self.r, int)
            return True
        if isinstance(self.l, int):
            a = False
        else:
            a = self.l.find_nested(depth + 1)
        if isinstance(self.r, int):
            b = False
        else:
            b = self.r.find_nested(depth + 1)
        return a or b

    def explode(self, depth: int = 0):
        if depth == 4:
            a = self
            while a.p is not None and a.p.l == a:
                a = a.p
            # print(f"Traveled up. {a=}. Now take step to the left, and travel down.")
            a = a.p
            if a is not None:
                if isinstance(a.l, int):
                    a.l += self.l
                else:
                    a = a.l
                    # print(f"Travel right next. {a=}")
                    while not isinstance(a.r, int):
                        a = a.r
                    # print(f"{self=}")
                    a.r += self.l

            b = self
            while b.p is not None and b.p.r == b:
                b = b.p
            # print(f"Traveled up. {b=}. Now take step to the right, and travel down.")
            b = b.p
            if b is not None:
                if isinstance(b.r, int):
                    b.r += self.r
                else:
                    b = b.r
                    # print(f"Travel left next. {b=}")
                    while not isinstance(b.l, int):
                        b = b.l
                    # print(f"{self=}")
                    b.l += self.r
            if self.p.l == self:
                self.p.l = 0
            else:
                self.p.r = 0
            return True
        else:
            if not isinstance(self.l, int):
                if self.l.explode(depth + 1):
                    return True
            if not isinstance(self.r, int):
                if self.r.explode(depth + 1):
                    return True
            return False

    def split(self):
        if isinstance(self.l, int):
            if self.l > 9:
                num = self.l
                self.l = SnailfishNumber()
                self.l.l = num // 2
                self.l.r = (num + 1) // 2
                self.l.p = self
                return True
        elif self.l.split():
            return True
        if isinstance(self.r, int):
            if self.r > 9:
                num = self.r
                self.r = SnailfishNumber()
                self.r.l = num // 2
                self.r.r = (num + 1) // 2
                self.r.p = self
                return True
        elif self.r.split():
            return True
        return False

    def reduce(self):
        while True:
            if self.explode():
                continue
            elif self.split():
                continue
            else:
                break

    def __int__(self):
        return 3 * int(self.l) + 2 * int(self.r)


def first(nums: list[str]):
    result = SnailfishNumber()
    result.build_from_string(nums[0])
    for x in nums[1:]:
        next_num = SnailfishNumber()
        next_num.build_from_string(x)
        result = result + next_num
    print(int(result))
    return int(result)


def second(nums: list[str]):
    import itertools
    maxi = 0
    for x,y in itertools.permutations(nums, 2):
        num1 = SnailfishNumber()
        num2 = SnailfishNumber()
        num1.build_from_string(x)
        num2.build_from_string(y)
        summ = num1 + num2
        maxi = max(int(summ), maxi)

    print(maxi)
    return maxi


if __name__ == '__main__':
    first(read())
    second(read())


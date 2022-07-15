def read(loc: str) -> list[str]:
    with open(loc) as f:
        r = f.readlines()
        # data = [[x for x in row[:-1]] for row in r]
        data = [row[:-1] for row in r]
        return data


def syntax_score(errors: list) -> int:
    matches = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137
    }
    return sum( matches[x] for x in errors )


def completion_score(nums: list) -> int:
    matches = {
        '(': 1,
        '[': 2,
        '{': 3,
        '<': 4
    }
    if not nums:
        return 0
    return 5*completion_score(nums[1:]) + matches[nums[0]]


def first(loc: str = './data/10.csv') -> int:
    matches = {
        '(': ')',
        '[': ']',
        '{': '}',
        '<': '>'
    }
    data = read(loc)
    errors = []
    for row in data:
        stack = []
        for x in row:
            if x in matches.keys():
                stack.append(x)
            elif x in matches.values(): # Always true
                if matches[stack[-1]] == x:
                    stack.pop()
                else:
                    errors.append(x)
                    break
    res = syntax_score(errors)
    print(res)
    return res


def second(loc: str = './data/10.csv') -> int:
    matches = {
        '(': ')',
        '[': ']',
        '{': '}',
        '<': '>'
    }
    data = read(loc)
    scores = []
    for row in data:
        stack = []
        for x in row:
            if x in matches.keys():
                stack.append(x)
            elif matches[stack[-1]] == x:
                stack.pop()
            else:
                stack = []
                break
        scores.append(completion_score(stack))
    scores = [x for x in scores if x != 0]
    scores.sort()
    res = scores[(len(scores)-1)//2]
    print(res)
    return res


first()
second()


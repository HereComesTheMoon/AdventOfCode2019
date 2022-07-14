import csv


# 8:25

def read():
    with open('./data/10.csv') as f:
        return list(csv.reader(f))


def syntax_score(errors: list):
    matches = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137
    }
    return sum( matches[x] for x in errors )


def completion_score(nums: list):
    matches = {
        '(': 1,
        '[': 2,
        '{': 3,
        '<': 4
    }
    if not nums:
        return 0
    return 5*completion_score(nums[1:]) + matches[nums[0]]


def first():
    matches = {
        '(': ')',
        '[': ']',
        '{': '}',
        '<': '>'
    }
    data = read()
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
    return syntax_score(errors)


def second():
    matches = {
        '(': ')',
        '[': ']',
        '{': '}',
        '<': '>'
    }
    data = read()
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
    return scores[(len(scores)-1)//2]


print(second())




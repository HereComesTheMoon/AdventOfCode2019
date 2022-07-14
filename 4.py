import copy
import csv


def readBingo():
    with open('./data/4a.csv') as f:
        r = csv.reader(f, delimiter=',')
        draws = [int(x) for x in r.__next__()]
    with open('./data/4b.csv') as f:
        r = csv.reader(f, delimiter=',')
        rows = [list(map(int, x)) for x in r if x]
        assert len(rows) % 5 == 0
        boards = []
        for k in range(len(rows) // 5):
            temp = []
            for x in rows[k * 5:(k + 1) * 5]:
                temp += x
            boards.append(copy.deepcopy(temp))
    return draws, boards


def boardWon(board: list[int, ...], drawn: list[int, ...]):
    results = [x in drawn for x in board]
    for k in range(5):
        if all(results[k * 5:(k + 1) * 5]) or all(results[k:k + 25:5]):
            return results
    return False


def printBoard(board: list[int, ...]):
    for k in range(5):
        print(board[k * 5:(k + 1) * 5])


def first():
    draws, boards = readBingo()
    for k in range(len(draws)):
        print(draws[:k])
        for x in boards:
            if results := boardWon(x, draws[:k]):
                printBoard(x)
                printBoard(results)
                print(draws[k - 1])
                a = sum([y for y, b in zip(x, results) if not b]) * draws[k - 1]
                print(a)
                return a


def second():
    draws, boards = readBingo()
    won = []
    for k in range(len(draws)):
        print(draws[:k])
        for j, x in enumerate(boards):
            if results := boardWon(x, draws[:k]):
                if j in won:
                    continue
                won.append(j)
                printBoard(x)
                printBoard(results)
                print(draws[k - 1])
                a = sum([y for y, b in zip(x, results) if not b]) * draws[k - 1]
                print(a)


first()
a = []


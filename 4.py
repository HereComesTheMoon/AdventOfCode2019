from itertools import chain
from tabulate import tabulate



def readBingo():
    with open('./data/4.csv') as f:
        first_row = f.readline()
        draws = list(map(int, first_row.split(",")))

        rows = f.readlines()
        boards = []
        while rows:
            next_board = rows[1:6]
            rows = rows[6:]
            boards.append(list(chain.from_iterable(map(int, row.split()) for row in next_board)))
    return draws, boards


def boardWon(board: list[int], drawn: list[int]):
    results = [x in drawn for x in board]
    for k in range(5):
        if all(results[k * 5:(k + 1) * 5]) or all(results[k:k + 25:5]):
            return results
    return False


def printBoard(board: list[int], name: str = ""):
    a = [board[k * 5:(k + 1) * 5] for k in range(5)]
    if name:
        print(name)
    print(tabulate(a))



def first():
    draws, boards = readBingo()
    for k in range(len(draws)):
        for x in boards:
            if results := boardWon(x, draws[:k]):
                printBoard(x, "Winning board:")
                printBoard(results, "Results:")
                print(draws[k - 1])
                a = sum([y for y, b in zip(x, results) if not b]) * draws[k - 1]
                print(a)
                return a


def second():
    draws, boards = readBingo()
    won = []
    for k in range(len(draws)):
        for j, x in enumerate(boards):
            if results := boardWon(x, draws[:k]):
                if j in won:
                    continue
                won.append(j)
                printBoard(x, "Losing board:")
                printBoard(results)
                a = sum([y for y, b in zip(x, results) if not b]) * draws[k - 1]
                print(a)


second()


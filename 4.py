from itertools import chain
from tabulate import tabulate



def readBingo(loc: str) -> tuple[list[int], list[list[int]]]:
    with open(loc) as f:
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



def first(loc: str = './data/4.csv'):
    draws, boards = readBingo(loc)
    for k in range(len(draws)):
        for x in boards:
            if results := boardWon(x, draws[:k]):
                printBoard(x, "Winning board:")
                printBoard(results, "Results:")
                print(draws[k - 1])
                a = sum([y for y, b in zip(x, results) if not b]) * draws[k - 1]
                print(a)
                return a


def second(loc: str = './data/4.csv'):
    draws, boards = readBingo(loc)
    wins_at = 0
    wins_val = 0
    for board in boards:
        for k in range(len(draws)):
            if results := boardWon(board, draws[:k]):
                if k > wins_at:
                    printBoard(results)
                    wins_at = k
                    wins_val = sum([y for y, b in zip(board, results) if not b]) * draws[k - 1]
                break
    print(f"Worst board wins after {wins_at} turns, with final score {wins_val}.")
    return wins_val

first()
second()

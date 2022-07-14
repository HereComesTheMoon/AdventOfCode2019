import collections
import copy
import math

REQ = 3000 + 10 + 40 + 30 # + 8
colors = ['A', 'B', 'C', 'D']
COST = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000
}

ROOMS = {
    'A': list('ADDC'),
    'B': list('DCBC'),
    'C': list('ABAD'),
    'D': list('BACB')
}

TESTROOMS = {  # 44169
    'A': list('BA'),
    'B': list('CD'),
    'C': list('BC'),
    'D': list('DA')
}
TESTROOMS2 = {
    'A': list('BDDA'),
    'B': list('CCBD'),
    'C': list('BBAC'),
    'D': list('DACA')
}

TR = {
    'A': list('DA'),
    'B': list('BB'),
    'C': list('CC'),
    'D': list('AD')
}
ROOM_LOC = {
    'A': 2,
    'B': 4,
    'C': 6,
    'D': 8,
}

CORRIDOR = [None] * 11


class Board:
    def __init__(self, corridor: list, rooms: dict, energy: int):
        self.corridor = corridor
        self.rooms = rooms
        self.energy = energy

    def __repr__(self):
        rep = "# Energy: " + str(self.energy) + "\n" + "#" + "".join(
            ['.' if x is None else x for x in self.corridor]) + "#\n"
        rooms = ""  # + "".join([str([x[k] for x in self.rooms.values()]) for k in range(len(self.rooms['A']))])
        for k in range(len(list(self.rooms.values())[0])):
            rooms += "   "
            for room in self.rooms.values():
                if room[k] is None:
                    rooms += ". "
                else:
                    rooms += room[k] + " "
            rooms += "  \n"
        return rep + rooms + "#" * 13


def move_to_room(x: str, x_pos: int, corridor: list, room: list) -> int:
    if x_pos == ROOM_LOC[x]:
        if all(y is None or y == x for y in room):
            return -1
    if x_pos < ROOM_LOC[x]:
        if any(y is not None for y in corridor[x_pos + 1:ROOM_LOC[x] + 1]):
            # print("here")
            return -1
    else:
        if any(y is not None for y in corridor[ROOM_LOC[x]:x_pos]):
            # print("her2e")
            return -1

    for j, y in list(enumerate(room))[::-1]:  # Reversed list with correct indices
        # print(f"Check room availability: {j=}, {y=}, {x=}")
        if y is None:
            # print("here3")
            return j
        if y != x:
            return -1
    return -1


def trivial_moves(board: Board):
    # Moves by amphipods in corridor. Can only move into the right room.
    for k, x in enumerate(board.corridor):
        if x is None:
            continue
        if (pos := move_to_room(x, k, board.corridor, board.rooms[x])) != -1:
            board.corridor[k] = None
            board.rooms[x][pos] = x
            board.energy += COST[x] * (abs(ROOM_LOC[x] - k) + 1 + pos)  # Move in front of room + enter + move to pos

    # Moves amphipods out of rooms, into target room
    for room_color, room in board.rooms.items():
        for k, x in enumerate(room):
            if x is None:  # Empty, check next element instead
                continue
            if k > 0 and room[k - 1] is not None:  # Path blocked either way, stop checking
                break
            # Path out of room free. Check if goal_room empty, and path available. If so, move
            if (pos := move_to_room(x, ROOM_LOC[room_color], board.corridor, board.rooms[x])) != -1:
                room[k] = None
                board.rooms[x][pos] = x
                # Move out of room + move in front of room + enter + move to pos
                board.energy += COST[x] * (abs(ROOM_LOC[x] - ROOM_LOC[room_color]) + 2 + pos + k)

    return board


def moves(board: Board):
    for room_color, room in board.rooms.items():
        for k, x in enumerate(room):
            if x is None:
                continue
            if k > 0 and room[k - 1] is not None:
                break
            if all(y == room_color for y in room[k:]):
                break
            accessible = accessible_corridor(board.corridor, ROOM_LOC[room_color])
            for pos in accessible:
                board_new = copy.deepcopy(board)
                board_new.corridor[pos] = x
                board_new.rooms[room_color][k] = None
                board_new.energy += COST[x] * (1 + abs(ROOM_LOC[room_color] - pos) + k)
                board_new = trivial_moves(board_new)
                yield board_new


def accessible_corridor(corridor: list, start_pos: int):
    for k in range(start_pos - 1 , -1, -1):
        if corridor[k] is not None:
            break
        if k not in ROOM_LOC.values():
            yield k

    for k in range(start_pos + 1, len(corridor)):
        if corridor[k] is not None:
            break
        if k not in ROOM_LOC.values():
            yield k


def solve():
    boards = [Board([None] * 11, TESTROOMS, 0)]
    print(boards[0])

    board = boards[0]
    board = trivial_moves(board)
    smooth = moves(board)
    for x in smooth:
        print(x)
        assert x == trivial_moves(x)
        smooth2 = moves(x)
        for y in smooth2:
            print(y)


def done(board: Board) -> bool:
    for room_color, room in board.rooms.items():
        if any(x != room_color for x in room):
            return False
    return True


def second():
    boards = [Board([None] * 11, TESTROOMS2, 0)]

    minimum = math.inf
    while boards:
        nxt = boards.pop()
        # print(nxt)
        nxt = trivial_moves(nxt)
        # print(nxt)
        if nxt.energy > 45169:
            continue
        # if nxt.energy == 4479:
        #     assert False
        if done(nxt):  # 11599
            minimum = min(minimum, nxt.energy)
            print(minimum)
            continue

        new_boards = moves(nxt)
        if nxt.corridor[-1] == 'D' and nxt.corridor[7] == 'B' and nxt.corridor[0] == 'A' and nxt.corridor[-2] == 'B' and nxt.corridor[1] == 'A' and nxt.corridor[3] == 'D':
            print("Nxt:")
            print(nxt)
            for new_board in new_boards:
                print(new_board)
            print(" NEXT OVER")
        else:
            for new_board in new_boards:
                boards.append(new_board)



    return minimum


print(second())

# solve()

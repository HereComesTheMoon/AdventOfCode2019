from collections import Counter
from typing import NamedTuple, Final, Iterable, Union, Generator
import heapq
from math import inf
from itertools import chain
# from tabulate import tabulate

# Rooms = namedtuple('Rooms', 'A B C D')

Rooms = NamedTuple("Rooms", [
    ('A', str),
    ('B', str),
    ('C', str),
    ('D', str),
])


# Important note: From each valid state the next possible moves only depend on the current state.


class State:
    room_index = {
            'A': 0,
            'B': 1,
            'C': 2,
            'D': 3,
        }
    room_place = {
            'A': 2,
            'B': 4,
            'C': 6,
            'D': 8,
        }

    def __init__(self, hallway: str, rooms: Rooms, energy: int) -> None:
        assert len(hallway) == 11 # Hallway is 11 tiles long
        assert all(len(room) for room in rooms) # No empty rooms, not implemented. Would be a bad idea.
        self.hallway: Final[str] = hallway
        self.rooms: Final[Rooms] = Rooms(*rooms)
        self.energy: int = energy


    def __key(self) -> tuple[str, Rooms]:
        return (self.hallway, self.rooms)


    def __hash__(self) -> int:
        return hash(self.__key())


    def __eq__(self, other: "State") -> bool:
        return self.__key() == other.__key()


    def __lt__(self, other: "State") -> bool:
        return self.energy < other.energy


    def __gt__(self, other: "State") -> bool:
        return self.energy > other.energy

    def __repr__(self):
        rep = "\n" + "|" + self.hallway + "|\n"
        for k in range(max(len(room) for room in self.rooms)):
            row = ["  |"] + [self.rooms[i][k] + "|" if k < len(self.rooms[k]) else "~|" for i in range(4)] + ["   \n"]
            rep += "".join(row)
        
        return rep[:-1].replace(" ", ".")


    def verify_state(self) -> bool:
        """Is the current state even valid? Right number of amphipods per room? This method was written first. This is not exhaustive: Whether it's possible to reach this state with a given energy value is not clear. Hence, self.energy has to stay mutable, and we cannot check it. Also, we cannot check whether a move was valid, ie. whether this valid board state was reached via a valid sequence of moves."""
        counter = Counter(chain(self.hallway, *self.rooms))

        # Check if the only symbols are ' ', 'A', 'B', 'C', 'D'
        number_distinct_symbols = len(counter) == 5

        # Check that the spaces in front of the rooms are not occupied
        spaces_empty = all(x == ' ' for x in self.hallway[2:9:2])

        # Check if there are no empty tiles behind amphipods
        empty_tiles_behind_amphipods_A = all(x == ' ' for x in self.rooms.A[: self.rooms.A.rfind(' ') + 1])
        empty_tiles_behind_amphipods_B = all(x == ' ' for x in self.rooms.B[: self.rooms.B.rfind(' ') + 1])
        empty_tiles_behind_amphipods_C = all(x == ' ' for x in self.rooms.C[: self.rooms.C.rfind(' ') + 1])
        empty_tiles_behind_amphipods_D = all(x == ' ' for x in self.rooms.D[: self.rooms.D.rfind(' ') + 1])

        # Check if the number of amphipods of type X corresponds to the number of spots in room X
        a = counter['A'] == len(self.rooms.A)
        b = counter['B'] == len(self.rooms.B)
        c = counter['C'] == len(self.rooms.C)
        d = counter['D'] == len(self.rooms.D)

        verify = [
                number_distinct_symbols,
                spaces_empty,
                empty_tiles_behind_amphipods_A,
                empty_tiles_behind_amphipods_B,
                empty_tiles_behind_amphipods_C,
                empty_tiles_behind_amphipods_D,
                a,
                b,
                c,
                d]
        verify_names = [
                "number_distinct_symbols",
                "spaces_empty",
                "empty_tiles_behind_amphipods_A",
                "empty_tiles_behind_amphipods_B",
                "empty_tiles_behind_amphipods_C",
                "empty_tiles_behind_amphipods_D",
                "a",
                "b",
                "c",
                "d"]

        if not all(verify):
            print(f"{State} is in an invalid state.")
            print(counter)
            for val, name in zip(verify, verify_names):
                if not val:
                    print(f"Violated: {name}")
            return False

        return True


    def check_move(self, start: tuple[str, int], goal: tuple[str, int]) -> bool:
        match start, goal:
            case ('H', _), ('H', _):
                assert False
            case ('H', _), _:
                s = start[1]
                room_index = State.room_index[goal[0]]
                room_place = State.room_place[goal[0]]
                assert s in range(len(self.hallway))
                assert goal[1] in range(len(self.rooms[room_index]))

                # Check that we are moving into the right room
                if self.hallway[s] != goal[0]:
                    return False

                # Check that the hallway is free
                if s < room_place:
                    if any(tile != ' ' for tile in self.hallway[s+1:room_place+1]):
                        return False
                else:
                    if any(tile != ' ' for tile in self.hallway[room_place:s]):
                        return False

                # Check that the room is free
                if any(tile != ' ' for tile in self.rooms[room_index][0:goal[1]+1]):
                    return False
                return True
            case _, ('H', _):
                g = goal[1]
                room_index = State.room_index[start[0]]
                room_place = State.room_place[start[0]]
                amphipod_type = self.rooms[room_index][start[1]]
                assert g in range(len(self.hallway))
                assert start[1] in range(len(self.rooms[room_index]))
                assert amphipod_type != ' '

                # Check that we are not moving onto a tile in front of a room 
                if g in State.room_place.values():
                    return False

                # Check that the hallway is free
                if g < room_place:
                    if any(tile != ' ' for tile in self.hallway[g:room_place+1]):
                        return False
                else:
                    if any(tile != ' ' for tile in self.hallway[room_place:g+1]):
                        return False

                # Check that the space in the room in front of us is free
                if any(tile != ' ' for tile in self.rooms[room_index][0:start[1]]):
                    return False

                # Check that we are not in position in our room yet
                if all(tile == start[0] for tile in self.rooms[room_index][start[1]:]):
                    return False
                return True

            case _:
                # Move from room to room
                start_room = self.rooms[State.room_index[start[0]]]
                start_room_place = State.room_place[start[0]]
                goal_room = self.rooms[State.room_index[goal[0]]]
                goal_room_place = State.room_place[goal[0]]
                amphipod_type = start_room[start[1]]

                assert goal[0] != start[0] # Starting room is not goal room
                assert amphipod_type == goal[0] # Move into right type of room, in particular amphipod_type != ' '
                assert start[1] in range(len(start_room))
                assert goal[1] in range(len(goal_room))

                hallway_range = self.hallway[min(start_room_place, goal_room_place):max(start_room_place, goal_room_place) + 1]
                # Check that hallway is free 
                if any(tile != ' ' for tile in hallway_range):
                    return False

                # Check that the space in the room in front of us is free
                if any(tile != ' ' for tile in start_room[0:start[1]]):
                    return False

                # check that goal room has no wrong amphipods in it 
                if any(tile != amphipod_type for tile in goal_room[goal[1]+1:]):
                    return False

                # Check that tiles in goal room are free 
                if any(tile != ' ' for tile in goal_room[:goal[1]+1]):
                    return False

                return True

        assert False

    def visible_hallway_space(self, tile: int) -> tuple[int, int]:
        l = tile
        while 0 <= l and self.hallway[l] == ' ':
            l -= 1
        if self.hallway[tile] == ' ':
            l += 1

        r = tile 
        while r < len(self.hallway) and self.hallway[r] == ' ':
            r += 1

        return l, r

    def move(self, start: tuple[str, int], goal: tuple[str, int]) -> "State":
        assert self.check_move(start, goal)
        match start, goal:
            case ('H', _), ('H', _):
                assert False
            case ('H', _), _:
                hw = self.hallway[:start[1]] + (" ") + self.hallway[start[1]+1:]
                room_index = State.room_index[goal[0]]
                ro = list(self.rooms)
                _ro = self.rooms[room_index]
                ro[room_index] = _ro[:goal[1]] + start[0] + _ro[goal[1]+1:]
                new_state = State(hw, Rooms(*ro), 0)
            case _, ('H', _):
                room_index = State.room_index[start[0]]
                hw = self.hallway[:goal[1]] + self.rooms[room_index][start[1]] + self.hallway[goal[1]+1:]
                ro = list(self.rooms)
                _ro = self.rooms[room_index]
                ro[room_index] = _ro[:start[1]] + " " + _ro[start[1]+1:]
                print(hw)
                print(ro)
                new_state = State(hw, Rooms(*ro), 0)
            case _:
                hw = self.hallway[:goal[1]] + (" ") + self.hallway[goal[1]+1:]
                room_index = State.room_index[start[0]]
                ro = list(self.rooms)
                _ro = self.rooms[room_index]
                ro[room_index] = _ro[:start[1]] + goal[0] + _ro[start[1]+1:]
                new_state = State(hw, Rooms(*ro), 0)
        assert new_state.verify_state()
        return new_state
        # next_state = State(

                # )
        # return self

    def neighbours(self) -> Generator["State", None, None]:
        """Types of moves: 1. Move amphipod into target room. 2. Move amphipod into hallway """
        # Move into room:
        # Iterate through the rooms, and search for an amphipod capable of moving into it
        # rooms_state: dict[str, tuple[bool, int]] = {} # rooms_state['A'] = possible_to_move_into_room, index_of_tile
        rooms_first: dict[str, int] = {} # Index of first occupied tile
        for amphipod_type, room in zip(State.room_index, self.rooms):
            first_occupied_tile = room.rfind(' ')
            # Equal to 0 if room is full
            # Equal to len(room) if room is empty, need to check this when accessing
            rooms_first[amphipod_type] = first_occupied_tile + 1

        for amphipod_type, room in zip(State.room_index, self.rooms):
            first_occupied_tile = rooms_first[amphipod_type]
            goal = (amphipod_type, first_occupied_tile - 1)
            if first_occupied_tile == len(room): # Room empty
                continue
            if any(tile != amphipod_type for tile in room[first_occupied_tile:]): # Can't move into this room yet
                continue
            l, r = self.visible_hallway_space(State.room_place[amphipod_type])
            if 0 < l and self.hallway[l - 1] == amphipod_type:
                yield self.move(("H", l-1), goal)
            if r < len(self.hallway) - 1 and self.hallway[r] == amphipod_type:
                yield self.move(("H", r), goal)
            for start_room_name, k in State.room_index.items():
                start_i = rooms_first[start_room_name] 
                if start_i == len(self.rooms[k]):
                    continue
                if self.rooms[k][start_i] != amphipod_type:
                    continue
                if amphipod_type == start_room_name:
                    continue
                if l <= State.room_place[start_room_name] < r:
                    yield self.move((start_room_name, start_i), goal)

        # Next: Move out of a room onto a hallway tile
        for start_room_name, k in State.room_index.items():
            start_i = rooms_first[start_room_name]
            if start_i == len(self.rooms[k]):
                continue
            l, r = self.visible_hallway_space(State.room_place[start_room_name])
            for tile in range(l, r):
                if tile in State.room_place.values():
                    continue
                yield self.move((start_room_name, start_i), ("H", tile))

        return None

            

class PriorityQueue():
    def __init__(self, starting_list: list[State]) -> None:
        self.q: list[State] = starting_list
        heapq.heapify(self.q)


    def put(self, item: State):
        heapq.heappush(self.q, item)


    def get(self) -> State:
        return heapq.heappop(self.q)


    def __bool__(self) -> bool:
        return bool(self.q)


    # def binary_search(self, goal: State) -> int:
        # current = 0
        # while goal < self.q[current]:
            # pass

    # def siftdown(self, startpos: int, pos: int):
        # heapq._siftdown(self.q, startpos, pos)


class Game:
    def __init__(self, starting_state: State) -> None:
        starting_state.verify_state()
        self.goal_state = State( " "*11, Rooms("A"*len(starting_state.rooms.A),
                                               "B"*len(starting_state.rooms.B),
                                               "C"*len(starting_state.rooms.C),
                                               "D"*len(starting_state.rooms.D)), 0)
        self.goal_state.verify_state()

        self.states: set[State] = {starting_state}
        self.visited: set[State] = set()

        self.frontier: PriorityQueue = PriorityQueue([starting_state])


    def search(self) -> int:
        while self.frontier:
            print("h")
            visiting = self.frontier.get()
            if visiting in self.visited:
                print("heh, not this time kiddo")
                break
            self.visited.add(visiting)
            if visiting == self.goal_state:
                print("Huzzah")
                print(visiting.energy)
                return(visiting.energy)
            for node in visiting.neighbours():
                if node not in self.visited:
                    print("ha")
                    self.frontier.put(node)
        return -1


def test():
    rooms = Rooms("AB", "BA", "CC", " D")
    state = State("         D ", rooms, 0)

    state.verify_state()
    sorted([state, state])


    Game(state)

    rooms = Rooms("  ", "BB", "CA", " D")
    state = State("CA       D ", rooms, 0)
    print(state.check_move(("H", 1), ("A", 1)))
    print(state.check_move(("H", 0), ("A", 1)))
    print(state.check_move(("H", 0), ("B", 1)))
    print(state.check_move(("H", 9), ("D", 1)))
    print(state.check_move(("H", 9), ("D", 0)))
    print()
    print(state)
    try:
        state.check_move(("A", 0), ("H", 0))
        state.check_move(("A", 1), ("H", 0))
        state.check_move(("A", 0), ("H", 1))
        state.check_move(("A", 1), ("H", 1))
        state.check_move(("A", 0), ("H", 2))
        state.check_move(("A", 1), ("H", 2))
        state.check_move(("A", 0), ("H", 3))
        state.check_move(("A", 1), ("H", 3))
    except AssertionError:
        pass


    assert state.check_move(("B", 0), ("H", 0)) == False
    assert state.check_move(("B", 1), ("H", 0)) == False
    assert state.check_move(("B", 0), ("H", 1)) == False
    assert state.check_move(("B", 1), ("H", 1)) == False
    assert state.check_move(("B", 0), ("H", 2)) == False
    assert state.check_move(("B", 1), ("H", 2)) == False
    assert state.check_move(("B", 0), ("H", 3)) == False
    assert state.check_move(("B", 1), ("H", 3)) == False

    assert state.check_move(("C", 0), ("H", 0)) == False
    assert state.check_move(("C", 0), ("H", 1)) == False
    assert state.check_move(("C", 0), ("H", 2)) == False
    assert state.check_move(("C", 0), ("H", 3)) == True
    assert state.check_move(("C", 0), ("H", 4)) == False
    assert state.check_move(("C", 0), ("H", 5)) == True
    assert state.check_move(("C", 0), ("H", 6)) == False
    assert state.check_move(("C", 0), ("H", 7)) == True
    assert state.check_move(("C", 0), ("H", 8)) == False
    assert state.check_move(("C", 0), ("H", 9)) == False
    assert state.check_move(("C", 0), ("H", 10)) == False


    rooms = Rooms(" D", "BB", "CA", " D")
    state = State("CA         ", rooms, 0)
    print(state)
    assert state.check_move(("A", 1), ("D", 0)) == True
    # assert state.check_move(("A", 0), ("D", 0)) == False
    assert state.check_move(("A", 1), ("D", 1)) == False
    # assert state.check_move(("A", 1), ("C", 1)) == False
    # assert state.check_move(("A", 1), ("C", 0)) == False


rooms = Rooms("BA", "CD", "BC", "DA")
state = State("           ", rooms, 0)

state.verify_state()

g = Game(state)
g.search()


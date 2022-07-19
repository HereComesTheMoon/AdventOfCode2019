from collections import Counter
from typing import NamedTuple, Final, Iterable
import heapq
# from dataclasses import dataclass
import itertools
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


    def verify_state(self) -> bool:
        """Is the current state even valid? Right number of amphipods per room? This method was written first. This is not exhaustive: Whether it's possible to reach this state with a given energy value is not clear. Hence, self.energy has to stay mutable, and we cannot check it. Also, we cannot check whether a move was valid, ie. whether this valid board state was reached via a valid sequence of moves."""
        counter = Counter(itertools.chain(self.hallway, *self.rooms))

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
        
    def neighbours(self) -> Iterable["State"]:
        pass

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


class Node:
    def __init__(self, content: State) -> None:
        self.content = content


class Game:
    def __init__(self, starting_state: State) -> None:
        starting_state.verify_state()
        self.goal_state = State( " "*11, Rooms("A"*len(starting_state.rooms.A),
                                               "B"*len(starting_state.rooms.B), 
                                               "C"*len(starting_state.rooms.C), 
                                               "D"*len(starting_state.rooms.D)), 0)
        self.goal_state.verify_state()

        self.states: dict[State, None] = {starting_state: None}
        self.visited: set[State] = set()

        self.frontier: PriorityQueue = PriorityQueue([starting_state])


    def search(self):
        self.frontier
        while self.frontier:
            visiting = self.frontier.get()
            if visiting == self.goal_state:
                print("Huzzah")
                print(visiting.energy)
                print("Huzzah")
                break
            for adjacent in visiting.neighbours():
                # if adjacent in self.states:
                    # self.states[adjacent]
                    # self.states.add(adjacent)
                self.frontier.put(adjacent)

        










rooms = Rooms("AB", "BA", "CC", " D")
state = State("         D ", rooms, 0)

state.verify_state()
sorted([state, state])


Game(state)


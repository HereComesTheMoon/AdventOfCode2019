from collections import namedtuple
from typing import NamedTuple

ROOM_LOC = {
    'A': 2,
    'B': 4,
    'C': 6,
    'D': 8,
}

COST = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000
}

Room = namedtuple('Room', ['A', 'B', 'C', 'D'])


class Node:
    def __init__(self, floor: str, rooms: Room, energy: int):
        self.floor = floor
        self.rooms = rooms
        self.energy = energy

    def moves(self):
        result = []
        for k, room in zip(Room._fields, self.rooms):
            print(k, room)
            print(room.find('D'))
            i = len(room) - len(room.lstrip('.')) # Index of first non-empty tile in the room
            if len(room) != i:


    def new_node(self, ):

            print( len(room) - len(room.lstrip('D')))




if __name__ == '__main__':
    test_room = Room('BDDA', 'CCBD', 'BBAC', 'DACA')
    node = Node("." * 11, test_room, 0)
    node.moves()

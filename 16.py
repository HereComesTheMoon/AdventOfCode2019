import math
from typing import Callable


class Packet:
    operators: list[Callable[..., int]] = [
        sum,
        math.prod,
        min,
        max,
        lambda _: 0, # This should never be called.
        lambda x, y: x > y,
        lambda x, y: x < y,
        lambda x, y: x == y
    ]

    def __init__(self, msg: str) -> None:
        self.version: str = msg[:3]
        self.type_id: str = msg[3:6]
        self.value: str = ""
        self.len_id: str = ""
        self.content: list["Packet"] = []

        if self.type_id == '100':
            self.value = self.literal_value(msg[6:])
        else:
            self.len_id = msg[6]
            self.content = self.operator(msg[6:])

    def operator(self, content: str) -> list["Packet"]:
        subpackets = []
        if self.len_id == '0':
            len_of_subpackets_in_bits = int(content[1:16], 2)
            pos = 16
            while pos < 16 + len_of_subpackets_in_bits:
                actual_content = content[pos:16 + len_of_subpackets_in_bits]
                subpacket = Packet(actual_content)
                pos += len(subpacket)
                subpackets.append(subpacket)
            return subpackets

        if self.len_id == '1':
            number_of_subpackets = int(content[1:12], 2)
            pos = 12
            for _ in range(number_of_subpackets):
                subpacket = Packet(content[pos:])
                pos += len(subpacket)
                subpackets.append(subpacket)
            return subpackets

        assert False

    def literal_value(self, content: str) -> str:
        assert self.type_id == '100'  # Literal value package
        leading_bit = content[0]
        self.value = ""
        k = 0
        while leading_bit == '1':
            self.value += content[k + 1:k + 5]
            k += 5
            leading_bit = content[k]
        assert leading_bit == '0'
        self.value += content[k + 1:k + 5]
        # print("value", type(self.value), self.value)
        return self.value

    def __len__(self) -> int:
        if self.type_id == '100':
            assert isinstance(self.value, str)
            assert len(self.value) % 4 == 0
            # Return len of header + length of content.
            temp_len = 6 + 5 * len(self.value) // 4
            return temp_len
        else:
            # Operator containing subpackages, return sum of subpackages + header
            return 6 + 12 + 4 * (self.len_id == '0') + sum(map(len, self.content))


    def version_sum(self) -> int:
        if self.type_id == '100':
            return int(self.version, 2)
        else:
            return int(self.version, 2) + sum(map(lambda l: l.version_sum(), self.content))


    def compute(self) -> int:
        if self.type_id == '100':
            return int(self.value, 2)

        op = Packet.operators[int(self.type_id, 2)]

        if 5 <= int(self.type_id, 2) <= 7:
            return op(self.content[0].compute(), self.content[1].compute())

        return op([x.compute() for x in self.content])


def read(loc: str = './data/16.txt') -> str:
    def hex_to_bin(c: str):
        assert len(c) == 1
        res = bin((int(c, 16)))[2:]
        return "0" * (4 - len(res)) + res

    with open(loc) as f:
        msg = f.read()[:-1]
        return "".join([hex_to_bin(c) for c in msg])


def first() -> int:
    p = Packet(read())
    res = p.version_sum()
    print(res)
    return res


def second() -> int:
    p = Packet(read())
    res = p.compute()
    print(res)
    return res


if __name__ == '__main__':
    first()
    second()


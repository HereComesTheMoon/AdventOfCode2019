import math


class Packet:
    operators = [
        sum,
        math.prod,
        min,
        max,
        None,
        lambda x, y: x > y,
        lambda x, y: x < y,
        lambda x, y: x == y
    ]

    def __init__(self, msg: str):
        self.version = msg[:3]
        self.type_id = msg[3:6]

        if self.type_id == '100':
            self.value = self.literal_value(msg[6:])
        else:
            self.len_id = msg[6]
            self.content = self.operator(msg[6:])
        # self.content = msg[6:]
        # self.value = self._type()

    def operator(self, content: str):
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
            for k in range(number_of_subpackets):
                subpacket = Packet(content[pos:])
                pos += len(subpacket)
                subpackets.append(subpacket)
            return subpackets

    def literal_value(self, content: str):
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

    def __len__(self):
        if self.type_id == '100':
            assert isinstance(self.value, str)
            assert len(self.value) % 4 == 0
            # Return len of header + length of content.
            temp_len = 6 + 5 * len(self.value) // 4
            return temp_len
            # return temp_len + (4 - (temp_len % 4)) % 4 # Adjust for closing zeroes ACTUALLY WRONG
        else:
            # Operator containing subpackages, return sum of subpackages + header
            return 6 + 12 + 4 * (self.len_id == '0') + sum(map(len, self.content))

    def version_sum(self):
        if self.type_id == '100':
            return int(self.version, 2)
        else:
            return int(self.version, 2) + sum(map(lambda l: l.version_sum(), self.content))

    def compute(self):
        if self.type_id == '100':
            return int(self.value, 2)

        op = Packet.operators[int(self.type_id, 2)]

        if 5 <= int(self.type_id, 2) <= 7:
            return op(self.content[0].compute(), self.content[1].compute())

        return op([x.compute() for x in self.content])


def read(msg: str = ""):
    if msg == "":
        with open('./data/16.csv') as f:
            msg = f.read()
            msg = msg[:-1]
    parsed = "".join([hex_to_bin(c) for c in msg])
    return parsed


def hex_to_bin(c: str):
    """len(c) == 1"""
    res = bin((int(c, 16)))[2:]
    return "0" * (4 - len(res)) + res


test = [
    "D2FE28",
    "38006F45291200",
    "EE00D40C823060",
    "8A004A801A8002F478",
    "620080001611562C8802118E34",
    "C0015000016115A2E0802F182340",
    "A0016C880162017C3686B18A3D4780"
]
for hex in test:
    binar = read(hex)
    print(hex, binar)
    p = Packet(binar)
    print(f"String {hex} has version sum {p.version_sum()}")

binaer = read()
p = Packet(binaer)
print(p.compute())

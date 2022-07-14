import csv
import random
from math import trunc


class ALU:
    def __init__(self, vars: dict):
        self.inst = {
                'inp': self.inp,
                'add': self.add,
                'mul': self.mul,
                'div': self.div,
                'mod': self.mod,
                'eql': self.eql,
                }
        self.var = {
                'w': vars['w'],
                'x': vars['x'],
                'y': vars['y'],
                'z': vars['z']
                }
        self.input_stack = []
        self.k = 0

    def in_b(self, b):
        if b in self.var: # Iterates over keys
            return self.var[b]
        else:
            return int(b)

    def inp(self, a: str, b: str = ""):
        self.k = self.k + 1
        print(self.var)
        next_input = int(input("Please provide input:"))
        self.var[a] = next_input
        self.input_stack.append(next_input)

    def add(self, a: str, b: str):
        self.var[a] = self.var[a] + self.in_b(b)

    def mul(self, a: str, b: str):
        self.var[a] = self.var[a] * self.in_b(b)

    def div(self, a: str, b: str):
        self.var[a] = trunc(self.var[a] / self.in_b(b))

    def mod(self, a: str, b: str):
        self.var[a] = self.var[a] % self.in_b(b)

    def eql(self, a: str, b: str):
        self.var[a] = int(self.var[a] == self.in_b(b))


def main():
    print("Hi")
    counts = 0
    program = read()
    # test = [12, 15, 11, -14, 12, -10, 11, 13, -7, 10, -2, -1, -4, -12]
    # test = [12, 15, 11, -14, 12, -10, 11, 13, -7, 10, -2, -1, -4, -13]
    # alu = ALU(test)
    # for p, a, b in program:
    #     alu.inst[p](a, b)
    # print(alu.var)
    # return 0

    alu = ALU()
    ptr = 0
    while ptr < len(program):
        p, a, b = program[ptr]
        ptr += alu.inst[p](a, b)

    print(alu.var)

    # for _ in range(10_000):
    #     inputs = [random.randint(1, 9) for i in range(14)]
    #     alu = ALU(inputs)
    #     for p, a, b in program:
    #         alu.inst[p](a, b)
    #     if alu.var['z'] == 0:
    #         print(f"SOLUTION: {inputs}")
#
# def run_alu(vars: dict, program: list):
#     if not program:
#         return -1
#     alu = ALU(vars)
#     ptr = 0
#     while True:
#         p, a, b = program[ptr]
#         ptr += 1
#         if p == "inp":
#             inpt = alu.inst[p](a, b)
#             whil
#             if inpt == "":
#                 return -1
#
#
#
#             run_alu(alu.var, program[ptr:])
#         alu.inst[p](a, b)

def read():
    with open('./data/24a.csv') as f:
        r = csv.reader(f, delimiter=' ')
        return [tuple(x) for x in r if len(x) == 3]


if __name__ == '__main__':
    main()

# 9 9 9 2 8
# from advent.intcode import IntcodeComputer, ReadTxtOpcode
from itertools import permutations

input = ReadTxtOpcode('inputs/day9.txt')

c = IntcodeComputer(
        memory=input.copy(),
        address=0,
        input_vals=[1],
        relative_base=0,
        debug=False)
while c.status != 'Halted':
    o = c.RunProgram()
    print(o)

c = IntcodeComputer(
        memory=input.copy(),
        address=0,
        input_vals=[2],
        relative_base=0,
        debug=False)
while c.status != 'Halted':
    o = c.RunProgram()
    print(o)
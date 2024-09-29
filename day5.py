from advent.intcode import IntcodeComputer, ReadTxtOpcode

input = ReadTxtOpcode('inputs/day5.txt')

c = IntcodeComputer(input.copy(), 0, 1)
o = c.RunProgram()
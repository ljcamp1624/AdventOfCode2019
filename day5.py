# from advent.intcode import IntcodeComputer, ReadTxtOpcode

input = ReadTxtOpcode('inputs/day5.txt')

c = IntcodeComputer(input.copy(), 0, [1], 0, False)
while True:
    o = c.RunProgram()
    if c.status == 'Halted':
        break
    print(o)
    

c = IntcodeComputer(input.copy(), 0, [5], 0, False)
o = c.RunProgram()
print(o)
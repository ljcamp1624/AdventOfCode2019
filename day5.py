# from advent.intcode import IntcodeComputer, ReadTxtOpcode

input = ReadTxtOpcode('inputs/day5.txt')

c = IntcodeComputer(
        memory=input.copy(),
        address=0,
        input_vals=[1],
        relative_base=0,
        debug=False)
while True:
    o = c.RunProgram()
    if c.status == 'Halted':
        break
    print(o)
    

c = IntcodeComputer(
        memory=input.copy(),
        address=0,
        input_vals=[5],
        relative_base=0,
        debug=False)
o = c.RunProgram()
print(o)
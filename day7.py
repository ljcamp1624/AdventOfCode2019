# from advent.intcode import IntcodeComputer, ReadTxtOpcode
from itertools import permutations

input = ReadTxtOpcode('inputs/day7.txt')

max_output = 0
for n, phase_settings in enumerate(permutations(list(range(5)))):
    computers = list([IntcodeComputer(input.copy(), 0, [p]) for p in list(phase_settings)])
    r = 0
    for i, c in enumerate(computers):
        c.input_vals.append(r)
        r = c.RunProgram()
    max_output = max(max_output, r)
print(max_output)

max_output = 0
for n, phase_settings in enumerate(permutations(list(range(5, 10)))):
    computers = list([IntcodeComputer(input.copy(), 0, [p]) for p in list(phase_settings)])
    r = 0
    break_soon = False
    while True:
        for i, c in enumerate(computers):
            if c.memory[c.address] == 99:
                break_soon = True
                break
            c.input_vals.append(r)
            r = c.RunProgram()
        if break_soon:
            break    
    max_output = max(max_output, r)
print(max_output)
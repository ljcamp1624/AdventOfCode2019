
# from advent.intcode import IntcodeComputer

input = ReadTxtOpcode('inputs/day2.txt')

computer = IntcodeComputer(memory=input.copy())
computer.memory[1] = 12
computer.memory[2] = 2
computer.RunProgram()
print(computer.memory[0])

for noun in range(100):
    for verb in range(100):
        computer = IntcodeComputer(memory=input.copy())
        computer.memory[1] = noun
        computer.memory[2] = verb
        computer.RunProgram()
        if computer.memory[0] == 19690720:
            print(100*noun + verb)
            break
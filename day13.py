from advent.intcode import IntcodeComputer, ReadTxtOpcode

input = ReadTxtOpcode('inputs/day13.txt')

def PrintScreen(objects):
    x = [pos[0] for pos in objects.keys()]
    y = [pos[1] for pos in objects.keys()]
    screen = []
    for j in range(0, max(y)-min(y)+1):
        screen.append([0]*(max(x)-min(x)+1))
    for pos, v in objects.items():
        if v == 0:
            screen[pos[1]][pos[0]] = ' '
        elif v == 1:
            if pos[1] == min(y):
                screen[pos[1]][pos[0]] = '_'
            else:
                screen[pos[1]][pos[0]] = '|'
        elif v == 2:
            screen[pos[1]][pos[0]] = '8'
        elif v == 3:
            screen[pos[1]][pos[0]] = '='
        elif v == 4:
            screen[pos[1]][pos[0]] = 'O'
    for row in screen:
        print(' '.join(row))
    return screen
#%%
c = IntcodeComputer(
        memory=input.copy(),
        address=0,
        input_vals=[],
        relative_base=0,
        debug=False)
objects = {}
while c.status != 'Halted':
    x = c.RunProgram()
    if x is None:
        break
    y = c.RunProgram()
    v = c.RunProgram()
    objects[(x, y)] = v
PrintScreen(objects);
print(sum([v==2 for _, v in objects]))

#%%
c = IntcodeComputer(
        memory=input.copy(),
        address=0,
        input_prompt=True,
        relative_base=0,
        debug=True)
c.memory[0] = 2

objects = {}
while c.status != 'Halted':
    while c.status != 'Waiting for input':
        x = c.RunProgram()
        if c.status != 'Waiting for input':
            break
        elif x == -1:
            _ = c.RunProgram()
            s = c.RunProgram()
        else:
            y = c.RunProgram()
            v = c.RunProgram()
            objects[(x, y)] = v
        if v == 3:
            curr_paddle_x = x
        elif v == 4:
            curr_ball_x = x
    move = curr_ball_x - curr_paddle_x
    if move == 0:
        c.manual_input = 0
    elif move > 0:
        c.manual_input = 1
    elif move < 0:
        c.manual_input = -1
    PrintScreen(objects);
    print(s)
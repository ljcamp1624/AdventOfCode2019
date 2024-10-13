from advent.intcode import IntcodeComputer, ReadTxtOpcode

input = ReadTxtOpcode('inputs/day11.txt')

def TurnDir(dir, ang=0):
    if ang==0:
        return dir
    elif ang==90:
        return (dir[1], -dir[0])
    elif ang==-90:
        return (-dir[1], dir[0])

def TakeStep(pos, dir):
    return (pos[0]+dir[0], pos[1]+dir[1])

c = IntcodeComputer(
        memory=input.copy(),
        address=0,
        input_vals=[0],
        relative_base=0,
        debug=False)

paint={}
painted=set()
curr_pos = (0,0)
curr_dir = (0,1)
k = 1
count = 0
while c.status != 'Halted':
    o = c.RunProgram()
    if o is None:
        break
    if k == 1:
        if curr_pos not in paint.keys():
            paint[curr_pos] = 0
        if o != paint[curr_pos]:
            painted.add(curr_pos)
        paint[curr_pos] = o
        k = 2
    elif k == 2:
        if o == 0:
            ang = 90
        elif o == 1:
            ang = -90
        curr_dir = TurnDir(curr_dir, ang)
        curr_pos = TakeStep(curr_pos, curr_dir)
        if curr_pos not in paint.keys():
            paint[curr_pos] = 0
        c.input_vals.append(paint[curr_pos])
        k = 1
print(len(painted))

c = IntcodeComputer(
        memory=input.copy(),
        address=0,
        input_vals=[1],
        relative_base=0,
        debug=False)

paint={}
painted=set()
curr_pos = (0,0)
curr_dir = (0,1)
k = 1
count = 0
while c.status != 'Halted':
    o = c.RunProgram()
    if o is None:
        break
    if k == 1:
        if curr_pos not in paint.keys():
            paint[curr_pos] = 0
        if o != paint[curr_pos]:
            painted.add(curr_pos)
        paint[curr_pos] = o
        k = 2
    elif k == 2:
        if o == 0:
            ang = 90
        elif o == 1:
            ang = -90
        curr_dir = TurnDir(curr_dir, ang)
        curr_pos = TakeStep(curr_pos, curr_dir)
        if curr_pos not in paint.keys():
            paint[curr_pos] = 0
        c.input_vals.append(paint[curr_pos])
        k = 1

y = [x[0] for x in paint.keys()]
x = [x[1] for x in paint.keys()]
output=[]
for i in range(0, max(x)-min(x)+1):
    output.append(['.']*(max(y)-min(y)+1))
for k, v in paint.items():
    if v == 1:
        output[k[1]-min(x)][k[0]-min(y)] = '#'
for o in output[::-1]:
    print(''.join(o[::-1]))
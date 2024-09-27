from advent.tools import ReadTxt

def BuildPath(path):
    out = [(0,0)]
    for p in path:
        d = p[0]
        n = int(p[1:])
        if d == 'U':
            out.append((out[-1][0], out[-1][1] + n))
        elif d == 'D':
            out.append((out[-1][0], out[-1][1] - n))
        elif d == 'R':
            out.append((out[-1][0] + n, out[-1][1]))
        elif d == 'L':
            out.append((out[-1][0] - n, out[-1][1]))
    return out

def AxisCross(a1, a2, b1, b2):
    if (a1 == a2) and ((b1 < a1) and (b2 > a1)) or ((b1 > a1) and (b2 < a1)):
        return a1
    elif (b1 == b2) and ((a1 < b1) and (a2 > b1)) or ((a1 > b1) and (a2 < b1)):
        return b1
    else:
        return None

def GetIntersections(coords1, coords2):
    intersections = []
    for c1, c2 in zip(coords1[:-1], coords1[1:]):
        for d1, d2 in zip(coords2[:-1], coords2[1:]):
            x1, x2, y1, y2 = c1[0], c2[0], c1[1], c2[1]
            i1, i2, j1, j2 = d1[0], d2[0], d1[1], d2[1]
            x = AxisCross(x1, x2, i1, i2)
            y = AxisCross(y1, y2, j1, j2)
            if x and y:
                if (x,y) not in intersections:
                    intersections.append((x,y))
    return intersections

def CheckCross(x, y, x1, x2, y1, y2):
    if min(x1, x2) < x and max(x1, x2) > x and (y == y1) and (y == y2):
        return True, 0
    elif min(y1, y2) < y and max(y1, y2) > y and (x == x1) and (x == x2):
        return True, 1
    else:
        return False, None
        
path1 = ReadTxt('inputs/day3_path1.txt')[0][0].split(',')
path2 = ReadTxt('inputs/day3_path2.txt')[0][0].split(',')
coords1 = BuildPath(path1)
coords2 = BuildPath(path2)
intersections = GetIntersections(coords1, coords2)

# Closest to center
dist = 999999999
for i in intersections:
    dist = min(dist, abs(i[0]) + abs(i[1]))
print(dist)

# Closest by time
time = 999999999
for i in intersections:
    t1 = 0
    for c1, c2 in zip(coords1[:-1], coords1[1:]):
        h, a = CheckCross(i[0], i[1], c1[0], c2[0], c1[1], c2[1])
        if h:
            if a == 0:
                t1 += abs(i[0] - c1[0])
            elif a == 1:
                t1 += abs(i[1] - c1[1])
            break
        elif not h:
            t1 += abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])
    t2 = 0
    for c1, c2 in zip(coords2[:-1], coords2[1:]):
        h, a = CheckCross(i[0], i[1], c1[0], c2[0], c1[1], c2[1])
        if h:
            if a == 0:
                t2 += abs(i[0] - c1[0])
            elif a == 1:
                t2 += abs(i[1] - c1[1])
            break
        elif not h:
            t2 += abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])
    time = min(time, t1 + t2)
print(time)
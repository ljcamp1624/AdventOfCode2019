from advent.tools import ReadTxt

def GetFuel(mass):
    return max(mass // 3 - 2, 0)
    
def GetFuelRecursive(mass):
    total_fuel = 0
    fuel = mass
    while fuel > 0:
        fuel = GetFuel(fuel)
        total_fuel += fuel
    return total_fuel

mass = ReadTxt('inputs/q1.txt')[0]
fuel = sum([GetFuel(int(m)) for m in mass])
print('part 1: ', fuel)
fuel = sum([GetFuelRecursive(int(m)) for m in mass])
print('part 2: ', fuel)
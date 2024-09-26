from advent.tools import ReadTxt

def ReadTxtOpcode(file_name):
    return [int(n) for n in ReadTxt(file_name)[0][0].split(',')]

class IntcodeComputer():
    
    def __init__(self, memory=[], address=0):
        self.memory = memory
        self.address = address
    
    def RunProgram(self):
        try:
            self.Execute()
        except:
            print('Failure at memory address: ' + str(self.address))
        
    def Execute(self):
        while True:
            opcode = self.memory[self.address]
            if opcode == 99:
                return None
            elif opcode in [1, 2]:
                params = self.memory[(self.address+1):(self.address + 4)]
                self.address += 4
                self.RunOpcode(opcode, params)
            else:
                raise Exception('Unrecognized Opcode: ' + opcode)
    
    def RunOpcode(self, opcode=None, params=None):
        if not opcode or not params:
            raise Exception('No Opcode Params')
        if opcode == 1:
            self.memory[params[2]] = self.memory[params[0]]+self.memory[params[1]]
        elif opcode == 2:
            self.memory[params[2]] = self.memory[params[0]]*self.memory[params[1]]
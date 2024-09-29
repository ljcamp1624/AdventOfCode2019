from advent.tools import ReadTxt

def ReadTxtOpcode(file_name):
    return [int(n) for n in ReadTxt(file_name)[0][0].split(',')]

class IntcodeComputer():
    
    def __init__(self, memory=[], address=0, input_vals=[], debug=False):
        self.memory = memory
        self.address = address
        self.input_vals = input_vals
        self.debug = debug
        
    def ProcessOpcode(self, full_opcode):
        opcode = full_opcode % 100
        param_modes = (full_opcode - (full_opcode % 100)) // 100
        param_modes = [((param_modes - (param_modes % x)) // x) % 10 for x in [1, 10, 100]]
        return opcode, param_modes
    
    def ProcessParameters(self, opcode, params, param_modes):
        param_idx = []
        if opcode in [1, 2, 5, 6, 7, 8]:
            param_idx = [0, 1]
        elif opcode == 3:
            return params
        elif opcode == 4:
            param_idx = [0]
        for i in param_idx:
            if param_modes[i] == 0:
                params[i] = self.memory[params[i]]
            elif param_modes[i] == 1:
                params[i] = params[i]
            else:
                raise Exception('Unrecognized param mode')
        return params
        
    def RunProgram(self):
        while True:
            
            # Process the full opcode
            full_opcode = self.memory[self.address]
            opcode, param_modes = self.ProcessOpcode(full_opcode)
            
            # Compute the delta for each opcode and grab parameters
            delta = 0
            if opcode == 99:
                return None
            elif opcode in [1, 2, 7, 8]:
                delta = 4
            elif opcode in [3, 4]:
                delta = 2
            elif opcode in [5, 6]:
                delta = 3
            else:
                raise Exception('Unrecognized Opcode ' + str(opcode) + ' at memory address ' + str(self.address))
            params = self.memory[(self.address+1):(self.address+delta)]
            param_modes = param_modes[:len(params)]

            # Update parameters according to paramater modes
            params = self.ProcessParameters(opcode, params, param_modes)
            
            # Debug
            if self.debug:
                print(self.address, full_opcode, opcode, params, param_modes)
            
            # Run opcode
            self.address += delta
            output = self.RunOpcode(opcode, params)
            if output is not None:
                return output
            
    def RunOpcode(self, opcode=None, params=None):
        if not opcode or not params:
            raise Exception('No Opcode or Params or Param Modes')
        
        if opcode == 1:
            self.memory[params[2]] = params[0] + params[1]

        elif opcode == 2:
            self.memory[params[2]] = params[0] * params[1]

        elif opcode == 3:
            if len(self.input_vals) == 0:
                raise Exception('No input value at memory address ' + str(self.address))
            self.memory[params[0]] = self.input_vals.pop(0)

        elif opcode == 4:
            return params[0]

        elif opcode == 5:
            if params[0]:
                self.address = params[1]

        elif opcode == 6:
            if not params[0]:
                self.address = params[1]
                    
        elif opcode == 7:
            if params[0] < params[1]:
                self.memory[params[2]] = 1
            else:
                self.memory[params[2]] = 0
                
        elif opcode == 8:
            if params[0] == params[1]:
                self.memory[params[2]] = 1
            else:
                self.memory[params[2]] = 0
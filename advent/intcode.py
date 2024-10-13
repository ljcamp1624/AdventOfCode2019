from advent.tools import ReadTxt

def ReadTxtOpcode(file_name):
    return [int(n) for n in ReadTxt(file_name)[0][0].split(',')]

class IntcodeComputer():
    
    def __init__(self, memory=[], address=0, input_vals=[], relative_base=0, debug=False):
        self.memory = memory
        self.address = address
        self.input_vals = input_vals
        self.relative_base = relative_base
        self.status = 'Waiting'
        self.debug = debug
        
    def ProcessOpcode(self, full_opcode):
        opcode = full_opcode % 100
        param_modes = (full_opcode - (full_opcode % 100)) // 100
        param_modes = [((param_modes - (param_modes % x)) // x) % 10 for x in [1, 10, 100]]
        return opcode, param_modes
    
    def ProcessInputParameters(self, opcode, params, param_modes):
        # Set the indices for input parameters based on opcode
        param_idx = []
        if opcode in [1, 2, 5, 6, 7, 8]:
            param_idx = [0, 1]
        elif opcode == 3:
            return params
        elif opcode in (4, 9):
            param_idx = [0]
        desc = 'Input parameters transformed from ' + str([params[i] for i in param_idx])
        # Transform input indices based on param modes
        for i in param_idx:
            if param_modes[i] == 0:
                params[i] = self.GetFromMemory([params[i]])[0]
            elif param_modes[i] == 1:
                params[i] = params[i]
            elif param_modes[i] == 2:
                params[i] = self.GetFromMemory([params[i] + self.relative_base])[0]
            else:
                raise Exception('Unrecognized parameter mode')
        desc += ' to ' + str([params[i] for i in param_idx])
        if self.debug:
            # Print description in debug mode
            print('\t'+desc)
        return params
    
    def ProcessOutputParameters(self, opcode, params, param_modes):
        # Set the indices for output parameters based on opcode
        param_idx = []
        if opcode in [1, 2, 7, 8]:
            param_idx = [2]
        elif opcode in [3]:
            param_idx = [0]
        elif opcode in (4, 9, 5, 6):
            return params
        desc = 'Output parameters transformed from ' + str([params[i] for i in param_idx])
        # Transform output indices based on param modes
        for i in param_idx:
            if param_modes[i] == 0:
                params[i] = params[i]
            elif param_modes[i] == 1:
                raise Exception('Invalid param mode for output parameter')
            elif param_modes[i] == 2:
                params[i] = params[i] + self.relative_base
            else:
                raise Exception('Unrecognized parameter mode')
        desc += ' to ' + str([params[i] for i in param_idx])
        if self.debug:
            # Print description in debug mode
            print('\t'+desc)
        return params
    
    def GetFromMemory(self, indices):
        out = []
        for i in indices:
            if i >= len(self.memory):
                out.append(0)
            else:
                out.append(self.memory[i])
        return out
    
    def AssignToMemory(self, index, value):
        if index >= len(self.memory):
            extra = index - len(self.memory) + 1
            self.memory += [0]*extra
        self.memory[index] = value

    def RunProgram(self):
        while True:
            
            # Process the full opcode
            self.status = 'Running'
            full_opcode = self.memory[self.address]
            opcode, param_modes = self.ProcessOpcode(full_opcode)
            
            # Compute the delta for each opcode and grab parameters
            delta = 0
            if opcode == 99:
                self.status = 'Halted'
                return None
            elif opcode in [1, 2, 7, 8]:
                delta = 4
            elif opcode in [3, 4, 9]:
                delta = 2
            elif opcode in [5, 6]:
                delta = 3
            else:
                raise Exception('Unrecognized Opcode ' + str(opcode) + ' at memory address ' + str(self.address))
            
            # Extend memory if needed
            params = self.GetFromMemory(list(range(self.address+1, self.address+delta)))
            param_modes = param_modes[:len(params)]
            
            # Debug
            if self.debug:
                print('Address: {}; Opcode: {}; Param Modes: {}; Params: {};'.format(self.address, full_opcode, param_modes, params))

            # Update parameters according to paramater modes
            params = self.ProcessInputParameters(opcode, params, param_modes)
            params = self.ProcessOutputParameters(opcode, params, param_modes)
            
            # Run opcode
            self.address += delta
            output = self.RunOpcode(opcode, params)
            if output is not None:
                self.status = 'Waiting'
                return output
            
    def RunOpcode(self, opcode=None, params=None, address_delta=0):
        return_val = None
        if not opcode or not params:
            raise Exception('No Opcode or Params or Param Modes')
        
        if opcode == 1:
            val = params[0] + params[1]
            self.AssignToMemory(params[2], val)
            desc1 = '{} + {} = {}'.format(params[0], params[1], val)
            desc2 = 'Memory at address {} set to {}.'.format(params[2], val)

        elif opcode == 2:
            val = params[0] * params[1]
            self.AssignToMemory(params[2], val)
            desc1 = '{} * {} = {}'.format(params[0], params[1], val)
            desc2 = 'Memory at address {} set to {}.'.format(params[2], val)

        elif opcode == 3:
            if len(self.input_vals) == 0:
                raise Exception('No input value at memory address ' + str(self.address))
            val = self.input_vals.pop(0)
            self.AssignToMemory(params[0], val)
            desc1 = 'Grabbed {} from inputs.'.format(val)
            desc2 = 'Memory at address {} set to {}.'.format(params[0], val)

        elif opcode == 4:
            desc1 = 'Assign {} as output.'.format(params[0])
            desc2 = 'Returned value {}.'.format(params[0])
            return_val = params[0]

        elif opcode == 5:
            desc1 = 'Checking {} == 1.'.format(params[0])
            desc2 = 'No action taken.'
            if params[0]:
                self.address = params[1]
                desc2 = 'Address set to {}'.format(params[1])

        elif opcode == 6:
            desc1 = 'Checking {} == 0.'.format(params[0])
            desc2 = 'No action taken.'
            if not params[0]:
                self.address = params[1]
                desc2 = 'Address set to {}'.format(params[1])
                    
        elif opcode == 7:
            desc1 = 'Checking {} < {}.'.format(params[0], params[1])
            if params[0] < params[1]:
                val = 1
            else:
                val = 0
            self.AssignToMemory(params[2], val)
            desc2 = 'Memory at address {} set to {}.'.format(params[2], val)
                
        elif opcode == 8:
            desc1 = 'Checking {} == {}.'.format(params[0], params[1])
            if params[0] == params[1]:
                val = 1
            else:
                val = 0
            self.AssignToMemory(params[2], val)
            desc2 = 'Memory at address {} set to {}.'.format(params[2], val)
                
        elif opcode == 9:
            desc1 = None
            desc2 = 'Relative base updated from {} to {}.'.format(self.relative_base, params[0])
            self.relative_base += params[0]
            
        if self.debug:
            if desc1:
                print('\tOperation: '+desc1)
            if desc2:
                print('\tResult: '+desc2)
        
        if return_val is not None:
            return return_val
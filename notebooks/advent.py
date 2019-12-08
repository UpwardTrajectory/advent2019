def opcode(raw_code):
    """Convert an opcode: ABCDE into {code, param_count, [modes]}
    
    Will auto-adjust the param_count and length of modes based
    on the dictionary param_counts
    
    ex) ABCDE  --  if DE is either 01 or 02:
    {
    'code': DE, 
    'param_count': 3, 
    'modes': [C, B, A],
    }
    """
    filled_code = str(raw_code).zfill(5)
    
    param_counts = {
        1: 3, 
        2: 3, 
        3: 1, 
        4: 1, 
        99: 0
    }
    
    # split @ 2 from right side, then reverse everything left of split
    modes = filled_code[:-2][::-1]
    code = int(filled_code[-2:])
    count = param_counts[code]
    
    modes = [int(x) for x in modes[:count]] 
    
    return {'code': code, 'param_count': count, 'modes': modes}


def modeify(intcode, i):
    """Apply a mode to a parameter"""
    j = i + 1
    _opcode = opcode(intcode[i])
    params = intcode[j: j + _opcode['param_count']]
    modes = _opcode['modes']#[:-1]
    
    mode_covert = {
        0: lambda x: intcode[x],    # position mode
        1: lambda x: x              # immediate mode
    }
    
    output = [mode_covert[mode](param) for mode, param in zip(modes, params)]
    #output.append(intcode[i + _opcode['param_count']])
    return output

def get_new_pos(intcode, mode, i, delta_i):
    if mode == 0:
        return intcode[i + delta_i]
    elif mode == 1:
        return i + delta_i
    
            
            
def single_code(intcode, i, halt=False, verbose=False):
    """Process a single intstruction from intcode
    
    return the same format we started with:
    (intcode, i, halt_status)
    """    
    _opcode = opcode(intcode[i])
    code = _opcode['code']
    modes = _opcode['modes']
    
    args = modeify(intcode, i)
    
    if verbose:
        print('params', intcode[i+1: i+1+_opcode['param_count']])
        print('modes', ['pos' if x is 0 else 'imm' for x in _opcode['modes']])
        print('args', args)
    
    if code == 99:
        return intcode, i, True
    elif code == 1:
        new_pos = get_new_pos(intcode, modes[-1], i, 3)
        new_value = sum(args[:-1])
    elif code == 2:
        new_pos = get_new_pos(intcode, modes[-1], i, 3)
        new_value = args[0] * args[1]
    elif code == 3:
        new_pos = get_new_pos(intcode, modes[-1], i, 1)
        new_value = int(input('Get this party started with input:'))
    elif code == 4:
        new_pos = get_new_pos(intcode, modes[-1], i, 1)
        print('THIS SHOULD BE ZERO (unless final output):', intcode[new_pos])
    
    if code != 4:
        intcode[new_pos] = new_value
        if verbose:
            print(f'updating intcode[{new_pos}] to {intcode[new_pos]}')
    
    i += _opcode['param_count'] + 1
    
    return intcode, i, halt


def run(intcode, i=0, halt=False, verbose=False):
    while not halt:
        if verbose:
            print('-----------------------------')
            print(f'pos {i} is code {intcode[i]}')
        intcode, i, halt = single_code(intcode, i, halt, verbose)
        
    if verbose:
        print('*************************')   
        print(f'halted at i = {i}')
        print('*************************')
        print()
    return intcode

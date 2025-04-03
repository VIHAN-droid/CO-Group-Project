def R_type(inst):
    ins = inst[1]
    rd = int(inst[2], 2)
    rs2 = int(inst[3], 2)
    rs1 = int(inst[4], 2)
    result = 0
    if ins == 'add':
        result = register[f'x{rs1}'] + register[f'x{rs2}']
    elif ins == 'sub':
        result = register[f'x{rs1}'] - register[f'x{rs2}']
    elif ins == 'or':
        result = register[f'x{rs1}'] | register[f'x{rs2}']
    elif ins == 'and':
        result = register[f'x{rs1}'] & register[f'x{rs2}']
    elif ins == 'slt':
        result = 1 if register[f'x{rs1}'] < register[f'x{rs2}'] else 0
    elif ins == 'srl':
        result = (register[f'x{rs1}'] % (1 << 32)) >> (register[f'x{rs2}'] & 0x1F)
    if rd != 0:
        register[f'x{rd}'] = result
    register['PC'] += 4

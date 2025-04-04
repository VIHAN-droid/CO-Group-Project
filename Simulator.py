import sys

func3 = {
    "000": ["add", "sub", "addi", "jalr", "beq"],
    "010": ["slt", "lw", "sw"],
    "101": ["srl"],
    "110": ["or"],
    "111": ["and"],
    "001": ["bne"]
}

func7 = {
    "0000000": ["add", "slt", "srl", "or", "and"],
    "0100000": ["sub"]
}

opcode = {
    "0110011": ["add", "sub", "slt", "srl", "or", "and"],
    "0000011": ["lw"],
    "0010011": ["addi"],
    "1100111": ["jalr"],
    "0100011": ["sw"],
    "1100011": ["beq", "bne"],
    "1101111": ["jal"]
}

register = {
    'PC': 0, 'x0': 0, 'x1': 0, 'x2': 380, 'x3': 0, 'x4': 0, 'x5': 0, 'x6': 0, 'x7': 0,
    'x8': 0, 'x9': 0, 'x10': 0, 'x11': 0, 'x12': 0, 'x13': 0, 'x14': 0, 'x15': 0,
    'x16': 0, 'x17': 0, 'x18': 0, 'x19': 0, 'x20': 0, 'x21': 0, 'x22': 0, 'x23': 0,
    'x24': 0, 'x25': 0, 'x26': 0, 'x27': 0, 'x28': 0, 'x29': 0, 'x30': 0, 'x31': 0
}

memory_32_bit = {
    "0x00010000": "0b00000000000000000000000000000000",
    "0x00010004": "0b00000000000000000000000000000000",
    "0x00010008": "0b00000000000000000000000000000000",
    "0x0001000C": "0b00000000000000000000000000000000",
    "0x00010010": "0b00000000000000000000000000000000",
    "0x00010014": "0b00000000000000000000000000000000",
    "0x00010018": "0b00000000000000000000000000000000",
    "0x0001001C": "0b00000000000000000000000000000000",
    "0x00010020": "0b00000000000000000000000000000000",
    "0x00010024": "0b00000000000000000000000000000000",
    "0x00010028": "0b00000000000000000000000000000000",
    "0x0001002C": "0b00000000000000000000000000000000",
    "0x00010030": "0b00000000000000000000000000000000",
    "0x00010034": "0b00000000000000000000000000000000",
    "0x00010038": "0b00000000000000000000000000000000",
    "0x0001003C": "0b00000000000000000000000000000000",
    "0x00010040": "0b00000000000000000000000000000000",
    "0x00010044": "0b00000000000000000000000000000000",
    "0x00010048": "0b00000000000000000000000000000000",
    "0x0001004C": "0b00000000000000000000000000000000",
    "0x00010050": "0b00000000000000000000000000000000",
    "0x00010054": "0b00000000000000000000000000000000",
    "0x00010058": "0b00000000000000000000000000000000",
    "0x0001005C": "0b00000000000000000000000000000000",
    "0x00010060": "0b00000000000000000000000000000000",
    "0x00010064": "0b00000000000000000000000000000000",
    "0x00010068": "0b00000000000000000000000000000000",
    "0x0001006C": "0b00000000000000000000000000000000",
    "0x00010070": "0b00000000000000000000000000000000",
    "0x00010074": "0b00000000000000000000000000000000",
    "0x00010078": "0b00000000000000000000000000000000",
    "0x0001007C": "0b00000000000000000000000000000000"
}

memory_dec = {
    "0x00010000": "0", "0x00010004": "0", "0x00010008": "0", "0x0001000C": "0",
    "0x00010010": "0", "0x00010014": "0", "0x00010018": "0", "0x0001001C": "0",
    "0x00010020": "0", "0x00010024": "0", "0x00010028": "0", "0x0001002C": "0",
    "0x00010030": "0", "0x00010034": "0", "0x00010038": "0", "0x0001003C": "0",
    "0x00010040": "0", "0x00010044": "0", "0x00010048": "0", "0x0001004C": "0",
    "0x00010050": "0", "0x00010054": "0", "0x00010058": "0", "0x0001005C": "0",
    "0x00010060": "0", "0x00010064": "0", "0x00010068": "0", "0x0001006C": "0",
    "0x00010070": "0", "0x00010074": "0", "0x00010078": "0", "0x0001007C": "0"
}

key_list = [
    "0x00010000", "0x00010004", "0x00010008", "0x0001000C",
    "0x00010010", "0x00010014", "0x00010018", "0x0001001C",
    "0x00010020", "0x00010024", "0x00010028", "0x0001002C",
    "0x00010030", "0x00010034", "0x00010038", "0x0001003C",
    "0x00010040", "0x00010044", "0x00010048", "0x0001004C",
    "0x00010050", "0x00010054", "0x00010058", "0x0001005C",
    "0x00010060", "0x00010064", "0x00010068", "0x0001006C",
    "0x00010070", "0x00010074", "0x00010078", "0x0001007C"
]

def decoder(binary_text):
    new_binary = binary_text[::-1]
    func_3 = new_binary[12:15][::-1]
    op_code = new_binary[0:7][::-1]
    if op_code == "0110011":  
        ins_type = "R"
        func_7 = new_binary[25:32][::-1]
        rs2 = new_binary[20:25][::-1]
        rs1 = new_binary[15:20][::-1]
        rd = new_binary[7:12][::-1]
        if func_3 == "000" and func_7 == "0000000":
            return [ins_type, "add", rd, rs2, rs1]
        elif func_3 == "000" and func_7 == "0100000":
            return [ins_type, "sub", rd, rs2, rs1]
        elif func_3 == "010" and func_7 == "0000000":
            return [ins_type, "slt", rd, rs2, rs1]
        elif func_3 == "101" and func_7 == "0000000":
            return [ins_type, "srl", rd, rs2, rs1]
        elif func_3 == "110" and func_7 == "0000000":
            return [ins_type, "or", rd, rs2, rs1]
        elif func_3 == "111" and func_7 == "0000000":
            return [ins_type, "and", rd, rs2, rs1]
    elif op_code == "0000011":  
        ins_type = "I"
        rd = new_binary[7:12][::-1]
        rs1 = new_binary[15:20][::-1]
        imm = new_binary[20:32][::-1]
        return [ins_type, "lw", rd, imm, rs1]
    elif op_code == "0010011":  
        ins_type = "I"
        rd = new_binary[7:12][::-1]
        rs1 = new_binary[15:20][::-1]
        imm = new_binary[20:32][::-1]
        return [ins_type, "addi", rd, imm, rs1]
    elif op_code == "1100111":  
        ins_type = "I"
        rd = new_binary[7:12][::-1]
        rs1 = new_binary[15:20][::-1]
        imm = new_binary[20:32][::-1]
        return [ins_type, "jalr", rd, imm, rs1]
    elif op_code == "0100011":  
        ins_type = "S"
        rs2 = new_binary[20:25][::-1]
        rs1 = new_binary[15:20][::-1]
        imm_front = new_binary[25:32][::-1]
        imm_back = new_binary[7:12][::-1]
        imm = imm_front + imm_back
        return [ins_type, "sw", rs2, imm, rs1]
    elif op_code == "1100011":  
        ins_type = "B"
        rs2 = new_binary[20:25][::-1]
        rs1 = new_binary[15:20][::-1]
        imm_11 = new_binary[7:8][::-1]
        imm_4_1 = new_binary[8:12][::-1]
        imm_10_5 = new_binary[25:31][::-1]
        imm_12 = new_binary[31:32][::-1]
        imm = imm_12 + imm_11 + imm_10_5 + imm_4_1 + "0"
        if func_3 == "000":
            return [ins_type, "beq", rs2, rs1, imm]
        elif func_3 == "001":
            return [ins_type, "bne", rs2, rs1, imm]
    elif op_code == "1101111":  # J-type (jal)
        ins_type = "J"
        rd = new_binary[7:12][::-1]
        imm_20 = new_binary[31:32][::-1]
        imm_10_1 = new_binary[21:31][::-1]
        imm_11 = new_binary[20:21][::-1]
        imm_19_12 = new_binary[12:20][::-1]
        imm = imm_20 + imm_19_12 + imm_11 + imm_10_1 + "0"
        return [ins_type, "jal", rd, imm]
    return None
    
def twos_complement(bin_str, num_bits):
    if bin_str.startswith('0b'):
        bin_str = bin_str[2:]
    if len(bin_str) < num_bits:
        bin_str = bin_str.zfill(num_bits)
    if len(bin_str) > num_bits:
        bin_str = bin_str[-num_bits:]
    value = int(bin_str, 2)
    if bin_str[0] == '1':
        value -= (1 << num_bits)
    return value

def int_to_hex(n, width=8):
    return f"0x{n:0{width}X}"

def int_to_32bit_bin(n):
    return f"0b{n & 0xFFFFFFFF:032b}"

def b_type_adjustment(a):
    rs1 = int(a[3], 2)
    rs2 = int(a[2], 2)
    imm = twos_complement(a[4], 13)
    if a[1] == 'beq':
        if rs1 == 0 and rs2 == 0 and imm == 0:
            return True
        if register[f'x{rs1}'] == register[f'x{rs2}']:
            register['PC'] += imm
        else:
            register['PC'] += 4
    else:
        if register[f'x{rs1}'] != register[f'x{rs2}']:
            register['PC'] += imm
        else:
            register['PC'] += 4
    return False

def jal_operation(a):
    rd = int(a[2], 2)
    imm = twos_complement(a[3], 21)
    if rd != 0:
        register[f'x{rd}'] = register['PC'] + 4
    register['PC'] += imm

def jalr_operation(a):
    rd = int(a[2], 2)
    rs1 = int(a[4], 2)
    imm = twos_complement(a[3], 12)
    target = (register[f'x{rs1}'] + imm) & ~1
    if rd != 0:
        register[f'x{rd}'] = register['PC'] + 4
    register['PC'] = target
    
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
    
def S_Type(lst):
    rs2 = int(lst[2], 2)
    imm = twos_complement(lst[3], 12)
    rs1 = int(lst[4], 2)
    base_value = register[f'x{rs1}']
    final_address = base_value + imm
    final_address_hex = int_to_hex(final_address)
    memory_32_bit[final_address_hex] = int_to_32bit_bin(register[f'x{rs2}'])
    memory_dec[final_address_hex] = str(register[f'x{rs2}'])
    register['PC'] += 4
    
def lw(lst):
    rd = int(lst[2], 2)
    imm = twos_complement(lst[3], 12)
    rs1 = int(lst[4], 2)
    base_value = register[f'x{rs1}']
    final_address = base_value + imm
    final_address_hex = int_to_hex(final_address)
    if final_address_hex in memory_dec:
        register[f'x{rd}'] = int(memory_dec[final_address_hex])
    register['PC'] += 4

# if len(sys.argv) != 3:
#     sys.exit(1)
input_filename = sys.argv[1]
output_filename = sys.argv[2]
with open(input_filename, "r") as file:
    instructions = [line.strip() for line in file]
    list_integer = []
    list_binary = []
    instruction_count = len(instructions)
    register['PC'] = 0

    while 0 <= register['PC'] // 4 < instruction_count:
        current_pc = register['PC']
        line = instructions[register['PC'] // 4]
        decoded = decoder(line)
        if not decoded:
            register['PC'] += 4
            continue

        halt = False
        if decoded[0] == 'R':
            R_type(decoded)
        elif decoded[0] == 'J':
            jal_operation(decoded)
        elif decoded[0] == 'B':
            halt = b_type_adjustment(decoded)
        elif decoded[0] == 'S':
            S_Type(decoded)
        elif decoded[0] == 'I':
            if decoded[1] == 'lw':
                lw(decoded)
            elif decoded[1] == 'addi':
                rd = int(decoded[2], 2)
                rs1 = int(decoded[4], 2)
                imm = twos_complement(decoded[3], 12)
                if rd != 0:
                    register[f'x{rd}'] = register[f'x{rs1}'] + imm
                register['PC'] += 4
            elif decoded[1] == 'jalr':
                jalr_operation(decoded)

        l3 = [register[reg] for reg in register]
        l4 = [int_to_32bit_bin(register[reg]) for reg in register]
        list_integer.append(l3)
        list_binary.append(l4)

        if halt:
            break

    with open(output_filename, "w") as output_file:
        for state in list_binary:
            output_file.write(" ".join(state) + "\n")
        for addr, value in memory_32_bit.items():
            if addr in key_list:
                output_file.write(f"{addr}:{value}\n")

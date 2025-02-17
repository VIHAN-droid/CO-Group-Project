R_type = ['add','sub','slt','sltu','xor','sll','srl','or','and'] 
I_type = ['lw','addi','sltiu','jalr']
S_type = ['sw']
B_type = ['beq','bne','blt','bge','bltu','bgeu']
U_type = ['lui','auipc']
J_type = ['jal']
Bonus = ['mul','rst','halt','rvrs']

register = {
    'zero': '00000',
    'ra':   '00001',
    'sp':   '00010',
    'gp':   '00011',
    'tp':   '00100',
    't0':   '00101',
    't1':   '00110',
    't2':   '00111',
    's0':   '01000',
    's1':   '01001',
    'a0':   '01010',
    'a1':   '01011',
    'a2':   '01100',
    'a3':   '01101',
    'a4':   '01110',
    'a5':   '01111',
    'a6':   '10000',
    'a7':   '10001',
    's2':   '10010',
    's3':   '10011',
    's4':   '10100',
    's5':   '10101',
    's6':   '10110',
    's7':   '10111',
    's8':   '11000',
    's9':   '11001',
    's10':   '11010',
    's11':   '11011',
    't3':   '11100',
    't4':   '11101',
    't5':   '11110',
    't6':   '11111',
}


func3 = {'add': '000',
    'sub': '000',
    'sll': '001',
    'slt': '010',
    'sltu': '011',
    'xor': '100',
    'srl': '101',
    'or': '110',
    'and': '111',
    'lw': '010',
    'addi': '000',
    'sltiu': '011',
    'jalr': '000',
    'sw': '010',
    'beq': '000',
    'bne': '001',
    'blt': '100',
    'bge': '101',
    'bltu': '110',
    'bgeu': '111'
}

func7 = {
    "add": "0000000", 
    "sub": "0100000", 
    "sll": "0000000", 
    "slt": "0000000", 
    "sltu": "0000000",
    "xor": "0000000",
    "srl": "0000000", 
    "sra": "0100000", 
    "or": "0000000",
    "and": "0000000"
}

opcode = {"add": "0110011", "sub": "0110011", "sll": "0110011", "slt": "0110011", "sltu": "0110011",
        "xor": "0110011", "srl": "0110011", "sra": "0110011", "or": "0110011","and": "0110011", "lw":"0000011", "addi":"0010011", 
        "jalr":"1100111", "sw":"0100011", "beq":"1100011"}

def R_identify(text):
    space_split = text.split(" ", 1)  # Split only at the first space to separate label
    if len(space_split) == 2 and space_split[0] not in func7:  # If there's a label
        text = space_split[1]  # Remove the label and process the instruction
    
    space_split = text.split(" ")
    ops = space_split[0]
    comma_split = text.split(",")

    if len(comma_split) != 3:
        return "error"
    
    rd = comma_split[0].split(" ")[1].strip()
    rs1 = comma_split[1].strip()
    rs2 = comma_split[2].strip()
    
    if rd not in register or rs1 not in register or rs2 not in register:
        return "error"
    
    binary_pattern = (
        func7[ops] +" "+ register[rs2]+" " + register[rs1] + " " + func3[ops] +" " + register[rd] + " " + opcode[ops]
    )
    
    return binary_pattern

# print(R_identify("add a0, a1, a2"))


# ..............................................................................................................................................}

def two_complement(num, bits):
    if num<0:
        num = (1 << bits) + num 
    return str(format(num, f"0{bits}b"))

def I_identify(text):
    space_split = text.split()
    
    # Check if there's a label
    if space_split[1] in func3:  # Assuming func3 contains valid instruction mnemonics
        ops = space_split[1]  # Instruction mnemonic
        instr_part = " ".join(space_split[1:])  # Extract the instruction part
    else:
        ops = space_split[0]  # Instruction mnemonic without label
        instr_part = text  # Full instruction if no label
    
    comma_split = instr_part.split(",")
    if len(comma_split) != 2:
        return "error"
    
    rd = comma_split[0].split(" ")[1].strip()
    imm_rs1_split = comma_split[1].strip().split("(")
    
    if len(imm_rs1_split) != 2:
        return "error"
    
    immediate_val = imm_rs1_split[0].strip()
    rs1 = imm_rs1_split[1].strip(")")
    
    if rd not in register or rs1 not in register:
        return "error"
    
    imm = two_complement(int(immediate_val), 12)
    
    final = " ".join([imm, register[rs1], func3[ops], register[rd], opcode[ops]])
    return final
# print(I_identify("l1 lw a6, -4(s9)"))
# ......................................................................................................................................................................
def S_identify(text):
    space_split = text.split()
    
    # Check if there's a label
    if space_split[1] in func3:
        ops = space_split[1]
        instr_start = 2
    else:
        ops = space_split[0]
        instr_start = 1
    
    comma_split = text.split(",")
    rs2 = comma_split[0].split()[instr_start].strip()
    
    imm_rs1_split = comma_split[1].strip().split("(")
    immediate_val = imm_rs1_split[0].strip()
    rs1 = imm_rs1_split[1].strip(")")
    
    if len(comma_split) != 2:
        return "error"
    if rs2 not in register or rs1 not in register:
        return "error"
    
    imm = two_complement(int(immediate_val), 12)
    final = " ".join([imm[:7], register[rs2], register[rs1], func3[ops], imm[7:], opcode[ops]])
    return final

print(S_identify("start sw a6, 8(s9)"))
#...........................................................................................................................................................

# def B_identify(text):
#     space_split = text.split(" ")
#     ops = space_split[0]

#     comma_split = text.split(",")
#     rs2 = comma_split[0].split(" ")[1].strip()
    
#     imm_rs1_split = comma_split[1].strip().split("(")
#     immediate_val = imm_rs1_split[0].strip()  
#     rs1 = imm_rs1_split[1].strip(")")  


#     if len(comma_split)!=2:
#         return "error"
#     if rs2 not in register or rs1 not in register:
#         return "error"
#     imm = two_complement(int(immediate_val), 5)
#     beq_imm = '1111111'
#     final = " ".join([beq_imm, register[rs2], register[rs1], func3[ops], imm, opcode[ops]])
#     return final


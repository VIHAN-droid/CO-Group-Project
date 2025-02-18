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
        "jalr":"1100111", "sw":"0100011", "beq":"1100011","blt":"1100011","bne":"1100011"}

def two_complement(num, bits):
    if num<0:
        num = (1 << bits) + num 
    return str(format(num, f"0{bits}b"))

def refining_data(data):
    a1 = "abcdefghijklmnopqrstuvwxyz-"
    a2 = "1234567890"
    valid_chars = set(a1 + a2)
    ans = []
    for line in data:
        line = line.strip()  
        char1 = 0
        ans1 = []
        while char1 < len(line):
            if line[char1] in valid_chars:
                char2 = char1
                while char1 < len(line) and line[char1] in valid_chars:
                    char1 += 1
                ans1.append(line[char2:char1]) 
            else:
                char1 += 1  
        ans.append(ans1)
    return ans


def imm1(str1):
    return f"{str1[-13]}{str1[-11]}{str1[-10]}{str1[-9]}{str1[-8]}{str1[-7]}{str1[-6]}"

def imm2(str1):
    return f"{str1[-5]}{str1[-4]}{str1[-3]}{str1[-2]}{str1[-12]}"

def b_type_find_imm(ls,count):
    k=ls[count]
    if k[-1].isdigit():
        return 4*int(k[-1])
    else:
        # if count!=0:
        for i in range(len(ls)):
            if ls[i][0]==k[-1]:
                return 4*(i-count)

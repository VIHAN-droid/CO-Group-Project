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
        "jalr":"1100111", "sw":"0100011", "beq":"1100011","blt":"1100011","bne":"1100011","jal":"1101111"}

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

def J_Identify(text_list,label_dict):

    if text_list[0] in opcode:
        ops = text_list[0]
        rd = text_list[1]
        x = text_list[2]
        if x.isdigit() or (x.startswith('-') and x[1:].isdigit()): 
            num = int(x)
            imm = two_complement(num,23)
        else:
            num = 4 * ( label_dict[x][0] - label_dict[x][-1] )
            imm = two_complement(num,23)

    elif text_list[1] in opcode:
        ops = text_list[1]
        rd = text_list[2]
        x = text_list[3]
        if x.isdigit() or (x.startswith('-') and x[1:].isdigit()): 
            num = int(x)
            imm = two_complement(num,23)
        else:
            num = 4 * ( label_dict[x][0] - label_dict[x][-1] )
            imm = two_complement(num,23)
        
    if rd not in register:
        return 'error'
    
    binary_pattern = ( imm[-21] + imm[-11:-1] + imm[-12] + imm[-20:-12] + register[rd] + opcode[ops] )
    return binary_pattern

def R_identify(text_list):

    if text_list[0] in func7: 
        ops = text_list[0]
        rd, rs1, rs2 = text_list[1], text_list[2], text_list[3]
    else:  
        ops = text_list[1]  
        rd, rs1, rs2 = text_list[2], text_list[3], text_list[4]

    if rd not in register or rs1 not in register or rs2 not in register:
        return "error"
    
    binary_pattern = (
        func7[ops] + "" + register[rs2] + "" + register[rs1] + "" +
        func3[ops] + "" + register[rd] + "" + opcode[ops]
    )
    
    return binary_pattern

def I_identify(text_list):

    if not isinstance(text_list, list) or len(text_list) < 4:
        return "error"
    if text_list[0] not in func3:
        if len(text_list) < 5:
            return "error"  
        ops = text_list[1]
        if ops == 'lw':
            rd = text_list[2]
            offset = text_list[3]
            rs1 = text_list[4]
        else:
            rd, rs1, immediate_val = text_list[2], text_list[3], text_list[4]
    else:
        ops = text_list[0]
        if ops == 'lw':
            rd = text_list[1]
            offset = text_list[2]
            rs1 = text_list[3]
        else:
            rd, rs1, immediate_val = text_list[1], text_list[2], text_list[3]

    if rd not in register or rs1 not in register:
        return "error"
    try:
        if ops == 'lw':
            imm = two_complement(int(offset), 12)
        else:
            imm = two_complement(int(immediate_val), 12)
    except ValueError:
        return "error"

    final = "".join([imm, register[rs1], func3[ops], register[rd], opcode[ops]])
    return final

def S_identify(text_list):

    if not isinstance(text_list, list) or len(text_list) < 4:
        return "error"

    if text_list[0] in func3:  
        ops = text_list[0]  
        rs2, immediate_val, rs1 = text_list[1], text_list[2], text_list[3]
    elif text_list[1] in func3:
        ops = text_list[1]  
        rs2, immediate_val, rs1 = text_list[2], text_list[3], text_list[4]
    else:
        return "error"
   
    if rs2 not in register or rs1 not in register: 
        return "error"
    
    imm = two_complement(int(immediate_val), 12)

    final = "".join([imm[:7], register[rs2], register[rs1], func3[ops], imm[7:], opcode[ops]])
    return final


def imm1(str1):
    return f"{str1[-12]}{str1[-11]}{str1[-10]}{str1[-9]}{str1[-8]}{str1[-7]}{str1[-6]}"


def imm2(str1):
    return f"{str1[-5]}{str1[-4]}{str1[-3]}{str1[-2]}{str1[-12]}"

def b_type_find_imm(ls,count):

    k=ls[count]
    if k[-1].isdigit() or k[-1][0]=="-" and k[-1][1:].isdigit():
        return 4*int(k[-1])
    
    else:
        # if count!=0:
        for i in range(len(ls)):
            if ls[i][0]==k[-1]:
                return 4*(i-count)

def return_b_type(imm,rs2,rs1,ops):

    final_imm = two_complement(imm, 12)
    imm_1 = imm1(final_imm)
    imm_2 = imm2(final_imm)
    binary_pattern = f"{imm_1}{register[rs2]}{register[rs1]}{func3[ops]}{imm_2}{opcode[ops]}"
    return binary_pattern

def B_Identify(text_list, label_dict, current_index):

    if text_list[0] in opcode:
        ops = text_list[0]
        rs1 = text_list[1]
        rs2 = text_list[2]
        label = text_list[3]

    elif text_list[1] in opcode:
        ops = text_list[1]
        rs1 = text_list[2]
        rs2 = text_list[3]
        label = text_list[4]
    else:
        return 'error'
    
    if rs1 not in register or rs2 not in register:
        return 'error'
    
    if label.isdigit() or (label.startswith('-') and label[1:].isdigit()):
        imm = int(label)
    else:
        if label not in label_dict:
            return 'error'
        imm = (label_dict[label][0] - current_index) * 4
    
    k=return_b_type(imm,rs2,rs1,ops)
    return k

def main(test_file):
    file = open(test_file, "r")
    label_dict = {}
    data = file.readlines()
    refined_data = refining_data(data)
    output_list = []
    counter = 0

    for i in refined_data:
        if len(i) == 5 and i[0] not in opcode:
            label_dict[i[0]] = [counter]
        elif len(i) == 4 and i[0] not in opcode:
            label_dict[i[0]] = [counter]
        counter2=0
        for j in refined_data:
            if j[-1] == i[0]:
                label_dict[i[0]].append(counter2)
            counter2+=1
        counter += 1

    for count in range(len(refined_data)):
        countt=0
        for i in refined_data[count]:
            if i in B_type:
                output_list.append(B_Identify(refined_data[count],label_dict,count))
                countt += 1

        instructions = refined_data[count]
        if countt == 0:
            if len(instructions) not in [3, 4, 5]:
                output_list.append('error')
                continue

            opcode_key = instructions[0] if instructions[0] in opcode else instructions[1] if len(instructions) > 1 and instructions[1] in opcode else None

            if opcode_key is None:
                output_list.append('error')
                continue
            
            if opcode_key in J_type:
                output_list.append(J_Identify(instructions,label_dict))
            elif opcode_key in R_type:
                output_list.append(R_identify(instructions))
            elif opcode_key in S_type:
                output_list.append(S_identify(instructions))
            elif opcode_key in I_type:
                output_list.append(I_identify(instructions))
            else:
                output_list.append('error')

    file.close()
    return output_list

def write_file(file):
    output_list = main(file)
    with open("Output.txt", "w") as f:
        for line in output_list:
            print(line)
            f.write(line)
            f.write("\n")

file_input = input("Enter the file name: ")
write_file(file_input)
print("Output is stored in Output.txt")

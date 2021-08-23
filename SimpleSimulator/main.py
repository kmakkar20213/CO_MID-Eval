import sys
import matplotlib.pyplot as plt
complete_input = sys.stdin.read()

lines=(complete_input.split("\n"))

register = {"000" : "0000000000000000" , "001" : "0000000000000000","010" :"0000000000000000" ,
            "011" :"0000000000000000","100" :"0000000000000000" , "101" :"0000000000000000",
            "110" :"0000000000000000","111" :"0000000000000000",}


def typeA(op , reg1 , reg2 , reg3):
    if op == "00000":
        if int(register[reg2] , 2) + int(register[reg3],2) <= (2**16 - 1):
            register[reg1] = bin(int(register[reg2] , 2) + int(register[reg3],2))[2:]
            register["111"] = "0000000000000000"
        else:
            register[reg1] = "0000000000000000"
            register["111"] = "0000000000001000"

    if op == "00001":
        if int(register[reg2], 2) + int(register[reg3], 2) >= 0:
            register[reg1] = bin(int(register[reg2], 2) - int(register[reg3], 2))[2:]
            register["111"] = "0000000000000000"

        else:
            register[reg1] = bin(int(register[reg2], 2) + int(register[reg3], 2))[-16:]
            register["111"] = "0000000000001000"

    if op == "00110":
        if int(register[reg2], 2) * int(register[reg3], 2) <= (2 ** 16 - 1):
            register[reg1] = bin(int(register[reg2], 2) * int(register[reg3], 2))[2:]
            register["111"] = "0000000000000000"
        else:
            register[reg1] = bin(int(register[reg2], 2) * int(register[reg3], 2))[-16:]
            register["111"] = "0000000000001000"

    if op == "01011":
        register[reg1] = bin(int(register[reg2],2) | int(register[reg3],2))[2:]
        register["111"] = "0000000000000000"

    if op == "01100":
        register[reg1] = bin(int(register[reg2],2) & int(register[reg3],2))[2:]
        register["111"] = "0000000000000000"

    if op == "01010":
        register[reg1] = bin(int(register[reg2],2) ^ int(register[reg3],2))[2:]
        register["111"] = "0000000000000000"


def typeB(op , reg1 , imm):
    if op == "00010":
        if int(imm,2) <= 255:
            register[reg1] = imm

    if op == "01000":
        register[reg1] = register[reg1][int(imm,2):] + ("0"**int(imm,2))

    if op == "01001":
        register[reg1] = ("0"**int(imm,2)) +  register[reg1][:16 - int(imm,2)]


def typeC(op , reg1 , reg2):
    if op == "00011":
        register[reg1] = register[reg2]
        register["111"] = "0000000000000000"

    if op == '00111':
        register["000"] = reg1 // reg2
        register['001'] = reg1%reg2
        register["111"] = "0000000000000000"
    if op == "01101":
        register[reg1] = bin(~int(register[reg2],2))[2,]
        register["111"] = "0000000000000000"

    if op == "01110":
        if int(register[reg1],2) == int(register[reg2],2):
            register["111"] = "0000000000000001"
        elif int(register[reg1],2) > int(register[reg2],2):
            register["111"] = "0000000000000010"
        elif int(register[reg1],2) < int(register[reg2],2):
            register["111"] = "0000000000000100"


def typeD(op,reg1,address):
    if op == "00100":
        register[reg1] = lines[int(address,2)]

    if op == "00101":
        while True:
            if len(lines) >= int(address,2) + 1:
                lines[int(address,2)] = to16(register[reg1])
                break
            else:
                lines.append("0000000000000000")

    register["111"] = "0000000000000000"

def typeE(op,address,pc):
    if op == "01111":
        register["111"] = "0000000000000000"
        run(int(address,2),lines)

    elif op == "10000" and register["111"] == "0000000000000100":
        register["111"] = "0000000000000000"
        run(int(address,2),lines)

    elif op == "10001" and register["111"] == "0000000000000010":
        register["111"] = "0000000000000000"
        run(int(address,2),lines)

    elif op == "10010" and register["111"] == "0000000000000001":
        register["111"] = "0000000000000000"
        run(int(address,2),lines)

    else :
        register["111"] = "0000000000000000"
        run(pc , lines)

def to16(s):
    new = "0"*(16-len(s)) + s
    return new


def to8(num):
    bi = bin(num)[2:]
    new = "0"*(8-len(bi)) + bi
    return new


opcodes= {"A":["00000","00001","00110", "01011" ,"01100","01010"] ,"B" : ["00010","01000","01001"] ,
    "C": ["00011",'00111',"01101","01110"] , "D": ["00100" , "00101"],
    "E": ["01111","10000","10001","10010"], "F": ["10011"]}

forplot = []
def run(PC , lines):

    forplot.append(PC)

    code = lines[PC]
    op = code[:5]
    for i in opcodes:
        if op in opcodes[i]:
            this = i
            break

    if this == "A":
        typeA(op , code[7:10] , code[10:13], code[13:16])

    if this == "B":
        typeB(op , code[5:8] , code[8:16])

    if this == "C":
        typeC(op , code[10:13] , code[13:16])

    if this == "D":
        typeD(op, code[5:8] , code[8:])

    if this == "E":
        print(to8(PC) , to16(register["000"]) , to16(register["001"]) , to16(register["010"]) , to16(register["011"]) ,
              to16(register["100"]) , to16(register["101"]) , to16(register["110"]) , '0000000000000000')
        typeE(op,code[8:],PC+1)



    if this == "F":
        register["111"] = "0000000000000000"
        print(to8(PC), to16(register["000"]), to16(register["001"]), to16(register["010"]), to16(register["011"]),
              to16(register["100"]), to16(register["101"]), to16(register["110"]), to16(register["111"]))
        return

    if this != "E":
        print(to8(PC) , to16(register["000"]) , to16(register["001"]) , to16(register["010"]) , to16(register["011"]) ,
              to16(register["100"]) , to16(register["101"]) , to16(register["110"]) , to16(register["111"]))
        run(PC+1 , lines)




run(0 , lines)
if len(lines) < 256:
    lines.extend(["0000000000000000"]*(256-len(lines)))

for i in lines:
    print(i)

x = range(1,len(forplot) + 1)
y = forplot

plt.scatter(x, y)
plt.show()

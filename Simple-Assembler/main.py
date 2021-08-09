
opcodes= {
 "add":"00000" ,  "sub":"00001" , "mov":"00010", "mov_r": "00011", "ld": "00100" , "st": "00101", "mul": "00110",
 "div": "00111",  "rs":"01000", "ls": "01001", "xor":"01010", "or": "01011", "and": "01100", "not":"01101",
 "cmp": "01110",  "jmp": "01111", "jlt": "10000", "jgt": "10001", "je": "10010", "hlt": "10011"
}
#replace key with value on in txt file, hecne defined dict
#since there are 2 move commands and dono ka name is mov to usi time based on arg we gotta check is it mov_r or mov_i


register= {
    "R0":"000", "R1":"001", "R2":"010", "R3":"011", "R4":"100", "R5":"101", "R6":"110", "FLAGS":"111"
}
label_dict= {}
var_dict={}
def decimalToBinary(n):
    return "{0:b}".format(int(n))

def length_adjuster(s):
    if(len(s)<8):
        c= 8- len(s)
        return "0"*c + s







f= open(r"C:\Users\Bhan\Desktop\demo.txt")
#print(f.readlines())
lines=[]
while True:
    x= f.readline()  # this returns the each line that ends with /n , basically used to separate commands
    #print(x)
    if not x:
        break
    lines.append(x.strip()) #store in a list the new lines, using strip to remove extra white spaces if any
f.close()

line=[]
c=0

for i in range(len(lines)):

    g=(lines[i]).split()


    x=g[0]
    if ":" in x:
        y= g[0][0:len(g[0])-2] #this is label type command
        label_dict[y]= c       #store label address in dict

        s=g[1]                 #in case of label next command is instruction #write case if not command
        if (s in opcodes.keys()):
            b = ""
            for i in g:
                b = b + str(i) + " "

            a = str(c) + str(" ") + b
            line.append(a)
            c = c + 1




    elif(x in opcodes.keys()):
        b=""
        for i in g:
            b=b+ str(i) + " "

        a= str(c)+ str(" ") + b
        line.append(a)
        c=c+1



for i in range(len(lines)):

    g=(lines[i]).split()
    #print("hhhhhhhhhhhh")
    #print(g)

    x=g[0]
    if len(g) != 1:
        t = g[1]


    if(x== "var"): #this we will need to modify for error handling
        b=""
        for i in g:
            b=b+ str(i) + " "

        a= str(c)+ str(" ") + b
        var_dict[t]= c #store var value in dict
        line.append(a)

        c=c+1

    #write code for unidentifiable object command present but it can be label.. i think we gotta check label:
#print(line)
#print("merii")


for i in range (len(line)):
    sub_line= line[i].split()

    if(len(sub_line)==2):
        sub_line[1]= "1001100000000000"
        line[i]=sub_line[1]
        #this instruction is hlt #type-f



    elif(len(sub_line)==3):
        # this is either of the jump instructions or var x declaration
        to_find= sub_line[1]
        if(to_find != "var"):
            op_code_value = opcodes[to_find]
            line[i]= str(op_code_value) +"000"+ length_adjuster(str(decimalToBinary(int(label_dict[sub_line[2]]))))
            #meed to ask on classsroom how is mem adrres given? as 8 bits
            #or we need to make it to 8 bits

    elif(len(sub_line)==4):
        #move instruction, load, store, div, rs, ls, not, cmp,
        to_find=sub_line[1]
        if(to_find== "mov"):
            # in this case we need to see if this is move immediate or move from another register

            if(sub_line[3]=="R0" or sub_line[3]=="R1" or sub_line[3]=="R2" or sub_line[3]=="R3" or
               sub_line[3]=="R4" or sub_line[3]=="R5" or sub_line[3]=="R6" or sub_line[3]=="R7"):
                op_code_value= str(opcodes["mov_r"])
                line[i]= str(op_code_value) + "00000" + str(register[sub_line[2]])+ str(register[sub_line[3]])
            else:
                op_code_value= str(opcodes["mov"])
                remove_dollar= int(sub_line[3][1:len(sub_line[3])]) #omit the dollar sign
                #print("ggggg")
                #print(remove_dollar)
                bin_equi=  length_adjuster(str(decimalToBinary(remove_dollar)))

                line[i]= str(op_code_value) + str(register[sub_line[2]]) + bin_equi

        elif (to_find == "ld"):
            a= str(opcodes[to_find])      #opcode ka binary
            b= register[sub_line[2]] #pass register value to get its binary

            c= length_adjuster(str(decimalToBinary(int(var_dict[sub_line[3]]))))
            line[i]= a+b+c

        elif(to_find=="st"):
            a= str(opcodes[to_find])
            b= register[sub_line[2]]
            print(sub_line[3])
            c= length_adjuster(str(decimalToBinary(int(var_dict[sub_line[3]]))))
            line[i]= a+b+c

        elif(to_find=="div"):
            a=str(opcodes[to_find])
            b="00000"
            c=sub_line[2]
            d=sub_line[3]
            line[i]= a+b+c+d

        elif(to_find=="rs"):
            a = str(opcodes[to_find])
            b= register[sub_line[2]]

            remove_dollar = int(sub_line[3][1:len(sub_line[3])])  # omit the dollar sign
            bin_equi = length_adjuster(str(decimalToBinary(remove_dollar)))

            line[i] = a + b + bin_equi

        elif (to_find == "ls"):
            a = str(opcodes[to_find])
            b = register[sub_line[2]]

            remove_dollar = int(sub_line[3][1:len(sub_line[3])])  # omit the dollar sign
            bin_equi = length_adjuster(str(decimalToBinary(remove_dollar)))

            line[i] = a + b + bin_equi

        elif (to_find == "not"):
            a = str(opcodes[to_find])
            b = "00000"
            c = register[sub_line[2]]
            d = register[sub_line[3]]
            line[i] = a + b + c + d

        elif (to_find == "cmp"):
            a = str(opcodes[to_find])
            b = "00000"
            c = register[sub_line[2]]
            d = register[sub_line[3]]
            line[i] = a + b + c + d


    elif(len(sub_line)==5):
        to_find = sub_line[1]
        #add, sub, mul, xor, or, and
        if (to_find == "add"):
            a = str(opcodes[to_find])
            b="00"
            c=register[sub_line[2]]
            d=register[sub_line[3]]
            e=register[sub_line[4]]
            line[i] = a + b + c + d + e


        elif (to_find == "sub"):
            a = str(opcodes[to_find])
            b = "00"
            c = register[sub_line[2]]
            d = register[sub_line[3]]
            e = register[sub_line[4]]
            line[i] = a + b + c + d + e


        elif (to_find == "mul"):
            a = str(opcodes[to_find])
            b = "00"
            c = register[sub_line[2]]
            d = register[sub_line[3]]
            e = register[sub_line[4]]
            line[i] = a + b + c + d + e


        elif (to_find == "xor"):
            a = str(opcodes[to_find])
            b = "00"
            c = register[sub_line[2]]
            d = register[sub_line[3]]
            e = register[sub_line[4]]
            line[i] = a + b + c + d + e


        elif (to_find == "or"):
            a = str(opcodes[to_find])
            b = "00"
            c = register[sub_line[2]]
            d = register[sub_line[3]]
            e = register[sub_line[4]]
            line[i] = a + b + c + d + e


        elif (to_find == "and"):
            a = str(opcodes[to_find])
            b = "00"
            c = register[sub_line[2]]
            d = register[sub_line[3]]
            e = register[sub_line[4]]
            line[i] = a + b + c + d + e


print(line)


















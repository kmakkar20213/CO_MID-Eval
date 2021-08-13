
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

def check_if_hlt_last(line):
    index=-1

    for i in range(len(line)):
        g=line[i].split()

        if(g[1]== "hlt" or g[2]=="hlt"):
            index= g[0]
            break



    s= line[int(index)+1].split()

    if s[1]=="var":
        return True
    else:
        return False


def typo_in_name(line):
    for i in range(len(line)):
        g=line.split()
        if not(isinstance(g[0],int)): #if each line is not getting a number before it this means that start point is not
            return False              #instruction or variable
        return True

def check_valid_reg_name(s):
    if s in register.keys():
        return True
    return False #modify all functions to handle this

def check_var_in_begin(lines):
     index=-1
     for i in range(len(lines)):
         line=lines[i].split()
         if(line[0]!="var"):
             index=i
             break

     if(index!=-1):
         for i in range(index+1, len(lines)):
             line=lines[i].split()
             if(line[0]=="var"):
                 return False

         return True
     else:
         #this would be case that code only contains variable declaration
         return True


def check_illegal_immediate_value(s):
    if int(s)>=0 and int(s)<=255:
        return True
    return False

def check_undefined_variables(s):
    if s in var_dict.keys():
        return True
    return  False

def check_undefined_labels(s):
    if s in label_dict.keys():
        return True
    return  False

def count_multiple_hlt(line):
    c=0


    for i in range(len(line)):
        g=line[i].split()



        if(g[1]== "hlt"):
            c=c+1
        elif(g[2]=="hlt"):
            c=c+1

    return c

def find_line_number(line):
    c=1
    f=open(r"C:\Users\Bhan\Desktop\demo.txt")
    while True:
        x = f.readline()  # this returns the each line that ends with /n , basically used to separate commands
        final_line= x.strip()
        if final_line == line:
            c=c+1
            break
        else:
            c=c+1
    return c

def find_line_number_2(line, lines):
    c=1
    for i in range(len(lines)):
        if(len(lines[i])!=0):
            g=lines[i].split()
            if(g== line):
                break
            else:
                c=c+1

    return c





error_counter=0
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
#print(lines)


for i in range(len(lines)):
    if(len(lines[i])!=0):



        g=(lines[i]).split()


        x=g[0]



        if ":" in x:
            if(len(g)!=1): #if len is 1 it means no instruction after label


                y= g[0][0:len(g[0])-1] #this is label type command
                if(y not in label_dict.keys() and y not in opcodes.keys()): #label cant be instruction type

                    label_dict[y]= c      #store label address in dict
                    s = g[1]

                    # in case of label next command is instruction #write case if not command
                    if (s in opcodes.keys()):
                        b = y + " "
                        for i in range(1, len(g)):
                            b = b + str(g[i]) + " "


                        a = str(c) + str(" ") + b
                        line.append(a)
                        c = c + 1


                else:
                    line_number = find_line_number(lines[i])
                    print("error at line" + str(find_line_number(lines[i]) -1) + ". you have already declared this label")
                    error_counter = error_counter+1


            elif(len(g)==1):
                line_number = find_line_number(lines[i])
                print("error at line" + str(find_line_number(lines[i]) -1) + " no instruction after label")
                error_counter = error_counter + 1




        elif(x in opcodes.keys()):
            b=""
            for i in g:
                b=b+ str(i) + " "

            a= str(c)+ str(" ") + b
            line.append(a)
            c=c+1







for i in range(len(lines)):

    if (len(lines[i]) != 0):
        #print(lines[i])
        g=(lines[i]).split()



        x=g[0]
        if len(g) != 1:
            t = g[1]


            if(x== "var" and t not in var_dict.keys()): #this we will need to modify for error handling
                b=""
                for i in g:
                    b=b+ str(i) + " "

                a= str(c)+ str(" ") + b
                var_dict[t]= c #store var value in dict
                line.append(a)

                c=c+1
            elif(t in var_dict.keys()):
                line_number=find_line_number(lines[i])
                print("error! trying to re-define a variable at line"+ str(line_number)) #re-defining of variables case
                error_counter = error_counter + 1

        elif(x=="var"):
            line_number = find_line_number(lines[i])
            print("error at line"+ str(line_number -1) + ". variable name not declared!")
            error_counter = error_counter + 1


#print(line)


#checks for multiple hlts
halt_checker1= count_multiple_hlt(line)
if(halt_checker1==0):
    print("missing hlt")
    error_counter = error_counter + 1
elif(halt_checker1>1):
    print("multiple hlts used")
    error_counter = error_counter + 1

if(halt_checker1==1):

    halt_checker2= check_if_hlt_last(line)
    if(not halt_checker2):
        print("halt is not last instruction")
        error_counter = error_counter + 1

#check
if(error_counter==0):

    for i in range (len(line)):


        sub_line= line[i].split()
        to_find = sub_line[1]

        if(to_find=="hlt"):  #instruction-1
            sub_line[1] = "1001100000000000"
            line[i] = sub_line[1]

        elif(to_find == "jgt" or to_find == "je" or to_find == "jmp" or to_find == "jlt"): #instruction-2,3,4,5
            op_code_value = opcodes[to_find]
            syntax_check = check_undefined_labels(sub_line[2])

            if (syntax_check):
                line[i] = str(op_code_value) + "000" + length_adjuster(str(decimalToBinary(int(label_dict[sub_line[2]]))))
            elif (to_find != "var"):
                error_on_line= str(find_line_number_2(str(sub_line[1]+ sub_line[2]), lines))
                print("error at line" + error_on_line+  " invalid syntax for given opcode of " + str(to_find)+ " type!!")
                error_counter = error_counter + 1

        elif(to_find== "mov"): #instruction-6,7
            syntax_check = check_valid_reg_name(sub_line[2])

            if (syntax_check):

                if (

                        sub_line[3] == "R0" or sub_line[3] == "R1" or sub_line[3] == "R2" or sub_line[3] == "R3" or
                        sub_line[3] == "R4" or sub_line[3] == "R5" or sub_line[3] == "R6" or sub_line[3] == "R7" or
                        sub_line[3] == "FLAGS"):

                    op_code_value = str(opcodes["mov_r"])
                    line[i] = str(op_code_value) + "00000" + str(register[sub_line[2]]) + str(register[sub_line[3]])

                elif ("$" in sub_line[3]):
                    op_code_value = str(opcodes["mov"])
                    remove_dollar = int(sub_line[3][1:len(sub_line[3])])  # omit the dollar sign
                    if (check_illegal_immediate_value(remove_dollar)):

                        # print("ggggg")
                        # print(remove_dollar)
                        bin_equi = length_adjuster(str(decimalToBinary(remove_dollar)))

                        line[i] = str(op_code_value) + str(register[sub_line[2]]) + bin_equi
                    else:
                        error_on_line = str(find_line_number_2(str(sub_line[1] + sub_line[2] +sub_line[3]), lines) -1)
                        print("error at line " + error_on_line+ " illegal immediate value used for register!")
                        error_counter = error_counter + 1

                else:
                    error_on_line = str(find_line_number_2(str(sub_line[1] + sub_line[2] + sub_line[3]), lines) - 1)
                    print("error at line " + error_on_line+ " invalid register used")
                    error_counter = error_counter + 1

            else:
                error_on_line = str(find_line_number_2(str(sub_line[1] + sub_line[2] + sub_line[3]), lines) - 1)
                print("error at line " + error_on_line+ " invalid register used at line!!")
                error_counter = error_counter + 1

        elif(to_find == "ld"): #instruction-8
            a = str(opcodes[to_find])  # opcode ka binary

            syntax_check = sub_line[2]!= "FLAGS" and check_valid_reg_name((sub_line[2])) and check_undefined_variables(sub_line[3])
            if (syntax_check):
                b = register[sub_line[2]]  # pass register value to get its binary

                c = length_adjuster(str(decimalToBinary(int(var_dict[sub_line[3]]))))
                line[i] = a + b + c
            else:
                error_on_line = str(find_line_number_2(str(sub_line[1] + sub_line[2] + sub_line[3]), lines) - 1)
                print("error at line " + error_on_line+ ". invalid register used or undefined variable input!!")
                error_counter = error_counter + 1

        elif (to_find == "st"): #instruction-9
            a = str(opcodes[to_find])
            syntax_check = sub_line[2]!= "FLAGS" and check_valid_reg_name((sub_line[2])) and check_undefined_variables(sub_line[3])
            if (syntax_check):
                b = register[sub_line[2]]
                # print(sub_line[3])
                c = length_adjuster(str(decimalToBinary(int(var_dict[sub_line[3]]))))
                line[i] = a + b + c
            else:
                error_on_line = str(find_line_number_2(str(sub_line[1] + sub_line[2] + sub_line[3]), lines) - 1)
                print("error at line " + error_on_line+ " invalid register used or undefined variable input!")
                error_counter = error_counter + 1


        elif (to_find == "div"): #instruction-10
            a = str(opcodes[to_find])
            b = "00000"
            syntax_check = sub_line[2]!= "FLAGS" and check_valid_reg_name((sub_line[2])) and check_valid_reg_name((sub_line[3]))
            if (syntax_check):
                c = sub_line[2]
                d = sub_line[3]
                line[i] = a + b + c + d
            else:
                error_on_line = str(find_line_number_2(str(sub_line[1] + sub_line[2] + sub_line[3]), lines) - 1)
                print("error at line " + error_on_line+ ". invalid register used!")
                error_counter = error_counter + 1

        elif (to_find == "rs"): #instruction-11
            a = str(opcodes[to_find])
            syntax_check = sub_line[2]!= "FLAGS" and check_valid_reg_name((sub_line[2]))
            if (syntax_check):
                b = register[sub_line[2]]

                remove_dollar = int(sub_line[3][1:len(sub_line[3])])  # omit the dollar sign
                if (check_illegal_immediate_value(remove_dollar)):
                    bin_equi = length_adjuster(str(decimalToBinary(remove_dollar)))

                    line[i] = a + b + bin_equi
                else:
                    error_on_line = str(find_line_number_2(str(sub_line[1] + sub_line[2] + sub_line[3]), lines) - 1)
                    print("error at line " + error_on_line + ". invalid immediate value used!!")

                    error_counter = error_counter + 1
            else:
                error_on_line = str(find_line_number_2(str(sub_line[1] + sub_line[2] + sub_line[3]), lines) - 1)
                print("error at line " + error_on_line + ". invalid register used!")
                error_counter = error_counter + 1

        elif (to_find == "ls"): #instruction-12
            a = str(opcodes[to_find])
            syntax_check = sub_line[2]!= "FLAGS" and check_valid_reg_name((sub_line[2]))
            if (syntax_check):

                b = register[sub_line[2]]

                remove_dollar = int(sub_line[3][1:len(sub_line[3])])  # omit the dollar sign
                if (check_illegal_immediate_value(remove_dollar)):
                    bin_equi = length_adjuster(str(decimalToBinary(remove_dollar)))

                    line[i] = a + b + bin_equi
                else:
                    error_on_line = str(find_line_number_2(str(sub_line[1] + sub_line[2] + sub_line[3]), lines) - 1)
                    print("error at line " + error_on_line + ". invalid immediate value used!!")
                    error_counter = error_counter + 1

            else:
                error_on_line = str(find_line_number_2(str(sub_line[1] + sub_line[2] + sub_line[3]), lines) - 1)
                print("error at line " + error_on_line +". invalid register used!")
                error_counter = error_counter + 1


        elif (to_find == "not"): #instruction-13
            syntax_check = sub_line[2]!= "FLAGS" and sub_line[3]!= "FLAGS" and check_valid_reg_name((sub_line[2])) and check_valid_reg_name((sub_line[3]))
            if (syntax_check):

                a = str(opcodes[to_find])
                b = "00000"
                c = register[sub_line[2]]
                d = register[sub_line[3]]
                line[i] = a + b + c + d

            else:
                error_on_line = str(find_line_number_2(str(sub_line[1] + sub_line[2] + sub_line[3]), lines) - 1)
                print("error at line " + error_on_line + ". invalid register used!")
                error_counter = error_counter + 1

        elif (to_find == "cmp"): #instruction-14
            syntax_check = sub_line[2]!= "FLAGS" and sub_line[3]!= "FLAGS" and check_valid_reg_name((sub_line[2])) and check_valid_reg_name((sub_line[3]))
            if (syntax_check):
                a = str(opcodes[to_find])
                b = "00000"
                c = register[sub_line[2]]
                d = register[sub_line[3]]
                line[i] = a + b + c + d

            else:
                error_on_line = str(find_line_number_2(str(sub_line[1] + sub_line[2] + sub_line[3]), lines) - 1)
                print("error at line " + error_on_line + "invalid register used!")
                error_counter = error_counter + 1
        #else:
            #print("2 invalid syntax for given opcode!!")

        elif(to_find == "add"): #instruction-15
                syntax_check = check_valid_reg_name((sub_line[2])) and check_valid_reg_name((sub_line[3])) and check_valid_reg_name((sub_line[4]))
                if (syntax_check):
                    a = str(opcodes[to_find])
                    b="00"
                    c=register[sub_line[2]]
                    d=register[sub_line[3]]
                    e=register[sub_line[4]]
                    line[i] = a + b + c + d + e
                else:
                    error_on_line = str(find_line_number_2(str(sub_line[1] + sub_line[2] + sub_line[3]+ sub_line[4]), lines) - 1)
                    print("error at line " + error_on_line + "invalid register used!")
                    error_counter = error_counter + 1

        elif (to_find == "sub"): #instruction-16
            syntax_check = check_valid_reg_name((sub_line[2])) and check_valid_reg_name(
                (sub_line[3])) and check_valid_reg_name((sub_line[4]))
            if (syntax_check):
                a = str(opcodes[to_find])
                b = "00"
                c = register[sub_line[2]]
                d = register[sub_line[3]]
                e = register[sub_line[4]]
                line[i] = a + b + c + d + e
            else:
                error_on_line = str(find_line_number_2(str(sub_line[1] + sub_line[2] + sub_line[3] + sub_line[4]), lines) - 1)
                print("error at line " + error_on_line + "invalid register used!")

                error_counter = error_counter + 1




        elif (to_find == "mul"): #instruction-17
            syntax_check = check_valid_reg_name((sub_line[2])) and check_valid_reg_name(
                (sub_line[3])) and check_valid_reg_name((sub_line[4]))
            if (syntax_check):
                a = str(opcodes[to_find])
                b = "00"
                c = register[sub_line[2]]
                d = register[sub_line[3]]
                e = register[sub_line[4]]
                line[i] = a + b + c + d + e
            else:

                error_on_line = str(find_line_number_2(str(sub_line[1] + sub_line[2] + sub_line[3] + sub_line[4]), lines) - 1)
                print("error at line " + error_on_line + "invalid register used!")
                error_counter = error_counter + 1



        elif (to_find == "xor"): #instruction-18
            syntax_check = check_valid_reg_name((sub_line[2])) and check_valid_reg_name(
                (sub_line[3])) and check_valid_reg_name((sub_line[4]))
            if (syntax_check):
                a = str(opcodes[to_find])
                b = "00"
                c = register[sub_line[2]]
                d = register[sub_line[3]]
                e = register[sub_line[4]]
                line[i] = a + b + c + d + e
            else:

                error_on_line = str(find_line_number_2(str(sub_line[1] + sub_line[2] + sub_line[3] + sub_line[4]), lines) - 1)
                print("error at line " + error_on_line + "invalid register used!")
                error_counter = error_counter + 1


        elif (to_find == "or"): #instruction-19
            syntax_check = check_valid_reg_name((sub_line[2])) and check_valid_reg_name(
                (sub_line[3])) and check_valid_reg_name((sub_line[4]))
            if (syntax_check):
                a = str(opcodes[to_find])
                b = "00"
                c = register[sub_line[2]]
                d = register[sub_line[3]]
                e = register[sub_line[4]]
                line[i] = a + b + c + d + e
            else:
                error_on_line = str(find_line_number_2(str(sub_line[1] + sub_line[2] + sub_line[3] + sub_line[4]), lines) - 1)
                print("error at line " + error_on_line + "invalid register used!")

                error_counter = error_counter + 1


        elif (to_find == "and"): #instruction-20
            syntax_check = check_valid_reg_name((sub_line[2])) and check_valid_reg_name(
                (sub_line[3])) and check_valid_reg_name((sub_line[4]))
            if (syntax_check):
                a = str(opcodes[to_find])
                b = "00"
                c = register[sub_line[2]]
                d = register[sub_line[3]]
                e = register[sub_line[4]]
                line[i] = a + b + c + d + e
            else:

                error_on_line = str(find_line_number_2(str(sub_line[1] + sub_line[2] + sub_line[3] + sub_line[4]), lines) - 1)
                print("error at line " + error_on_line + "invalid register used!")
                error_counter = error_counter + 1

        elif(to_find in label_dict.keys()):
            instruction= sub_line[2]
            if(instruction in opcodes.keys()): # this check if instruction after label is valid or not

                op_code_value=opcodes[instruction]

                if(len(sub_line)==3):
                    # this instruction is halt
                    line[i] = "1001100000000000"

                elif (len(sub_line) == 4):
                    # this is either of the jump instructions
                    line[i] = str(op_code_value) + "000" + length_adjuster(str(decimalToBinary(int(label_dict[sub_line[3]]))))

                elif(len(sub_line) == 5):
                    # move instruction, load, store, div, rs, ls, not, cmp,
                    if (instruction == "mov"):
                        syntax_check = check_valid_reg_name(sub_line[3])

                        if (syntax_check):

                            if (

                                 sub_line[4] == "R0" or sub_line[4] == "R1" or sub_line[4] == "R2" or sub_line[
                                4] == "R3" or
                                    sub_line[4] == "R4" or sub_line[4] == "R5" or sub_line[4] == "R6" or sub_line[
                                4] == "R7" or sub_line[4] == "FLAGS"):

                                op_code_value = str(opcodes["mov_r"])
                                line[i] = str(op_code_value) + "00000" + str(register[sub_line[3]]) + str(
                                    register[sub_line[4]])

                            elif ("$" in sub_line[4]):
                                op_code_value = str(opcodes["mov"])
                                remove_dollar = int(sub_line[3][1:len(sub_line[4])])  # omit the dollar sign
                                if (check_illegal_immediate_value(remove_dollar)):

                                    # print("ggggg")
                                    # print(remove_dollar)
                                    bin_equi = length_adjuster(str(decimalToBinary(remove_dollar)))

                                    line[i] = str(op_code_value) + str(register[sub_line[3]]) + bin_equi
                                else:
                                    error_on_line = str(find_line_number_2(str(sub_line[2] + sub_line[3] + sub_line[4]),
                                                           lines) - 1)

                                    print("error at line " + error_on_line + "invalid register used!")
                                    error_counter = error_counter + 1
                            else:
                                #print(line[i])
                                error_on_line = str(find_line_number_2(str(sub_line[2] + sub_line[3] + sub_line[4]), lines) - 1)
                                print("error at line " + error_on_line + " invalid register used")

                                error_counter = error_counter + 1

                        else:
                            error_on_line = str(find_line_number_2(str(sub_line[2] + sub_line[3] + sub_line[4]), lines) - 1)
                            print("error at line " + error_on_line + " invalid register used at line!!")

                            error_counter = error_counter + 1

                    elif (instruction == "ld"):
                        a = str(opcodes[instruction])  # opcode ka binary

                        syntax_check = check_valid_reg_name((sub_line[3])) and check_undefined_variables(sub_line[4])
                        if (syntax_check):
                            b = register[sub_line[3]]  # pass register value to get its binary

                            c = length_adjuster(str(decimalToBinary(int(var_dict[sub_line[3]]))))
                            line[i] = a + b + c
                        else:
                            error_on_line = str(find_line_number_2(str(sub_line[2] + sub_line[3] + sub_line[4]), lines) - 1)
                            print("error at line " + error_on_line + ". invalid register used or undefined variable input!!")

                            error_counter = error_counter + 1

                    elif (instruction == "st"):
                        a = str(opcodes[instruction])
                        syntax_check = check_valid_reg_name((sub_line[3])) and check_undefined_variables(sub_line[4])
                        if (syntax_check):
                            b = register[sub_line[3]]
                            # print(sub_line[3])
                            c = length_adjuster(str(decimalToBinary(int(var_dict[sub_line[4]]))))
                            line[i] = a + b + c
                        else:
                            error_on_line = str(find_line_number_2(str(sub_line[2] + sub_line[3] + sub_line[4]), lines) - 1)
                            print("error at line " + error_on_line + " invalid register used or undefined variable input!")

                            error_counter = error_counter + 1

                    elif (instruction == "div"):
                        a = str(opcodes[instruction])
                        b = "00000"
                        syntax_check = check_valid_reg_name((sub_line[3])) and check_valid_reg_name((sub_line[4]))
                        if (syntax_check):
                            c = sub_line[3]
                            d = sub_line[4]
                            line[i] = a + b + c + d
                        else:
                            error_on_line = str(find_line_number_2(str(sub_line[2] + sub_line[3] + sub_line[4]), lines) - 1)
                            print("error at line " + error_on_line + ". invalid register used!")

                            error_counter = error_counter + 1

                    elif (to_find == "rs"):
                        a = str(opcodes[instruction])
                        syntax_check = check_valid_reg_name((sub_line[3]))
                        if (syntax_check):
                            b = register[sub_line[3]]

                            remove_dollar = int(sub_line[4][1:len(sub_line[4])])  # omit the dollar sign
                            if (check_illegal_immediate_value(remove_dollar)):
                                bin_equi = length_adjuster(str(decimalToBinary(remove_dollar)))

                                line[i] = a + b + bin_equi
                            else:
                                error_on_line = str(find_line_number_2(str(sub_line[2] + sub_line[3] + sub_line[4]), lines) - 1)
                                print("error at line " + error_on_line + ". invalid immediate value used!!")

                                error_counter = error_counter + 1
                        else:
                            error_on_line = str(find_line_number_2(str(sub_line[2] + sub_line[3] + sub_line[4]), lines) - 1)
                            print("error at line " + error_on_line + ". invalid register used!")

                            error_counter = error_counter + 1

                    elif (to_find == "ls"):
                        a = str(opcodes[instruction])
                        syntax_check = check_valid_reg_name((sub_line[3]))
                        if (syntax_check):

                            b = register[sub_line[3]]

                            remove_dollar = int(sub_line[4][1:len(sub_line[4])])  # omit the dollar sign
                            if (check_illegal_immediate_value(remove_dollar)):
                                bin_equi = length_adjuster(str(decimalToBinary(remove_dollar)))

                                line[i] = a + b + bin_equi
                            else:
                                error_on_line = str(find_line_number_2(str(sub_line[2] + sub_line[3] + sub_line[4]), lines) - 1)
                                print("error at line " + error_on_line + ". invalid immediate value used!!")

                                error_counter = error_counter + 1

                        else:
                            error_on_line = str(find_line_number_2(str(sub_line[2] + sub_line[3] + sub_line[4]), lines) - 1)
                            print("error at line " + error_on_line + ". invalid register used!")

                            error_counter = error_counter + 1

                    elif (to_find == "not"):
                        syntax_check = check_valid_reg_name((sub_line[3])) and check_valid_reg_name((sub_line[4]))
                        if (syntax_check):

                            a = str(opcodes[instruction])
                            b = "00000"
                            c = register[sub_line[3]]
                            d = register[sub_line[4]]
                            line[i] = a + b + c + d

                        else:
                            error_on_line = str(find_line_number_2(str(sub_line[2] + sub_line[3] + sub_line[4]), lines) - 1)
                            print("error at line " + error_on_line + ". invalid register used!")

                            error_counter = error_counter + 1

                    elif (to_find == "cmp"):
                        syntax_check = check_valid_reg_name((sub_line[3])) and check_valid_reg_name((sub_line[4]))
                        if (syntax_check):
                            a = str(opcodes[instruction])
                            b = "00000"
                            c = register[sub_line[3]]
                            d = register[sub_line[4]]
                            line[i] = a + b + c + d

                        else:
                            error_on_line = str(find_line_number_2(str(sub_line[2] + sub_line[3] + sub_line[4]), lines) - 1)
                            print("error at line " + error_on_line + "invalid register used!")

                            error_counter = error_counter + 1

                elif(len(sub_line)==6):
                    if (instruction == "add"):
                        syntax_check = check_valid_reg_name((sub_line[3])) and check_valid_reg_name(
                            (sub_line[4])) and check_valid_reg_name((sub_line[5]))
                        if (syntax_check):
                            a = str(opcodes[instruction])
                            b = "00"
                            c = register[sub_line[3]]
                            d = register[sub_line[4]]
                            e = register[sub_line[5]]
                            line[i] = a + b + c + d + e
                        else:
                            error_on_line = str(find_line_number_2(str(sub_line[2] + sub_line[3] + sub_line[4] + sub_line[5]),
                                                   lines) - 1)
                            print("error at line " + error_on_line + "invalid register used!")

                            error_counter = error_counter + 1



                    elif (instruction == "sub"):
                        syntax_check = check_valid_reg_name((sub_line[3])) and check_valid_reg_name(
                            (sub_line[4])) and check_valid_reg_name((sub_line[5]))
                        if (syntax_check):
                            a = str(opcodes[instruction])
                            b = "00"
                            c = register[sub_line[3]]
                            d = register[sub_line[4]]
                            e = register[sub_line[5]]
                            line[i] = a + b + c + d + e
                        else:
                            error_on_line = str(find_line_number_2(str(sub_line[2] + sub_line[3] + sub_line[4] + sub_line[5]),
                                                   lines) - 1)
                            print("error at line " + error_on_line + "invalid register used!")

                            error_counter = error_counter + 1




                    elif (to_find == "mul"):
                        syntax_check = check_valid_reg_name((sub_line[3])) and check_valid_reg_name(
                            (sub_line[4])) and check_valid_reg_name((sub_line[5]))
                        if (syntax_check):
                            a = str(opcodes[instruction])
                            b = "00"
                            c = register[sub_line[3]]
                            d = register[sub_line[4]]
                            e = register[sub_line[5]]
                            line[i] = a + b + c + d + e
                        else:
                            error_on_line = str(
                                find_line_number_2(str(sub_line[2] + sub_line[3] + sub_line[4] + sub_line[5]),
                                                   lines) - 1)
                            print("error at line " + error_on_line + "invalid register used!")

                            error_counter = error_counter + 1



                    elif (to_find == "xor"):
                        syntax_check = check_valid_reg_name((sub_line[3])) and check_valid_reg_name(
                            (sub_line[4])) and check_valid_reg_name((sub_line[5]))
                        if (syntax_check):
                            a = str(opcodes[instruction])
                            b = "00"
                            c = register[sub_line[3]]
                            d = register[sub_line[4]]
                            e = register[sub_line[5]]
                            line[i] = a + b + c + d + e
                        else:
                            error_on_line = str(
                                find_line_number_2(str(sub_line[2] + sub_line[3] + sub_line[4] + sub_line[5]),
                                                   lines) - 1)
                            print("error at line " + error_on_line + "invalid register used!")

                            error_counter = error_counter + 1


                    elif (to_find == "or"):
                        syntax_check = check_valid_reg_name((sub_line[3])) and check_valid_reg_name(
                            (sub_line[4])) and check_valid_reg_name((sub_line[5]))
                        if (syntax_check):
                            a = str(opcodes[instruction])
                            b = "00"
                            c = register[sub_line[3]]
                            d = register[sub_line[4]]
                            e = register[sub_line[5]]
                            line[i] = a + b + c + d + e
                        else:
                            error_on_line = str(
                                find_line_number_2(str(sub_line[1] + sub_line[2] + sub_line[3] + sub_line[4]),
                                                   lines) - 1)
                            print("error at line " + error_on_line + "invalid register used!")

                            error_counter = error_counter + 1


                    elif (to_find == "and"):
                        syntax_check = check_valid_reg_name((sub_line[3])) and check_valid_reg_name(
                            (sub_line[4])) and check_valid_reg_name((sub_line[5]))
                        if (syntax_check):
                            a = str(opcodes[instruction])
                            b = "00"
                            c = register[sub_line[3]]
                            d = register[sub_line[4]]
                            e = register[sub_line[5]]
                            line[i] = a + b + c + d + e
                        else:
                            error_on_line = str(
                                find_line_number_2(str(sub_line[1] + sub_line[2] + sub_line[3] + sub_line[4]),
                                                   lines) - 1)
                            print("error at line " + error_on_line + "invalid register used!")

                            error_counter = error_counter + 1

if(error_counter==0):
    for i in range(len(line)):
        g=line[i].split()
        if(len(g)==1):
            print(g[0])

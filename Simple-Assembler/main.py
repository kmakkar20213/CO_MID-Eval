import sys
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

instruction_length ={ "add":"4" ,  "sub":"4" , "mov":"3", "mov_r": "3", "ld": "3" , "st": "3", "mul": "4",
 "div": "3",  "rs":"3", "ls": "3", "xor":"4", "or": "4", "and": "4", "not":"3",
 "cmp": "3",  "jmp": "2", "jlt": "2", "jgt": "2", "je": "2", "hlt": "1" }

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

        if(g[1]== "hlt" or (len(g)>2 and g[2]=="hlt" ) ):
            if(i==len(line)-1): #there was no variable, only instructions and hlt
                return True

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
         if(len(line)!=0 and line[0]!="var"): #if empty line then ignore
             index=i
             break

     if(index!=-1):
         for i in range(index+1, len(lines)):
             line=lines[i].split()
             if(len(line)!=0 and line[0]=="var"):
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
        elif(len(g)>2 and g[2]=="hlt"):
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


    a=line.split()


    for i in range(len(lines)):
        if(len(lines[i])!=0):
            g=lines[i].split()
            #print(g)
            if(g== a):
                break
            else:
                c=c+1
        else:
            c=c+1

    return c

def check_illegal_flag_use(lines):
     c = 0
     for i in range(len(lines)):

         if(len(lines[i])!=0):
             g=lines[i].split()
             if(g[0]!= "mov" and g[0] in opcodes.keys()):
                 if((len(g)>1 and g[1]=="FLAGS") or (len(g)>2 and g[2]=="FLAGS")):
                    print("illegal flag usage at line"+ str(i+1))
                    c=c+1

             elif(len(g)>2 and g[1]!="mov" and g[1] in opcodes.keys()):
                 if(g[2]=="FLAGS" or (len(g)>3 and g[3]=="FLAGS")):
                     print("illegal flag usage at line" + str(i + 1))
                     c=c+1

     return c

def check_arguments_after_instruction(lines):
    c=0
    for i in range(len(lines)):
        if (len(lines[i]) != 0):
            g = lines[i].split()
            if (g[0] in opcodes.keys()):
               a= int(instruction_length[g[0]])
               if((a)!=len(g)):
                   c=c+1
                   print("number of arguments required for instruction "+ g[0]+ " donot match syntax at line "+ str(i+1))

            elif(len(g)>1 and g[1] in opcodes.keys()):
                a = int(instruction_length[g[1]])
                if ((a+1) != len(g)):
                    c = c + 1
                    print("number of arguments required for instruction " + g[1] + " donot match syntax at line " + str(
                        i + 1))

    return c






error_counter=0
'''f= open(r"input.txt")'''
complete_input = sys.stdin.read()

lines=(complete_input.split("\n"))

'''lines=[]
while True:
    x= f.readline()  # this returns the each line that ends with /n , basically used to separate commands

    if not x:
        break
    lines.append(x.strip()) #store in a list the new lines, using strip to remove extra white spaces if any
f.close()
'''
line=[]
c=0


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
                        print("label not followed by valid command at line"+str(find_line_number(lines[i]) -1))
                        error_counter = error_counter + 1


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

        elif(x !="var"):
            line_number = str(find_line_number(lines[i]) -1)
            print("unidentified command: "+ str(x)+ " given at line "+ line_number)
            error_counter = error_counter + 1








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
            elif(x=="var" and t in var_dict.keys()):
                line_number=find_line_number(lines[i])
                print("error! trying to re-define a variable at line "+ str(line_number-1)) #re-defining of variables case
                error_counter = error_counter + 1

        elif(x=="var"):
            line_number = find_line_number(lines[i])
            print("error at line"+ str(line_number -1) + ". variable name not declared!")
            error_counter = error_counter + 1


if(error_counter==0):
#check for variables in beginning
    var_in_beg= check_var_in_begin(lines)
    if(var_in_beg==False):
        print("error! variables not defined in beginning!")
        error_counter=error_counter+1

if(error_counter==0):
#checks for multiple hlts
    halt_checker1= count_multiple_hlt(line)
    if(halt_checker1==0):
        print("error! missing hlt")
        error_counter = error_counter + 1
    elif(halt_checker1>1):
        print("error! multiple hlts used")
        error_counter = error_counter + 1

    if(halt_checker1==1):

        halt_checker2= check_if_hlt_last(line)
        if(not halt_checker2):
            print("error! hlt is not last instruction")
            error_counter = error_counter + 1

#check for invalid flag use
if(error_counter==0):
    error_counter=error_counter + check_illegal_flag_use(lines)
    error_counter=error_counter + check_arguments_after_instruction(lines)

#check
if(error_counter==0):

    for i in range (len(line)):


        sub_line= line[i].split()
        to_find = sub_line[1]


        if(to_find=="hlt"):  #instruction-1
            if(len(sub_line) == 2):
                sub_line[1] = "1001100000000000"
                line[i] = sub_line[1]



        elif(to_find == "jgt" or to_find == "je" or to_find == "jmp" or to_find == "jlt"): #instruction-2,3,4,5
            op_code_value = opcodes[to_find]
            if (len(sub_line) == 3):
                syntax_check = check_undefined_labels(sub_line[2])

                if (syntax_check):
                    line[i] = str(op_code_value) + "000" + length_adjuster(str(decimalToBinary(int(label_dict[sub_line[2]]))))
                elif (to_find != "var"):
                    error_on_line= str(find_line_number_2(str(sub_line[1]+" "+ sub_line[2]), lines))
                    print("error at line" + error_on_line+  "." + sub_line[2]+ " has not been defined as a label. ")
                    error_counter = error_counter + 1



        elif(to_find== "mov"): #instruction-6,7
            if (len(sub_line) == 4):
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
            if (len(sub_line) == 4):
                a = str(opcodes[to_find])  # opcode ka binary

                syntax_check = sub_line[2]!= "FLAGS" and check_valid_reg_name((sub_line[2])) and check_undefined_variables(sub_line[3])

                if (syntax_check):
                    b = register[sub_line[2]]  # pass register value to get its binary

                    c = length_adjuster(str(decimalToBinary(int(var_dict[sub_line[3]]))))
                    line[i] = a + b + c
                else:

                    error_on_line = str(find_line_number_2(str(sub_line[1] +" "+  sub_line[2] +" "+ sub_line[3]), lines))
                    if(not check_valid_reg_name((sub_line[2]))):
                        print("error at line " + error_on_line+ ". invalid register used")
                        error_counter = error_counter + 1

                    elif(not check_undefined_variables(sub_line[3])):
                        print("error at line " + error_on_line + " variable used has not been defined!")
                        error_counter = error_counter + 1






        elif (to_find == "st"): #instruction-9
            if (len(sub_line) == 4):
                a = str(opcodes[to_find])
                syntax_check = sub_line[2]!= "FLAGS" and check_valid_reg_name((sub_line[2])) and check_undefined_variables(sub_line[3])
                if (syntax_check):
                    b = register[sub_line[2]]
                    # print(sub_line[3])
                    c = length_adjuster(str(decimalToBinary(int(var_dict[sub_line[3]]))))
                    line[i] = a + b + c
                else:
                    error_on_line = str(find_line_number_2(str(sub_line[1] +" "+ sub_line[2] +" "+ sub_line[3]), lines))
                    if (not check_valid_reg_name((sub_line[2]))):
                        print("error at line " + error_on_line + ". invalid register used")
                        error_counter = error_counter + 1

                    elif (not check_undefined_variables(sub_line[3])):
                        print("error at line " + error_on_line + " variable used has not been defined!")
                        error_counter = error_counter + 1




        elif (to_find == "div"): #instruction-10
            if(len(sub_line)==4):
                a = str(opcodes[to_find])
                b = "00000"
                syntax_check = sub_line[2]!= "FLAGS" and check_valid_reg_name((sub_line[2])) and check_valid_reg_name((sub_line[3]))
                if (syntax_check):
                    c = sub_line[2]
                    d = sub_line[3]
                    line[i] = a + b + c + d
                else:
                    error_on_line = str(find_line_number_2(str(sub_line[1] + " "+ sub_line[2] + " "+ sub_line[3]), lines) - 1)
                    print("error at line " + error_on_line+ ". invalid register used!")
                    error_counter = error_counter + 1



        elif (to_find == "rs"): #instruction-11
            if (len(sub_line) == 4):
                a = str(opcodes[to_find])
                syntax_check = sub_line[2]!= "FLAGS" and check_valid_reg_name((sub_line[2]))
                if (syntax_check):
                    b = register[sub_line[2]]

                    remove_dollar = int(sub_line[3][1:len(sub_line[3])])  # omit the dollar sign
                    if (check_illegal_immediate_value(remove_dollar)):
                        bin_equi = length_adjuster(str(decimalToBinary(remove_dollar)))

                        line[i] = a + b + bin_equi
                    else:
                        error_on_line = str(find_line_number_2(str(sub_line[1] +" "+ sub_line[2] +" "+ sub_line[3]), lines) - 1)
                        print("error at line " + error_on_line + ". invalid immediate value used!!")

                        error_counter = error_counter + 1
                else:
                    error_on_line = str(find_line_number_2(str(sub_line[1] + " "+sub_line[2] + " "+sub_line[3]), lines) - 1)
                    print("error at line " + error_on_line + ". invalid register used!")
                    error_counter = error_counter + 1



        elif (to_find == "ls"): #instruction-12
            if (len(sub_line) == 4):
                a = str(opcodes[to_find])
                syntax_check = sub_line[2]!= "FLAGS" and check_valid_reg_name((sub_line[2]))
                if (syntax_check):

                    b = register[sub_line[2]]

                    remove_dollar = int(sub_line[3][1:len(sub_line[3])])  # omit the dollar sign
                    if (check_illegal_immediate_value(remove_dollar)):
                        bin_equi = length_adjuster(str(decimalToBinary(remove_dollar)))

                        line[i] = a + b + bin_equi
                    else:
                        error_on_line = str(find_line_number_2(str(sub_line[1] +" "+ sub_line[2] +" "+ sub_line[3]), lines) - 1)
                        print("error at line " + error_on_line + ". invalid immediate value used!!")
                        error_counter = error_counter + 1

                else:
                    error_on_line = str(find_line_number_2(str(sub_line[1] +" "+ sub_line[2] +" "+ sub_line[3]), lines) - 1)
                    print("error at line " + error_on_line +". invalid register used!")
                    error_counter = error_counter + 1



        elif (to_find == "not"): #instruction-13
            if (len(sub_line) == 4):
                syntax_check = sub_line[2]!= "FLAGS" and sub_line[3]!= "FLAGS" and check_valid_reg_name((sub_line[2])) and check_valid_reg_name((sub_line[3]))
                if (syntax_check):

                    a = str(opcodes[to_find])
                    b = "00000"
                    c = register[sub_line[2]]
                    d = register[sub_line[3]]
                    line[i] = a + b + c + d

                else:
                    error_on_line = str(find_line_number_2(str(sub_line[1] +" "+ sub_line[2] +" "+ sub_line[3]), lines) - 1)
                    print("error at line " + error_on_line + ". invalid register used!")
                    error_counter = error_counter + 1


        elif (to_find == "cmp"): #instruction-14
            if (len(sub_line) == 4):
                syntax_check = sub_line[2]!= "FLAGS" and sub_line[3]!= "FLAGS" and check_valid_reg_name((sub_line[2])) and check_valid_reg_name((sub_line[3]))
                if (syntax_check):
                    a = str(opcodes[to_find])
                    b = "00000"
                    c = register[sub_line[2]]
                    d = register[sub_line[3]]
                    line[i] = a + b + c + d

                else:
                    error_on_line = str(find_line_number_2(str(sub_line[1] + " "+sub_line[2] +" "+ sub_line[3]), lines) - 1)
                    print("error at line " + error_on_line + "invalid register used!")
                    error_counter = error_counter + 1




        elif(to_find == "add"): #instruction-15
            if (len(sub_line) == 5):
                    syntax_check = check_valid_reg_name((sub_line[2])) and check_valid_reg_name((sub_line[3])) and check_valid_reg_name((sub_line[4]))
                    if (syntax_check):
                        a = str(opcodes[to_find])
                        b="00"
                        c=register[sub_line[2]]
                        d=register[sub_line[3]]
                        e=register[sub_line[4]]
                        line[i] = a + b + c + d + e

                    else:

                            error_on_line = str(find_line_number_2(str(sub_line[1] +" "+ sub_line[2] + " "+sub_line[3]+ sub_line[4]), lines) - 1)
                            print("error at line " + error_on_line + "invalid register used!")
                            error_counter = error_counter + 1


        elif (to_find == "sub"): #instruction-16
            if (len(sub_line) == 5):
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

                        error_on_line = str(find_line_number_2(str(sub_line[1] +" "+ sub_line[2] +" "+ sub_line[3] +" "+ sub_line[4]), lines) - 1)
                        print("error at line " + error_on_line + "invalid register used!")

                        error_counter = error_counter + 1





        elif (to_find == "mul"): #instruction-17
            if (len(sub_line) == 5):
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

                    if (len(sub_line) == 5):
                        error_on_line = str(find_line_number_2(str(sub_line[1] +" "+ sub_line[2] +" "+ sub_line[3] +" "+ sub_line[4]), lines) - 1)
                        print("error at line " + error_on_line + "invalid register used!")
                        error_counter = error_counter + 1




        elif (to_find == "xor"): #instruction-18
            if (len(sub_line) == 5):
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
                    if (len(sub_line) == 5):
                        error_on_line = str(find_line_number_2(str(sub_line[1] + " "+sub_line[2] +" "+ sub_line[3] +" "+ sub_line[4]), lines) - 1)
                        print("error at line " + error_on_line + "invalid register used!")
                        error_counter = error_counter + 1




        elif (to_find == "or"): #instruction-19
            if (len(sub_line) == 5):
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

                        error_on_line = str(find_line_number_2(str(sub_line[1] + " "+sub_line[2] + " "+sub_line[3] +" "+ sub_line[4]), lines) - 1)
                        print("error at line " + error_on_line + "invalid register used!")



        elif (to_find == "and"): #instruction-20
            if (len(sub_line) == 5):
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
                    if (len(sub_line) == 5):
                        error_on_line = str(find_line_number_2(str(sub_line[1] +" "+ sub_line[2] + " "+sub_line[3] +" "+ sub_line[4]), lines) - 1)
                        print("error at line " + error_on_line + "invalid register used!")


        elif(to_find in label_dict.keys()): # this check if instruction after label is valid or not
            instruction= sub_line[2]

            op_code_value=opcodes[instruction]

            if(len(sub_line)==3):
                    if(instruction=="hlt"):
                        # this instruction is halt
                        line[i] = "1001100000000000"



            elif (len(sub_line) == 4):
                    # this is either of the jump instructions
                    if (instruction == "jmp" or instruction == "jlt" or instruction == "jgt" or instruction == "je" ):
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
                                    error_on_line = str(find_line_number_2(sub_line[1] +": "+str(sub_line[2] + " "+sub_line[3] +" "+ sub_line[4]),
                                                           lines) - 1)

                                    print("error at line " + error_on_line + "illegal immediate value used for register!")
                                    error_counter = error_counter + 1
                            else:
                                #print(line[i])
                                error_on_line = str(find_line_number_2(sub_line[1] +": "+ str(sub_line[2] +" "+ sub_line[3] + " "+sub_line[4]), lines) - 1)
                                print("error at line " + error_on_line + " invalid register used")

                                error_counter = error_counter + 1

                        else:
                            #a=(sub_line[1] +": "+sub_line[2] +" "+ sub_line[3] +" "+ sub_line[4])
                            #print(a.split())

                            error_on_line = str(find_line_number_2(str(sub_line[1] +": "+sub_line[2] +" "+ sub_line[3] +" "+ sub_line[4]), lines))
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
                            error_on_line = str(find_line_number_2(str(sub_line[1] +": "+sub_line[2] +" "+ sub_line[3] + " "+sub_line[4]), lines) - 1)
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
                            error_on_line = str(find_line_number_2(str(sub_line[1] +": "+ sub_line[2] +" "+ sub_line[3] +" "+ sub_line[4]), lines) - 1)
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
                            error_on_line = str(find_line_number_2(str(sub_line[1] +": "+ sub_line[2] +" "+ sub_line[3] +" "+ sub_line[4]), lines) - 1)
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
                                error_on_line = str(find_line_number_2(str(sub_line[1] +": "+ sub_line[2] +" "+ sub_line[3] + " "+sub_line[4]), lines) - 1)
                                print("error at line " + error_on_line + ". invalid immediate value used!!")

                                error_counter = error_counter + 1
                        else:
                            error_on_line = str(find_line_number_2(str(sub_line[1] +": "+ sub_line[2] +" "+ sub_line[3] +" "+ sub_line[4]), lines) - 1)
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
                                error_on_line = str(find_line_number_2(str(sub_line[1] +": "+ sub_line[2] +" "+ sub_line[3] +" "+ sub_line[4]), lines) - 1)
                                print("error at line " + error_on_line + ". invalid immediate value used!!")

                                error_counter = error_counter + 1

                        else:
                            error_on_line = str(find_line_number_2(str(sub_line[1] +": "+ sub_line[2] + " "+sub_line[3] +" "+ sub_line[4]), lines) - 1)
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
                            error_on_line = str(find_line_number_2(str(sub_line[1] +": "+ sub_line[2] +" "+ sub_line[3] +" "+ sub_line[4]), lines) - 1)
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
                            error_on_line = str(find_line_number_2(str(sub_line[1] +": "+ sub_line[2] +" "+ sub_line[3] + " "+sub_line[4]), lines) - 1)
                            print("error at line " + error_on_line + "invalid register used!")

                            error_counter = error_counter + 1
                    else:
                        print("invalid syntax given for instruction"+ instruction)
                        error_counter=error_counter+1

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
                            error_on_line = str(find_line_number_2(str(sub_line[1] +": "+ sub_line[2] + " "+sub_line[3] +" "+ sub_line[4] + " "+sub_line[5]),
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
                            error_on_line = str(find_line_number_2(str(sub_line[1] +": "+ sub_line[2] +" "+ sub_line[3] +" "+ sub_line[4] +" "+ sub_line[5]),
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
                                find_line_number_2(str(sub_line[1] +": "+ sub_line[2] +" "+ sub_line[3] +" "+ sub_line[4] +" "+ sub_line[5]),
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
                                find_line_number_2(str(sub_line[1] +": "+ sub_line[2] +" "+ sub_line[3] +" "+ sub_line[4] +" "+ sub_line[5]),
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
                                find_line_number_2(str(sub_line[1] +": "+ sub_line[2] +" "+ sub_line[3] +" "+ sub_line[4]),
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
                                find_line_number_2(str(sub_line[1] +": "+ sub_line[2] +" "+ sub_line[3] +" "+ sub_line[4]),
                                                   lines) - 1)
                            print("error at line " + error_on_line + "invalid register used!")

                            error_counter = error_counter + 1
                    else:
                        print("invalid syntax given for instruction " + instruction)
                        error_counter=error_counter+1




if(error_counter==0):
    for i in range(len(line)):
        g=line[i].split()
        if(len(g)==1):
            print(g[0])

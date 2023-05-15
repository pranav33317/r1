operations={"add":"00000","sub":"00001","movimm":"00010","movreg":"00011","ld":"00100","st":"00101","mul":"00110",
            "div":"00111","rs":"01000","ls":"01001","xor":"01010","or":"01011","and":"01100","not":"01101",
            "cmp":"01110","jmp":"01111","jlt":"11100","jgt":"11101","je":"11111","hlt":"11010","mov":"0"}
registers={"R0":"000","R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110","FLAGS":"111"}
A=["add","sub","mul","xor","or","and"]
B=["movimm","rs","ls"]
C=["movreg","div","not","cmp"]
D=["ld","st"]
E=["jmp","jlt","jgt","je"]
F=["hlt"]
R0=["0"]*16
R1=["0"]*16
R2=["0"]*16
R3=["0"]*16
R4=["0"]*16
R5=["0"]*16
R6=["0"]*16
FLAGS=["0"]*16
variables={}
f=open("textfile.txt")
f2=open("outfile.txt","w+")
L1=f.readlines()
L2=[]
labels={}
#labels_values
variables_list=[]
write_list=[]
print(L1)
if len(L1)>128:
    f2.write("Instructions exceed memory limit")
    exit()
var_flag=0
for i in range(len(L1)):
    if L1[i]=="\n":
       pass
    else:
        if ((L1[i]).strip()).split()[0][-1]==":":
            var_flag=1
            labels[((L1[i].strip()).split()[0])[:-1]]=str(format(i,f'0{7}b'))
            L2.append(((((L1[i]).strip()).split())[1:]))
        elif (((L1[i]).strip()).split())[0]=="var":
            if var_flag==0:
                variables_list.append(((L1[i].strip()).split())[1])
            else:
                f2.write("Variable not declared at start in line number"+str(i))
                exit()
        elif ((L1[i]).strip()).split()[0] in operations:
            var_flag=1
            L2.append((L1[i].strip()).split())
        elif ((L1[i]).strip()).split()[0][-1]!=":" or ((L1[i]).strip()).split()[0] not in operations or ((L1[i]).strip()).split()[0]!="var":
            f2.write("Keyword not recognized")
            exit()
if ["hlt"] not in L2:
    f2.write("Halt missing")
    exit()
if L2[-1][0]!="hlt":
    f2.write("Halt must be last instruction")
    exit()
variables_list.append("")
for i in range(len(variables_list)):
    L2.append("")
    L2[len(L2)-1]=variables_list[i]
    variables[variables_list[i]]=L2.index(variables_list[i])
L2.pop(len(L2)-1)
print(L2)
if len(L2)>128:
    f2.write("Memory limit exceeded")
    exit()
print(labels)
for i in range(len(L2)):
    if L2[i][0] not in operations:
        f2.write("Typo in operation at line number"+str(i))
        exit()
    if L2[i][0]=="hlt":
        write_list.append(operations[L2[i][0]]+("0"*11))
        break
    elif L2[i][0]=="jmp":
        temp=i
        if L2[i][1] in variables_list:
            if L2[i][1] not in labels:
                f2.write("Variable used as label at line number"+str(i))
                exit()
        if L2[i][1] not in list(labels.keys()):
            f2.write("Undefined label used at line number"+str(i))
            exit()
        num=int(labels[L2[i][1]])
        i=num
        write_list.append(operations[L2[temp][0]]+("0"*4)+labels[L2[temp][1]])
        write_list.append("\n")
    elif L2[i][0]=="jlt":
        temp=i
        if L2[i][1] in variables_list:
            if L2[i][1] not in labels:
                f2.write("Variable used as label at line number"+str(i))
                exit()
        if L2[i][1] not in list(labels.keys()):
            f2.write("Undefined label used at line number"+str(i))
            exit()
        if FLAGS[13]=="1":
            num=int(labels[L2[i][1]])
            i=num
        num_bin_str=str(format(num,f'0{7}b'))
        write_list.append(operations[L2[temp][0]]+("0"*4)+labels[L2[temp][1]])
        write_list.append("\n")
    elif L2[i][0]=="jgt":
        temp=i
        if L2[i][1] in variables_list:
            if L2[i][1] not in labels:
                f2.write("Variable used as label at line number"+str(i))
                exit()
        if L2[i][1] not in labels:
            f2.write("Undefined label used at line number"+str(i))
            exit()
        if FLAGS[14]=="1":
            num=int(labels[L2[i][1]])
            i=num
        num_bin_str=str(format(num,f'0{7}b'))
        write_list.append(operations[L2[temp][0]]+("0"*4)+labels[L2[temp][1]])
        write_list.append("\n")
    elif L2[i][0]=="je":
        temp=i
        if L2[i][1] in variables_list:
            if L2[i][1] not in labels:
                f2.write("Variable used as label at line number"+str(i))
                exit()
        if L2[i][1] not in labels:
            f2.write("Undefined label used at line number"+str(i))
            exit()
        if FLAGS[15]=="1":
            num=int(labels[L2[i][1]])
            i=num
        num_bin_str=str(format(num,f'0{7}b'))
        write_list.append(operations[L2[temp][0]]+("0"*4)+labels[L2[temp][1]])
        write_list.append("\n")
    elif L2[i][0] in A:
        str1=eval(L2[i][1])
        str2=eval(L2[i][2])
        str3=eval(L2[i][3])
        if L2[i][1] not in registers:
            f2.write("Typo in register name at line number"+str(i))
            exit()
        if str1 is FLAGS:
            f2.write("Illegal use of FLAGS register at line number"+str(i))
            exit()
        str1eval=""
        str2eval=""
        str3eval=""
        for j in str1:
            str1eval+=j
        for j in str2:
            str2eval+=j
        for j in str3:
            str3eval+=j
        num1=int(str1eval,2)
        num2=int(str2eval,2)
        num3=int(str3eval,2)
        if L2[i][0]=="add":
            num1=num2+num3
            if num1>127:
                num1=0
                FLAGS[12]=1
        elif L2[i][0]=="sub":
            num1=num2-num3
            if num1<0:
                num1=0
                FLAGS[12]=1
        elif L2[i][0]=="mul":
            num1=num2*num3
            if num1>127:
                num1=0
                FLAGS[12]=1
        elif L2[i][0]=="xor":
            num1=num2^num3
        elif L2[i][0]=="or":
            num1=num2|num3
        elif L2[i][0]=="and":
            num1=num2&num3
        str1val=str(format(num1,f'0{7}b'))
        str1val=list(str1val)
        str1[9:]=str1val
        write_list.append(operations[L2[i][0]]+("0"*2)+registers[str(L2[i][1])]+registers[str(L2[i][2])]+registers[str(L2[i][3])])
        write_list.append("\n")
    elif L2[i][0]=="cmp":
        str1=eval(L2[i][1])
        str2=eval(L2[i][2])
        if L2[i][1] not in registers:
            f2.write("Typo in register name at line number"+str(i))
            exit()
        if L2[i][2] not in registers:
            f2.write("Typo in register name at line number"+str(i))
            exit()
        if str1 is FLAGS:
            f2.write("Illegal use of FLAGS register at line number"+str(i))
            exit()
        if str2 is FLAGS:
            f2.write("Illegal use of FLAGS register at line number"+str(i))
            exit()
        str1eval=""
        str2eval=""
        for j in str1:
            str1eval+=j
        for j in str2:
            str2eval+=j
        num1=int(str1eval,2)
        num2=int(str2eval,2)
        if num1>num2:
            FLAGS[14]="1"
        elif num1<num2:
            FLAGS[13]="1"
        elif num1==num2:
            FLAGS[15]="1"
        write_list.append(operations[L2[i][0]]+("0"*5)+registers[str(L2[i][1])]+registers[str(L2[i][2])])
        write_list.append("\n")
    elif L2[i][0]=="not":
        str1=eval(L2[i][1])
        str2=eval(L2[i][2])
        if L2[i][1] not in registers:
            f2.write("Typo in register name at line number"+str(i))
            exit()
        if L2[i][2] not in registers:
            f2.write("Typo in register name at line number"+str(i))
            exit()
        if str1 is FLAGS:
            f2.write("Illegal use of FLAGS register at line number"+str(i))
            exit()
        if str2 is FLAGS:
            f2.write("Illegal use of FLAGS register at line number"+str(i))
            exit()
        str2eval=""
        for i in str2:
            str2eval+=i
        num1=int(str2eval,2)
        size=7
        max=(2**size)-1
        num1=max-num2
        str1eval=str(format(num2,f'0{7}b'))
        str1eval=list(str2eval)
        str1[9:]=str1eval
        write_list.append(operations[L2[i][0]]+("0"*5)+str(L2[i][1])+str(L2[i][2]))
        write_list.append("\n")
    elif L2[i][0]=="rs":
        str1=eval(L2[i][1])
        if L2[i][1] not in registers:
            f2.write("Typo in register name at line number"+str(i))
            exit()
        if str1 is FLAGS:
            f2.write("Illegal use of FLAGS register at line number"+str(i))
            exit()
        num1=int(L2[i][2])
        if num1>127:
            f2.write("Illegal immediate value at line number"+str(i))
            exit()
        num1val=str(format(num1,f'0{7}b'))
        num1val=list(num1val)
        str1[7:16]=str1[0:9]
        str1[0:7]=num1val
        num_bin_str=""
        for j in num_bin:
            num_bin_str+=j
        write_list.append(operations[L2[i][0]]+"0"+str(L2[i][1])+str(num_bin_str))
        write_list.append("\n")
    elif L2[i][0]=="ls":
        str1=eval(L2[i][1])
        if L2[i][1] not in registers:
            f2.write("Typo in register name at line number"+str(i))
            exit()
        if str1 is FLAGS:
            f2.write("Illegal use of FLAGS register at line number"+str(i))
            exit()
        num1=int(L2[i][2])
        if num1>127:
            f2.write("Illegal immediate value at line number"+str(i))
            exit()
        num1val=str(format(num1,f'0{7}b'))
        num1val=list(num1val)
        str1[0:9]=str1[7:16]
        str1[9:16]=num1val
        num_bin_str=""
        for j in num1val:
            num_bin_str+=j
        write_list.append(operations[L2[i][0]]+"0"+str(L2[i][1])+str(num_bin_str))
        write_list.append("\n")
    elif L2[i][0]=="div":
        str1=eval(L2[i][1])
        str2=eval(L2[i][2])
        if L2[i][1] not in registers:
            f2.write("Typo in register name at line number"+str(i))
            exit()
        if L2[i][2] not in registers:
            f2.write("Typo in register name at line number"+str(i))
            exit()
        if str1 is FLAGS:
            f2.write("Illegal use of FLAGS register at line number"+str(i))
            exit()
        if str2 is FLAGS:
            f2.write("Illegal use of FLAGS register at line number"+str(i))
            exit()
        str1eval=""
        str2eval=""
        for i in str1:
            str1eval+=i
        for i in str2:
            str2eval+=i
        num1=int(str1eval,2)
        num2=int(str2eval,2)
        if num2==0:
            quot=0
            rem=0
            quot_bin=str(format(quot,f'0{7}b'))
            rem_bin=str(format(rem,f'0{7}b'))
            quot_bin=list(quot_bin)
            rem_bin=list(rem_bin)
            R1[9:]=quot_bin
            R2[9:]=rem_bin
        else:
            quot=num1//num2
            rem=num1%num2
            quot_bin=str(format(quot,f'0{7}b'))
            rem_bin=str(format(rem,f'0{7}b'))
            quot_bin=list(quot_bin)
            rem_bin=list(rem_bin)
            R1[9:]=quot_bin
            R2[9:]=rem_bin
        write_list.append(operations[L2[i][0]]+("0"*5)+str(L2[i][1])+str(L2[i][2]))
        write_list.append("\n")
    elif L2[i][0]=="mov":
        if L2[i][2] in list(registers.keys()):
            str1=eval(L2[i][1])
            str2=eval(L2[i][2])
            if L2[i][1] not in registers:
                f2.write("Typo in register name at line number"+str(i))
                exit()
            if L2[i][2] not in registers:
                f2.write("Typo in register name at line number"+str(i))
                exit()
            if str1 is FLAGS:
                f2.write("Illegal use of FLAGS register at line number"+str(i))
                exit()
            str1=str2.copy()
            write_list.append(operations[(L2[i][0]+"reg")]+("0"*5)+registers[str(L2[i][1])]+registers[str(L2[i][2])])
            write_list.append("\n")
        else:
            str1=eval(L2[i][1])
            if L2[i][1] not in registers:
                f2.write("Typo in register name at line number"+str(i))
                exit()
            if str1 is FLAGS:
                f2.write("Illegal use of FLAGS register at line number"+str(i))
                exit()
            num=int(L2[i][2][1:])
            if num>127:
                f2.write("Illegal immediate value at line number"+str(i))
                exit()
            num_bin=str(format(num,f'0{7}b'))
            num_bin=list(num_bin)
            str1[9:]=num_bin
            num_bin_str=""
            for j in num_bin:
                num_bin_str+=j
            write_list.append(operations[(L2[i][0]+"imm")]+"0"+str(registers[str(L2[i][1])])+str(num_bin_str))
            write_list.append("\n")
    elif L2[i][0]=="ld":
        str1=eval(L2[i][1])
        if L2[i][1] not in registers:
                f2.write("Typo in register name at line number"+str(i))
                exit()
        if str1 is FLAGS:
            f2.write("Illegal use of FLAGS register at line number"+str(i))
            exit()
        try:
            num2=variables[L2[i][2]]
        except:
            if L2[i][2] in labels:
                f2.write("Label used in place of variable")
                exit()
            else:
                f2.write("Undefined variable used")
                exit()
        #value=L2[num2]
        value_bin=str(format(num2,f'0{7}b'))
        #value_bin=list(value_bin)
        #str1[9:]=value_bin
        write_list.append(operations[L2[i][0]]+"0"+registers[str(L2[i][1])]+str(value_bin))
        write_list.append("\n")
    elif L2[i][0]=="st":
        str1=eval(L2[i][1])
        if L2[i][1] not in registers:
            f2.write("Typo in register name at line number"+str(i))
            exit()
        if str1 is FLAGS:
            f2.write("Illegal use of FLAGS register at line number"+str(i))
            exit()
        try:
            num2=variables[L2[i][2]]
        except:
            if L2[i][2] in labels:
                f2.write("Label used in place of variable")
                exit()
            else:
                f2.write("Undefined variable used")
                exit()
        #value=L2[num2]
        #str1eval=""
        #for i in str1:
        #    str1eval+=i
        #value=int(str1eval,2)
        value_bin=str(format(num2,f'0{7}b'))
        #L2[num2]=value_bin
        write_list.append(operations[L2[i][0]]+"0"+registers[str(L2[i][1])]+str(value_bin))
        write_list.append("\n")
f.close()
f2.writelines(write_list)
f2.close()

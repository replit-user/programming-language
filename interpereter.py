from sys import argv
path=argv[1]
program=[]
jump_occured=False
class STACK:
    def __init__(self,size:int):
        self.size=int(size)
        self.sp=0
        self.memmory=[0 for _ in range(size)]
    def push(self,number):
        self.sp+=1
        self.memmory[self.sp]=float(number)
        if self.sp>self.size:
            return OverflowError("overflow error")
    def pop(self):
        number=self.memmory[self.sp]
        self.memmory[self.sp]=0
        self.sp-=1
        if self.sp<0:
            raise OverflowError("underflow error")
        return number
    def top(self):
        return self.memmory[self.sp]
mem=STACK(32)
i=0
def execute(instruction:str):
    if "#" in instruction and not instruction.startswith("#"):
        execute(instruction.split("#")[0])
    elif instruction.startswith("#"):
        return None
    global i
    if instruction in ["MUL","DIV","SUB","ADD"]:
        a=mem.pop()
        b=mem.pop()
        jump_occured=False
        if instruction=="MUL":
            mem.push(a*b)
        elif instruction=="DIV":
            if not a==0:
                mem.push(b/a)
            else:
                raise ZeroDivisionError("division by 0 error")
        elif instruction=="SUB":
            mem.push(b-a)
        elif instruction=="ADD":
            mem.push(a+b)
    elif instruction=="POP":
        mem.pop()
        jump_occured=False
    elif instruction.startswith("PUSH "):
        number=instruction.removeprefix("PUSH ")
        mem.push(number)
        jump_occured=False
    elif instruction=="OUTV":
        print(mem.top())
        jump_occured=False
    elif instruction.startswith("OUT "):
        string=instruction.removeprefix("OUT ")
        print(string)
        jump_occured=False
    elif instruction.startswith("JMP.EQ."):
        number=int(instruction.split(".")[2].split(" ")[0])
        line=int(instruction.split(" ")[1])
        jump_occured=False
        if mem.top()==number:
            i=line
            jump_occured=True
    elif instruction.startswith("JMP.GT."):
        number=int(instruction.split(".")[2].split(" ")[0])
        line=int(instruction.split(" ")[1])
        jump_occured=False
        if mem.top()<number:
            i=line
            jump_occured=True
    elif instruction.startswith("JMP.LT."):
        number=int(instruction.split(".")[2].split(" ")[0])
        line=int(instruction.split(" ")[1])
        jump_occured=False
        if mem.top()>number:
            i=line
            jump_occured=True
    elif instruction=="HALT":
        exit()
    elif instruction=="READ":
        number=float(input())
        mem.push(number)
        jump_occured=False
    elif instruction.startswith("JMP "):
        number=instruction.split(" ")[1]
        i=int(number)
        jump_occured=True
    else:
        return None
with open(f"{path}.oll","r") as f:
    program=[line.strip() for line in f.readlines()]
while i<len(program):
    execute(program[i])
    if jump_occured==False:
        i+=1
    else:
        continue
    
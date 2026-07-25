# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
class stack():
    def __init__(self):
        self.val=[]
    def isempty(self):
        return len(self.val)==0
    def push(self,item):
        self.val.append(item)
    def top(self):
        return self.val[-1]
    def pop(self):
        del self.val[-1]

def operatorcheck():
    for i in range(len(exp)):
        if exp[i] not in ch:
            return 0
    return 1

def bracketcheck():
    bracket=stack()
    for i in range(len(exp)):
        if exp[i]=='(':
            bracket.push('(')
        if exp[i]==')':
            if bracket.isempty():
                return 0
            else:
                bracket.pop()
    if bracket.isempty():
        return 1
    else:
        return 0

def onlybracket():
    for i in range(len(exp)):
        if exp[i]!='(' and exp[i]!=')':
            return 0
    return 1
            
def cut():
    i=0
    while i<=len(exp)-1:
        if exp[i]=='*' or exp[i]=='/' or exp[i]=='(' or exp[i]==')':
            expression.append(exp[i])
            i+=1
            continue
        if exp[i]=='+' or exp[i]=='-':
            if i==0 or exp[i-1] not in ch[5:]:
                temp=''+exp[i]
                i+=1
                while i<=len(exp)-1 and exp[i] in ch[6:]:
                    temp=temp+exp[i]
                    i+=1
                expression.append(float(temp))
                continue
            else:
                expression.append(exp[i])
                i+=1
                continue
        if exp[i] in ch[6:]:
            temp=''
            while i<=len(exp)-1 and exp[i] in ch[6:]:
                temp=temp+exp[i]
                i+=1
            expression.append(float(temp))
            continue
def value(s,x,y):
    if s=='+':
        return x+y
    if s=='*':
        return x*y
    if s=='-':
        return x-y
    if s=='/':
        return x/y

def calc():
    operator=stack()
    operand=stack()
    for i in range(len(expression)):
        if expression[i] not in ch[0:6]:
            operand.push(expression[i])
        elif expression[i]=='(':
            operator.push('(')
        elif expression[i]==')':
            while operator.top()!='(':
                b=operand.top()
                operand.pop()
                a=operand.top()
                operand.pop()
                operand.push(value(operator.top(),a,b))
                operator.pop()
            operator.pop()
        elif expression[i] in ch[0:4]:
            while not operator.isempty() and prior[operator.top()]>=prior[expression[i]]:
                b=operand.top()
                operand.pop()
                a=operand.top()
                operand.pop()
                operand.push(value(operator.top(),a,b))
                operator.pop()
            operator.push(expression[i])
    while not operator.isempty():
        b=operand.top()
        operand.pop()
        a=operand.top()
        operand.pop()
        operand.push(value(operator.top(),a,b))
        operator.pop()
    print('{:.3f}'.format(operand.top()))
                
        
ch=['+','-','*','/','(',')','.','0','1','2','3','4','5','6','7','8','9']
prior={'*':3,'/':3,'+':2,'-':2,'(':1}
while True:
    s=list(map(str,input().split()))
    if s==["quit"]:
        break
    if len(s)==0:
        print("No expression.")
        continue
    exp=""
    for i in range(len(s)):
        exp=exp+s[i]
    if operatorcheck()==False:
        print("Unknown operator.")
        continue
    if bracketcheck()==False:
        print("Unmatched bracket.")
        continue
    if onlybracket()==True:
        print("No expression.")
        continue
    expression=[]
    try:
        cut()
        calc()
    except:
        print("Not implemented.")
        continue

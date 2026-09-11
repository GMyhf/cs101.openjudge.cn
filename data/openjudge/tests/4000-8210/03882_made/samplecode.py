import sys
MASK=0xffffffff
def i32(x):
    x &= MASK
    return x-0x100000000 if x >= 0x80000000 else x
def div0(a,b):
    q=abs(a)//abs(b)
    return -q if (a<0) != (b<0) else q
def evaluate(s):
    nums=[]; ops=[]; prec={'+':1,'-':1,'*':2,'/':2}
    def apply():
        op=ops.pop(); b=nums.pop(); a=nums.pop()
        nums.append(i32(a+b) if op=='+' else i32(a-b) if op=='-' else i32(a*b) if op=='*' else i32(div0(a,b)))
    i=0
    while i<len(s):
        c=s[i]
        if c.isdigit():
            x=0
            while i<len(s) and s[i].isdigit(): x=i32(x*10+ord(s[i])-48); i+=1
            nums.append(x); continue
        if c=='(': ops.append(c)
        elif c==')':
            while ops and ops[-1]!='(': apply()
            if ops: ops.pop()
        elif c in prec:
            while ops and ops[-1]!='(' and prec[ops[-1]]>=prec[c]: apply()
            ops.append(c)
        i+=1
    while ops: apply()
    return nums[-1]
def solve(text):
    v=text.split(); return ''.join(str(evaluate(v[i]))+'\n' for i in range(1,int(v[0])+1))
if __name__=='__main__': sys.stdout.write(solve(sys.stdin.read()))

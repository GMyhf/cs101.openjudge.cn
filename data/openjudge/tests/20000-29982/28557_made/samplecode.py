# T-004-r2 reference implementation
import sys
out=[]
for line in sys.stdin.read().splitlines()[1:]:
    a,b=map(int,line.split()); carry=0; count=0
    while a or b:
        carry,a,b=(a%10+b%10+carry)//10,a//10,b//10
        count += carry
    out.append(str(count))
print("\n".join(out))
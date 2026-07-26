# T-004-r3 reference implementation
import sys
lines=sys.stdin.read().splitlines()
while lines and not lines[-1].strip(): lines.pop()
n=len(lines)//2; rows=[]
for i in range(n):
    name=lines[2*i]; a=lines[2*i+1].split()
    ident,sex=a[0].split(","); age=a[1]
    rows.append((name, i, ident, sex, age))
for x in sorted(rows,key=lambda z:z[0].lower()):
    print(x[0]); print(f"{int(x[2]):08d},{x[3]} {x[4]}")

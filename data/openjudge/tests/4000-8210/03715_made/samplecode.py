# T-004-r3 reference implementation
import sys
from datetime import date
lines=sys.stdin.read().splitlines(); n=len(lines)-1; rows=[]
for i in range(n):
    parts=lines[1+i].split(); name=parts[0]; y,m,d,Y,M,D=map(int,parts[1:])
    rows.append((name,(date(Y,M,D)-date(y,m,d)).days+1,i,a[p-1-0] if False else ""))
for row in sorted(rows,key=lambda x:(-x[1],x[2])): print(row[0],row[1])
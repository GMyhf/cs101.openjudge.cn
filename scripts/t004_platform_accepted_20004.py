# External reference: cs101.openjudge.cn practice/20004 statistics, Accepted solution 43218123.
# Source: http://cs101.openjudge.cn/practice/solution/43218123/
# Statistics: http://cs101.openjudge.cn/practice/20004/statistics/
# License: not declared on submission page; no license inferred
r=[float(i[:-1])/100 for i in input().split()]
t=[1+r[0]]
for i in r[1:]:
    t.append(t[-1]*(1+i))
l=len(t)
mmin=[(t[-1],l-1)]
for i in range(1,len(r)):
    if t[l-i-1]<mmin[i-1][0]:
        mmin.append((t[l-i-1],l-i-1))
    else:
        mmin.append(mmin[i-1])
ans,pos=0,0
for i in range(len(t)):
    if ans<(t[i]-mmin[l-i-1][0])/t[i]:
        ans=(t[i]-mmin[l-i-1][0])/t[i]
        pos=mmin[l-i-1][1]-i
print(f'{-1*ans*100:.1f}% {pos}')

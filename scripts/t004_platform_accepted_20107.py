# External reference: cs101.openjudge.cn practice/20107 statistics, Accepted solution 22600399.
# Source: http://cs101.openjudge.cn/practice/solution/22600399/
# Statistics: http://cs101.openjudge.cn/practice/20107/statistics/
# License: not declared on submission page; no license inferred
d=int(input())
n,T=map(int,input().split())
z=[[0 for i in range(135)] for i in range(135)]
times=[]
for i in range(n):
    times.append(list(map(int,input().split())))
    z[times[i][0]][times[i][1]]=i+1
    times[i].remove(times[i][0])
    times[i].remove(times[i][0])

def take(x1,x2,y1,y2,t):
    s=0
    if(x1<0):
        x1=0
    if(y1<0):
        y1=0
    if(x2>128):
        x2=128
    if(y2>128):
        y2=128
    for i in range(x1,x2+1):
        for j in range(y1,y2+1):
            if(z[i][j]>0):
                s+=times[z[i][j]-1][t]
    return s

maxn=-1
num=0
t0=0
for i in range(0,129):
    for j in range(0,129):
        for t in range(0,T):
            a=take(i-d,i+d,j-d,j+d,t)
            if(maxn<a):
                maxn=a
                num=1
                t0=t
            elif(maxn==a):
                num+=1

print(num,t0,maxn)

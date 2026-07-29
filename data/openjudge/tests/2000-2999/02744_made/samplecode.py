# External reference: http://cs101.openjudge.cn/practice/02744/statistics/
# Accepted submission: 46688613
# Source: http://cs101.openjudge.cn/practice/solution/46688613/
# License: not declared on the submission page; no license is inferred.

def find_i(x,y):
    mmax=[0,0,0]
    lx=len(x)
    ly=len(y)
    for i in range(lx):
        for j in range(ly):
            px,py=i,j
            while px<lx and py<ly and x[px]==y[py]:
                px+=1
                py+=1
            if(px-i)>mmax[0]:
                mmax[0]=px-i
                mmax[1:]=i,px
    return x[mmax[1]:mmax[2]]
def find_x(x,y):
    cur1=find_i(x,y)
    cur2=find_i(x,y[::-1])
    return cur1 if len(cur1)>len(cur2) else cur2
for i in range(int(input())):
    n=int(input())
    ss=sorted([input() for _ in range(n)],key=lambda x:len(x))
    cur=ss[0]
    for i in range(1,n):cur=find_x(cur,ss[i])
    print(len(cur))

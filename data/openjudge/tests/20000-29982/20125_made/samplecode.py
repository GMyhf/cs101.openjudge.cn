# External reference: statistics page /practice/20125/
# Accepted submission: 41484284
# Source: http://cs101.openjudge.cn/practice/solution/41484284/
# License: not declared on the submission page; no license is inferred.

# External reference: cs101.openjudge.cn practice/20125 statistics, Accepted solution 41484284.
# Source: http://cs101.openjudge.cn/practice/solution/41484284/
# Statistics: http://cs101.openjudge.cn/practice/20125/statistics/
# License: not declared on submission page; no license inferred
# 王楚惟
l=int(input())
'''a=[int(i)for i in input().split()]
s=list(set(a))
b=[a.count(i)for i in s]
l=len(b)
n=n//2'''
b=[int(i)for i in input().split()]
n=0
for i in b:
    n+=i
n=n//2

cun=0
if n==0:
    print(1)
else:
    
    tem=0
    def ans(i):
        global cun
        global tem
        if i==l:
            if tem==n:
                cun=cun+1
        else:
            for j in range(b[i]+1):
                if tem+j>n:
                    break
                else:
                    tem=tem+j
                    ans(i+1)
                    tem=tem-j

    if l==1:
        print(1)
    elif l==2:
        print(min(b[0],b[1])+1)
    else:
        ans(0)
        print(cun)

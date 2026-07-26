# External reference: cs101.openjudge.cn practice/05349 statistics, Accepted solution 52106037.
# Source: http://cs101.openjudge.cn/practice/solution/52106037/
# Statistics: http://cs101.openjudge.cn/practice/05349/statistics/
# License: not declared on submission page; no license inferred
n=int(input())
strings=[]
for i in range(n):
    strings.append(input())
stan=input().upper().split('[')
x=stan[1].split(']')
stan[1]=x[0]
stan.append(x[1])
m=len(stan[0])
n=len(stan[2])
ans=[]
i=0
for s in strings:
    S=s.upper()
    if S[:m]==stan[0] and S[len(s)-n:]==stan[2] and S[m:len(s)-n] in stan[1] and len(s)==m+n+1:
        ans.append((i+1,s))
    i+=1
for a,s in ans:
    print(a,s)
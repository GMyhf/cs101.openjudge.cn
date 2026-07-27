# External reference: statistics page /practice/28322/
# Accepted submission: 52484649
# Source: http://cs101.openjudge.cn/practice/solution/52484649/
# License: not declared on the submission page; no license is inferred.

def en(s):
    stack=[]
    n=len(s)
    ans=''
    for i in range(n):
        if ord(s[i])%2==0:
            ans+=s[i]
            while stack:
                x=stack.pop()
                ans+=x
        else:
            stack.append(s[i])
    if stack:
        ans+='0'
    while stack:
                x=stack.pop()
                ans+=x
    return ans

def de(t):
    n=len(t)
    ans=''
    l=0
    for i in range(1,n):
        if  ord(t[i])%2==0:
            ans+=t[i-1:l-1:-1] if l>0 else t[i-1::-1]
            l=i
        elif t[i]=='0':
            ans+=t[i-1:l-1:-1]
            l=i+1
            break
    ans+=t[-1:l-1:-1] if l>0 else t[::-1]
    if ans[-1]=='0':
        return ans[:-1]
    return ans

t=int(input())
for i in range(t):
    task=input()
    if task=='encrypt':
        s=input()
        print(en(s))
    else:
        t=input()
        print(de(t))
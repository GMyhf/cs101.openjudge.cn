# External reference: statistics page /practice/27312/
# Accepted submission: 52514507
# Source: http://cs101.openjudge.cn/practice/solution/52514507/
# License: not declared on the submission page; no license is inferred.

n=int(input())
las=-1
s=input()
ans=0
i=0
fan=""
while i<=n-2:
    if s[i]==s[i+1]:
        i+=2
        continue
    elif s[i]=="H" and s[i+1]=="G":
        if las!=1:
            fan=fan+"1"
            las=1
        i+=2
        continue
    else:
        if las!=0:
            fan=fan+"0"
            las=0
        i+=2
        continue
if fan=="":
    ans=0
elif fan[0]=="1":
    ans=len(fan)-len(fan)%2
else:
    ans=len(fan)-(len(fan)+1)%2
print(ans)
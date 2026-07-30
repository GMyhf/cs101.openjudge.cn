# External reference: http://cs101.openjudge.cn/practice/16530/statistics/
# Accepted submission: 52537507
# Source: http://cs101.openjudge.cn/practice/solution/52537507/
# License: not declared on the submission page; no license is inferred.

n=int(input())
names=[]
for i in range(n):
    names.append(input())
names.sort()
x=n//2-1
a=names[x]
b=names[x+1]
def main(a,b):
    if a in b:
        return a
    m=len(a)
    n=len(b)
    same=''
    for i in range(len(a)):
        if a[i]==b[i]:
            same+=a[i]
        else:
            diff=i
            break
    if ord(b[diff])-ord(a[diff])>1:
        return same+chr(ord(a[diff])+1)
    if diff!=n-1:
        return b[:diff+1]
    x0=a[:diff+1]
    for i in range(m-diff):
        x=x0+'Z'*i
        if x>=a:
            return x
x=main(a,b)
while x>a and x[-1]>'A':
    x=x[:-1]+chr((ord(x[-1])-1))
if x<a:
    x=x[:-1]+chr((ord(x[-1])+1))
print(x)

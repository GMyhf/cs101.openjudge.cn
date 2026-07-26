# External reference: statistics page /practice/04143/
# Accepted submission: 52701344
# Source: http://cs101.openjudge.cn/practice/solution/52701344/
# License: not declared on the submission page; no license is inferred.

a=int(input())
b=list(map(int, input().split()))
b.sort()
c=int(input())
left=0
right=a-1
while left<right:
    while b[left]+b[right]>c:
        right-=1
    if b[left]+b[right]==c:
        print(b[left],b[right],end=" ")
        quit()
    else:
        left+=1
print("No")
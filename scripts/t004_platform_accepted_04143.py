# External reference: cs101.openjudge.cn practice/04143 statistics, Accepted solution 52701344.
# Source: http://cs101.openjudge.cn/practice/solution/52701344/
# Statistics: http://cs101.openjudge.cn/practice/04143/statistics/
# License: not declared on submission page; no license inferred
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
# External reference: http://cs101.openjudge.cn/practice/18156/statistics/
# Accepted submission: 52468268
# Source: http://cs101.openjudge.cn/practice/solution/52468268/
# License: not declared on the submission page; no license is inferred.

T=int(input())
num=[int(i) for i in input().split()]
num.sort()
best=float('inf')
left=0
right=len(num)-1
while True:
    if left>=right:
        break
    current=num[left]+num[right]
    if abs(current-T)<abs(best-T):
        best=current
    elif abs(current-T)==abs(best-T):
        best=min(current,best)
    if current<T:
        left+=1
    elif current>T:
        right-=1
    else:
        best=T
        break
print(best)

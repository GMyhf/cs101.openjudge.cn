# External reference: cs101.openjudge.cn practice/04139 statistics, Accepted solution 51213960.
# Source: http://cs101.openjudge.cn/practice/solution/51213960/
# Statistics: http://cs101.openjudge.cn/practice/04139/statistics/
# License: not declared on submission page; no license inferred
a,b,c=map(int,input().split())
result=0
for k in range(c//b+1):
    if (c-b*k)%a==0:
        result+=1
print(result)
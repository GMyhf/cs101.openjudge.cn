# External reference: http://cs101.openjudge.cn/practice/02696/statistics/
# Accepted submission: 51484214
# Source: http://cs101.openjudge.cn/practice/solution/51484214/
# License: not declared on the submission page; no license is inferred.

dict1={'mul':'*','div':'//','add':'+','sub':'-','mod':'%'}
for _ in range(int(input())):
    a,x,b=input().split()
    print(eval(a+dict1[x]+b))

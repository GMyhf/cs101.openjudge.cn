# External reference: cs101.openjudge.cn practice/19971 statistics, Accepted solution 43885342.
# Source: http://cs101.openjudge.cn/practice/solution/43885342/
# Statistics: http://cs101.openjudge.cn/practice/19971/statistics/
# License: not declared on submission page; no license inferred
a=[[1]]
for i in range(1,1001):
    a.append([1])
    if i%2:
        for j in range(i//2):a[-1].append(a[-2][j]+a[-2][j+1])
    else:
        for j in range(i//2-1):a[-1].append(a[-2][j]+a[-2][j+1])
        a[-1].append(a[-2][-1]*2)
for i in range(int(input())):c,b=map(int,input().split());print(a[b][b-c]if c*2>b else a[b][c])

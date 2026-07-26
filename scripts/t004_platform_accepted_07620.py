# External reference: cs101.openjudge.cn practice/07620 statistics, Accepted solution 52536053.
# Source: http://cs101.openjudge.cn/practice/solution/52536053/
# Statistics: http://cs101.openjudge.cn/practice/07620/statistics/
# License: not declared on submission page; no license inferred
n=int(input())
intervals=[]
for i in range(n):
    intervals.append(tuple(int(i) for i in input().split()))
intervals.sort()
cleft=intervals[0][0]
cright=intervals[0][1]
for left,right in intervals:
    if left>cright:
        print("no")
        break
    else:
        cright=max(right,cright)
else:
    print(cleft,cright)
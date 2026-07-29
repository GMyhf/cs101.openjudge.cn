# External reference: http://cs101.openjudge.cn/practice/01089/statistics/
# Accepted submission: 52536537
# Source: http://cs101.openjudge.cn/practice/solution/52536537/
# License: not declared on the submission page; no license is inferred.

n = int(input())
intervals = []
for _ in range(n):
    intervals.append(list(map(int,input().split())))
intervals.sort()
#print(intervals)
def xianghouhebing(i):
    j = 1
    while i + j < n and intervals[i+j][0] <= intervals[i][1]: #可合并
        intervals[i][1] = max(intervals[i][1], intervals[i+j][1]) #进行合并
        j += 1 #遍历下一个
    return i+j
i = 0
remainder = [0]*n
while i < n:
    remainder[i] = 1
    i = xianghouhebing(i)
#print(intervals)
for k in range(n):
    if remainder[k]:
        print(*intervals[k])

# External reference: http://cs101.openjudge.cn/practice/29918/statistics/
# Accepted submission: 52266773
# Source: http://cs101.openjudge.cn/practice/solution/52266773/
# License: not declared on the submission page; no license is inferred.

l=[(220, 284),(1184, 1210),(2620, 2924),(5020, 5564),(6232, 6368),(10744, 10856),(12285, 14595),(17296, 18416),(63020, 76084),(66928, 66992),(67095, 71145),(69615, 87633),(79750, 88730)]
answer=[]
n=int(input())
for i in l:
    if i[0]<=n and i[1]<=n:
        answer.append(i)
for i in answer:
    print(i[0],i[1])

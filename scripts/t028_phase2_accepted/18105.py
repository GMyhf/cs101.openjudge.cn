# External reference: http://cs101.openjudge.cn/practice/18105/statistics/
# Accepted submission: 51275218
# Source: http://cs101.openjudge.cn/practice/solution/51275218/
# License: not declared on the submission page; no license is inferred.

li = [int(x) for x in input().split()]
li.sort(reverse=True)
for i in range(len(li)):
    if li[i] >= i + 1:
        h = i + 1
    else:
        break
print(h)

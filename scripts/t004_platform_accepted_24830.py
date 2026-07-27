# External reference: statistics page /practice/24830/
# Accepted submission: 52740101
# Source: http://cs101.openjudge.cn/practice/solution/52740101/
# License: not declared on the submission page; no license is inferred.

n = int(input())
h = list(map(int, input().split()))
# 环形处理，加倍
arr = h + h

max_len = 0
current = 0

for i in range(len(arr) - 1):
    if arr[i] > arr[i + 1]:
        current += 1
        if current > max_len:
            max_len = current
    else:
        current = 0

# 最长不能超过一圈
max_len = min(max_len, n)
# 全相等输出 0
if max_len == 0:
    print(0)
else:
    print(max_len)
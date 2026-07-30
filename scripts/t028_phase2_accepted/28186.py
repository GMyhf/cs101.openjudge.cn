# External reference: http://cs101.openjudge.cn/practice/28186/statistics/
# Accepted submission: 52734661
# Source: http://cs101.openjudge.cn/practice/solution/52734661/
# License: not declared on the submission page; no license is inferred.

from collections import deque

n, m = map(int, input().split())
a = list(map(int, input().split()))

# 队列存 (编号, 需要的糖果数)
q = deque()
for i in range(n):
    q.append((i + 1, a[i]))  # 编号从1开始

last = 0  # 记录最后回家的人

while q:
    idx, need = q.popleft()
    need -= m  # 发m颗糖
    if need > 0:
        # 还不够，去队尾
        q.append((idx, need))
    else:
        # 够了，回家，更新最后一个
        last = idx

print(last)

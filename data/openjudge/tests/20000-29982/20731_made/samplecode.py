# External reference: statistics page /practice/20731/
# Accepted submission: 52201327
# Source: http://cs101.openjudge.cn/practice/solution/52201327/
# License: not declared on the submission page; no license is inferred.
# 2026-10-08 本地重写：上面引用的原始代码在题面范围内有缺陷，下面已换成按题面重写的实现，不再是原提交（原因见下方注释与 CHANGELOG）。
# 原样例解（AC 提交 52201327，http://cs101.openjudge.cn/practice/solution/52201327/）在 x>y 时
# 会漏掉交换（如 x=3,y=1），在本仓数据上答案错误；这里改为直接交换后求边缘和。

m, n = map(int, input().split())
a = [list(map(int, input().split())) for _ in range(m)]
x, y = map(int, input().split())
a[x - 1], a[y - 1] = a[y - 1], a[x - 1]
print(sum(a[i][j] for i in range(m) for j in range(n)
          if i == 0 or i == m - 1 or j == 0 or j == n - 1))

# External reference: http://cs101.openjudge.cn/practice/02679/statistics/
# Accepted submission: 52502033
# Source: http://cs101.openjudge.cn/practice/solution/52502033/
# License: not declared on the submission page; no license is inferred.
#
# 算法逐字取自上面那份平台 Accepted 提交，2026-09-12 只加了这段注释。
# 题面（描述）明写 **1 < k < 10**，所以 k 只有 2..9 八个合法取值、立方和最大 2025。
# 2026-09-12 之前生成器写的是 `r.randint(1, 10000)`，21 组里有 20 组的 k 越界
# （最大 9982），于是一份在题面范围内完全正确的 C++ `int` 解会溢出挂第 2 组、
# 一份 k=2..9 的查表解直接 Runtime Error。数据已按题面重建，见 CHANGELOG。

k = int(input())
res = 0
for i in range(1, k + 1):
    res += i ** 3

print(res)

# External reference: http://cs101.openjudge.cn/practice/02986/statistics/
# Accepted submission: 51426424
# Source: http://cs101.openjudge.cn/practice/solution/51426424/
# License: not declared on the submission page; no license is inferred.
# 2026-10-08 本地重写：上面引用的原始代码在题面范围内有缺陷，下面已换成按题面重写的实现，不再是原提交（原因见下方注释与 CHANGELOG）。
# 自写参考解（替换原先引用的提交 51426424：它只判 n//2^i - (n-k)//2^i，漏减 k//2^i，
# 例如 "3 2"、"16777215 5713800" 都会错输出 0）。
# 由 Lucas 定理：C(n,k) 为奇数当且仅当 k 的二进制位是 n 的子集，即 n & k == k。
import sys

out = []
for line in sys.stdin.read().splitlines():
    if not line.strip():
        continue
    n, k = map(int, line.split())
    out.append("1" if n & k == k else "0")
print("\n".join(out))

# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 1067: 取石子游戏
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/01067/
# License: not declared; no license is inferred.
# 2026-10-08 本地重写：上面引用的原始代码在题面范围内有缺陷，下面已换成按题面重写的实现，不再是原提交（原因见下方注释与 CHANGELOG）。
# 参考解：威佐夫博弈。原先引用的 2020fall 代码用浮点 k*(sqrt5+1)/2 求 Beatty 数，在 k 为某些斐波那契数
# （如 102334155、267914296）时差 1；这里改成精确整数 floor(k*phi) = (k + isqrt(5k^2)) // 2。
import sys
from math import isqrt
out = []
for line in sys.stdin.read().split("\n"):
    t = line.split()
    if len(t) < 2:
        continue
    a, b = sorted(map(int, t[:2]))
    k = b - a
    out.append("0" if a == (k + isqrt(5 * k * k)) // 2 else "1")
print("\n".join(out))

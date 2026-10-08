# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 1061: 青蛙的约会
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/01061/
# License: not declared in source collection; no license is inferred.
# 2026-10-08 本地重写：上面引用的原始代码在题面范围内有缺陷，下面已换成按题面重写的实现，不再是原提交（原因见下方注释与 CHANGELOG）。
# 参考解：原先引用的 2020fall 代码在 L 不是 a 的倍数时逐个试 i=1..L-1，L 接近 2.1e9 时必然超时，
# 而且 i*(b//c) 不保证最小；旧生成器只用不超过 4001 的素数 L 并且永不出现 Impossible。
# 这里改成扩展欧几里得：t*(m-n) ≡ y-x (mod L)，求最小正整数 t。
from math import gcd
x, y, m, n, L = map(int, input().split())
a = (m - n) % L
b = (y - x) % L
g = gcd(a, L)
if b % g:
    print("Impossible")
else:
    M = L // g
    print((b // g) * pow(a // g, -1, M) % M)

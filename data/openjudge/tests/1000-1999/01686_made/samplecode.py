# External reference: http://cs101.openjudge.cn/practice/01686/statistics/
# Accepted submission: 48613173
# Source: http://cs101.openjudge.cn/practice/solution/48613173/
# License: not declared on the submission page; no license is inferred.
# 2026-10-08 本地修正：上面引用的原始代码在题面范围内有缺陷，已按题面改过，与原提交不再逐字一致（见 CHANGELOG）。
# 原代码只给 a–z 赋值，碰上大写变量（题面写明区分大小写）会 NameError；
# 且代入 (0,1) 的随机小数，高次幂下溢后会误判相等。改为给 52 个字母代入大随机整数、精确比较。

import random
from string import ascii_letters
random.seed(1686)
def check(s1,s2):
    for _ in range(10):
        env={ch:random.randint(10**6,10**9) for ch in ascii_letters}
        if eval(s1.strip(),{},env)!=eval(s2.strip(),{},env):
            return False
    return True
n=int(input())
for _ in range(n):
    s1=input()
    s2=input()
    print("YES" if check(s1,s2) else "NO")

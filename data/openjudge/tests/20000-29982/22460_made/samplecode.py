# External reference: statistics page /practice/22460/
# Accepted submission: 45199466
# Source: http://cs101.openjudge.cn/practice/solution/45199466/
# License: not declared on the submission page; no license is inferred.
# 2026-10-08 本地重写：上面引用的原始代码在题面范围内有缺陷，下面已换成按题面重写的实现，不再是原提交（原因见下方注释与 CHANGELOG）。
# 原 AC 提交 45199466 会把「完整树后再接一棵同首数字的树」（如 1 # # 1 # #）误判为 T，
# 已换成与 producecase.py 中 REFERENCE 相同的槽位计数写法。
import sys
def check(ls):
    slots = 1
    for t in ls:
        if slots == 0:
            return False
        slots += 1 if t != '#' else -1
    return slots == 0

data = sys.stdin.read().split()
p = 0
out = []
while True:
    n = int(data[p]); p += 1
    if n == 0:
        break
    ls = data[p:p + n]; p += n
    out.append('T' if check(ls) else 'F')
print('\n'.join(out))

# External reference: statistics page /practice/04143/
# Accepted submission: 52701344
# Source: http://cs101.openjudge.cn/practice/solution/52701344/
# License: not declared on the submission page; no license is inferred.
#
# 2026-10-07 审计改写：上面那份 AC 提交的双指针 `while b[left]+b[right]>c: right-=1`
# 不检查 right>=left，会让同一元素自己配对（`2\n1 3\n2` 输出 `1 1`），全部元素
# 都大于 m 时下标走成负数后 IndexError。平台原数据没卡到，加强后的数据会卡到，
# 故换成与 producecase.py 内嵌 REFERENCE 相同的按值计数写法。
# 2026-10-08 本地修正：上面引用的原始代码在题面范围内有缺陷，已按题面改过，与原提交不再逐字一致（见 CHANGELOG）。
import sys
from collections import Counter
d = sys.stdin.read().split()
n = int(d[0]); a = list(map(int, d[1:1 + n])); m = int(d[1 + n])
c = Counter(a)
ans = 'No'
for x in sorted(c):
    y = m - x
    if y < x:
        break
    if (y > x and y in c) or (y == x and c[x] >= 2):
        ans = f'{x} {y}'
        break
print(ans)

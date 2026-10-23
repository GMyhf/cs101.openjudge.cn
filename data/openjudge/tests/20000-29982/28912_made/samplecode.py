# External reference: http://cs101.openjudge.cn/practice/28912/statistics/
# Accepted submission: 50926112
# Source: http://cs101.openjudge.cn/practice/solution/50926112/
# License: not declared on the submission page; no license is inferred.

# 本地修正：仅访问整数位置，按离散差分事件扫描，不使用浮点折点。
from collections import defaultdict
import sys

n, bound = map(int, sys.stdin.readline().split())
terms = [tuple(map(int, sys.stdin.readline().split())) for _ in range(n)]
current = sum(c*abs(b) for a, b, c in terms)
slope = sum(c*(abs(a+b)-abs(b)) for a, b, c in terms)
events = defaultdict(int)
for a, b, c in terms:
    if not a:
        continue
    if a < 0:
        a, b = -a, -b
    k, r = divmod(-b, a)
    if 1 <= k < bound:
        events[k] += 2*c*(a-r)
    if 1 <= k+1 < bound:
        events[k+1] += 2*c*r
minimum = maximum = current
previous = 0
for x in sorted(events):
    current += (x-previous)*slope
    minimum, maximum = min(minimum, current), max(maximum, current)
    slope += events[x]
    previous = x
current += (bound-previous)*slope
print(max(maximum, current), min(minimum, current))

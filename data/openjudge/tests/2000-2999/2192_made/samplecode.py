# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
# Heading: 2192: Zipper
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md
# Upstream problem: http://cs101.openjudge.cn/2024sp_routine/02192/
# License: not declared in source collection; no license is inferred.
# 袁籁2300010728
from functools import lru_cache


@lru_cache
def f(a, b, c):
    if len(c) == 0:
        return True
    else:
        if len(a) and c[0] == a[0] and f(a[1:], b, c[1:]):
            return True
        elif len(b) and c[0] == b[0] and f(a, b[1:], c[1:]):
            return True
        else:
            return False


n = int(input())
for _ in range(n):
    a, b, c = input().split()
    x = len(c)
    if f(a, b, c):
        print('Data set %d: yes' % (_ + 1))
    else:
        print('Data set %d: no' % (_ + 1))

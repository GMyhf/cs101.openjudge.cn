# External reference: /practice/29750/statistics/
# Accepted submission: 52710073
# Source: http://cs101.openjudge.cn/practice/solution/52710073/
# License: not declared on the submission page; no license is inferred.

n = int(input())
a = [*map(int, input().split())]
a = [0] + a
num = ['', 'A', 'B', 'C']
def f(n, l, m, r): # n代表当前移动的是第n个圆盘
    if n == 0:
        return
    if (l, r) in [(1, 2), (2, 1), (2, 3), (3, 2)] or a[n] == 0:
        f(n-1, l, r, m)
        print(f'moving disk {n} from {num[l]} to {num[r]}')
        f(n-1, m, l, r)
    else:
        f(n-1, l, m, r)
        print(f'moving disk {n} from {num[l]} to {num[m]}')
        f(n-1, r, m, l)
        print(f'moving disk {n} from {num[m]} to {num[r]}')
        f(n-1, l, m, r)
f(n, 1, 2, 3)
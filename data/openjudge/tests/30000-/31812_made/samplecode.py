"""本仓库自写参考解；原题：dsa.openjudge.cn/2022final1/5/。按左右子树大小差的绝对值求和。"""
import sys


def solve(text):
    a = list(map(int, text.split()))
    n = a[0]
    children = [[] for _ in range(n+1)]
    for u, v in zip(a[1::2], a[2::2]):
        children[u].append(v)
    order = [1]
    for u in order:
        order.extend(children[u])
    size = [1] * (n+1)
    total = 0
    for u in reversed(order):
        cs = children[u]
        left = size[cs[0]] if cs else 0
        right = size[cs[1]] if len(cs) == 2 else 0
        size[u] += left + right
        total += abs(left-right)
    delta = [0] * (n+1)
    best = n
    for u in order:
        if not children[u]:
            best = min(best, delta[u])
        for v in children[u]:
            other = size[u]-1-size[v]
            delta[v] = delta[u] + (-1 if size[v] > other else 1)
    return str(total + best) + '\n'


if __name__ == '__main__':
    print(solve(sys.stdin.read()), end='')

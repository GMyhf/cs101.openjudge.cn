"""本仓库自写参考解；原题：dsa.openjudge.cn/2022final1/3/。"""
import sys


def solve(text):
    a = list(map(int, text.split()))
    n = a[0]
    edges = sorted((a[i+2], a[i]-1, a[i+1]-1) for i in range(1, len(a), 3))
    parent = list(range(n))
    size = [1] * n
    def find(x):
        while x != parent[x]:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    answer = 0
    for w, u, v in edges:
        u, v = find(u), find(v)
        answer += (w+1) * size[u] * size[v] - 1
        if size[u] < size[v]:
            u, v = v, u
        parent[v] = u
        size[u] += size[v]
    return str(answer) + '\n'


if __name__ == '__main__':
    print(solve(sys.stdin.read()), end='')

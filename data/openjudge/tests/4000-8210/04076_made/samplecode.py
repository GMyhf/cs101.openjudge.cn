# 2026-10 审计替换：原 samplecode 为递归 DFS，K 近 1000 时超出 Python 默认递归深度（RecursionError）；现为显式栈迭代 DFS，搜索顺序不变。
# 小组与 producecase.py 的位集 oracle 对拍，大组答案由构造保证。
import sys
def main():
    a = sys.stdin.buffer.read().split()
    m, n = int(a[0]), int(a[1])
    g = [int(x) for x in a[2:2 + m * n]]
    k = int(a[2 + m * n]); pat = [int(x) for x in a[3 + m * n:3 + m * n + k]]
    if k > m * n:
        print(0); return
    nb = []
    for i in range(m):
        for j in range(n):
            z = []
            if i + 1 < m: z.append((i + 1) * n + j)
            if i > 0: z.append((i - 1) * n + j)
            if j + 1 < n: z.append(i * n + j + 1)
            if j > 0: z.append(i * n + j - 1)
            nb.append(z)
    used = bytearray(m * n)
    for s in range(m * n):
        if g[s] != pat[0]:
            continue
        if k == 1:
            print(1); return
        used[s] = 1
        stack = [(s, 0)]               # (格子, 已尝试到的邻居下标)
        while stack:
            u, t = stack[-1]
            p = len(stack)             # 下一个要匹配 pat[p]
            nxt = -1
            z = nb[u]
            while t < len(z):
                v = z[t]; t += 1
                if not used[v] and g[v] == pat[p]:
                    nxt = v; break
            if nxt < 0:
                stack.pop(); used[u] = 0
                continue
            stack[-1] = (u, t)
            if p + 1 == k:
                print(1); return
            used[nxt] = 1
            stack.append((nxt, 0))
    print(0)
main()

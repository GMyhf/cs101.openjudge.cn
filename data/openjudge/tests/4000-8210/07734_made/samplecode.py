# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
import sys
sys.setrecursionlimit(1000000)


def solve():
    T = int(input())

    for case in range(1, T + 1):
        n, m = map(int, input().split())

        # 扩展域：1~n 表示性别A，n+1~2n 表示性别B
        parent = list(range(2 * n + 1))

        def find(i):
            if parent[i] == i:
                return i
            parent[i] = find(parent[i])
            return parent[i]

        def union(i, j):
            root_i = find(i)
            root_j = find(j)
            if root_i != root_j:
                parent[root_i] = root_j

        suspicious = False
        for _ in range(m):
            u, v = map(int, input().split())
            if suspicious: continue

            # 如果 u 和 v 已经在同一个性别域里，说明他们是同性！
            if find(u) == find(v):
                suspicious = True
            else:
                # u 恋爱对象必须是 v 的异性分身
                union(u, v + n)
                # v 恋爱对象必须是 u 的异性分身
                union(v, u + n)

        print(f"Scenario #{case}:")
        if suspicious:
            print("Suspicious bugs found!")
        else:
            print("No suspicious bugs found!")
        print()


solve()

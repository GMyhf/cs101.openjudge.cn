# External reference: http://cs101.openjudge.cn/practice/02492/statistics/
# Accepted submission: 45386458
# Source: http://cs101.openjudge.cn/practice/solution/45386458/
# License: not declared on the submission page; no license is inferred.

class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))

    def find(self, x):
        if x != self.parent[x]:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rootX = self.find(x)
        rootY = self.find(y)
        if rootX != rootY:
            self.parent[rootY] = rootX

    def is_connected(self, x, y):
        return self.find(x) == self.find(y)


def solve_bug_life(scenarios):
    for i in range(1, scenarios + 1):
        n, m = map(int, input().split())
        uf = UnionFind(2 * n + 1)  # 为每个虫子创建两个节点表示其可能的两种性别
        suspicious = False
        for _ in range(m):
            u, v = map(int, input().split())
            if suspicious:
                continue

            if uf.is_connected(u, v):
                suspicious = True
            uf.union(u, v + n)  # 将u的一种性别与v的另一种性别关联
            uf.union(u + n, v)  # 同理


        print(f'Scenario #{i}:')
        print('Suspicious bugs found!' if suspicious else 'No suspicious bugs found!')
        print()


# 读取场景数量并解决问题
scenarios = int(input())
solve_bug_life(scenarios)

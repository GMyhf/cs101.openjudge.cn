# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
import sys
from collections import defaultdict, deque


def solve():
    data = sys.stdin.readline().strip().split()
    if not data:
        return
    m, n = map(int, data)

    # 1) 读入所有 “A > B” 关系，建图
    edges = defaultdict(list)
    indegree = [0] * (m + 1)
    for _ in range(n):
        line = sys.stdin.readline().strip()
        if not line:
            continue
        left_str, right_str = line.split('>')
        A = int(left_str.strip())
        B = int(right_str.strip())
        edges[A].append(B)
        indegree[B] += 1

    # 2) 拓扑排序：检查矛盾（环）和是否唯一
    q = deque()
    for u in range(1, m + 1):
        if indegree[u] == 0:
            q.append(u)

    topo_list = []
    multiple = False
    while q:
        if len(q) > 1:
            multiple = True
        u = q.popleft()
        topo_list.append(u)
        for v in edges[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                q.append(v)

    if len(topo_list) < m:
        print("Device error.")
        return
    if multiple:
        print("Not determined.")
        return

    # 3) 生成“位置从大到小”的序列 pos_order（前序 根→右→左）
    pos_order = []

    def dfs(u):
        if u > m:
            return
        pos_order.append(u)
        dfs(2 * u + 1)
        dfs(2 * u)

    dfs(1)

    # 4) 给这些位置分配流量编号（topo_list 为从大到小的编号）
    assigned = [0] * (m + 1)
    for i in range(m):
        assigned[pos_order[i]] = topo_list[i]

    # 5) 使用递归方式中序遍历 assigned[]
    res = []

    def inorder(u):
        if u > m:
            return
        inorder(2 * u)
        res.append(str(assigned[u]))
        inorder(2 * u + 1)

    inorder(1)
    print(" ".join(res))


if __name__ == "__main__":
    solve()

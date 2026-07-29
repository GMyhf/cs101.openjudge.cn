# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
# Heading: 2186: Popular Cows
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/02186/
# License: not declared; no license is inferred.
import sys

# 增加递归深度
sys.setrecursionlimit(100000)

def solve():
    # 使用快读
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    m = int(input_data[1])

    adj = [[] for _ in range(n + 1)]
    edges = []
    idx = 2
    for _ in range(m):
        u = int(input_data[idx])
        v = int(input_data[idx+1])
        adj[u].append(v)
        edges.append((u, v))
        idx += 2

    # --- Tarjan 算法变量 ---
    dfn = [0] * (n + 1)
    low = [0] * (n + 1)
    stack = []
    in_stack = [False] * (n + 1)
    timer = 0

    scc_id = [0] * (n + 1)
    scc_size = {} # 记录每个 SCC 包含的节点数
    scc_count = 0

    def tarjan(u):
        nonlocal timer, scc_count
        timer += 1
        dfn[u] = low[u] = timer
        stack.append(u)
        in_stack[u] = True

        for v in adj[u]:
            if not dfn[v]:
                tarjan(v)
                low[u] = min(low[u], low[v])
            elif in_stack[v]:
                low[u] = min(low[u], dfn[v])

        if dfn[u] == low[u]:
            scc_count += 1
            count = 0
            while True:
                node = stack.pop()
                in_stack[node] = False
                scc_id[node] = scc_count
                count += 1
                if node == u:
                    break
            scc_size[scc_count] = count

    # 寻找 SCC
    for i in range(1, n + 1):
        if not dfn[i]:
            tarjan(i)

    # --- 统计缩点后各 SCC 的出度 ---
    out_degree = [0] * (scc_count + 1)
    for u, v in edges:
        if scc_id[u] != scc_id[v]:
            out_degree[scc_id[u]] += 1

    # --- 分析结论 ---
    zero_out_count = 0
    target_scc = 0

    for i in range(1, scc_count + 1):
        if out_degree[i] == 0:
            zero_out_count += 1
            target_scc = i

    if zero_out_count == 1:
        # 只有一个出度为 0 的 SCC，该 SCC 里的牛就是答案
        print(scc_size[target_scc])
    else:
        # 如果有多个出度为 0 的点，说明它们之间互不到达，没有牛能被所有人崇拜
        print(0)

if __name__ == "__main__":
    solve()

# External reference: /practice/29647/statistics/
# Accepted submission: 52829529
# Source: http://cs101.openjudge.cn/practice/solution/52829529/
# License: not declared on the submission page; no license is inferred.

import sys

def solve():
    # 增加递归深度限制，防止树退化为链时导致栈溢出
    sys.setrecursionlimit(2000)
    
    # 一次性读取所有输入数据
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    
    # 存储快乐指数，下标从 1 开始
    r = [0] * (n + 1)
    for i in range(1, n + 1):
        r[i] = int(input_data[i])
    
    # 构建邻接表和记录是否有上司
    adj = [[] for _ in range(n + 1)]
    has_parent = [False] * (n + 1)
    
    idx = n + 1
    # 读取 n - 1 条关系
    for _ in range(n - 1):
        if idx >= len(input_data):
            break
        l = int(input_data[idx])
        k = int(input_data[idx + 1])
        adj[k].append(l)  # k 是 l 的直接上司
        has_parent[l] = True
        idx += 2
        
    # 寻找根节点（没有直接上司的职员）
    root = 1
    for i in range(1, n + 1):
        if not has_parent[i]:
            root = i
            break
            
    # 定义树形 DP 的 DFS 函数
    # 返回一个元组 (dp[u][0], dp[u][1])
    # dp[u][0] 表示 u 不参加的最大值，dp[u][1] 表示 u 参加的最大值
    def dfs(u):
        dp_u_0 = 0
        dp_u_1 = r[u]
        
        for v in adj[u]:
            dp_v_0, dp_v_1 = dfs(v)
            # u 不参加：子节点 v 可以参加，也可以不参加
            dp_u_0 += max(dp_v_0, dp_v_1)
            # u 参加：子节点 v 绝对不能参加
            dp_u_1 += dp_v_0
            
        return dp_u_0, dp_u_1

    # 从根节点开始搜索
    ans_0, ans_1 = dfs(root)
    
    # 输出最大快乐指数
    print(max(ans_0, ans_1))

if __name__ == '__main__':
    solve()
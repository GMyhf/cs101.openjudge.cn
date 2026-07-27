# External reference: /practice/30222/statistics/
# Accepted submission: 52829485
# Source: http://cs101.openjudge.cn/practice/solution/52829485/
# License: not declared on the submission page; no license is inferred.

import sys
from collections import deque

def solve():
    # 读取所有输入
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    M = int(input_data[1])
    
    # 任务耗时，采用1-based索引
    T = [0] + [int(x) for x in input_data[2:2+N]]
    
    adj = [[] for _ in range(N + 1)]
    in_degree = [0] * (N + 1)
    
    # 构建邻接表和入度数组
    idx = 2 + N
    for _ in range(M):
        if idx >= len(input_data):
            break
        u = int(input_data[idx])
        v = int(input_data[idx+1])
        adj[u].append(v)
        in_degree[v] += 1
        idx += 2
        
    # 拓扑排序队列
    queue = deque()
    dp = [0] * (N + 1)
    
    # 初始化入度为 0 的节点
    for i in range(1, N + 1):
        dp[i] = T[i]
        if in_degree[i] == 0:
            queue.append(i)
            
    processed_count = 0
    
    # 拓扑排序与动态规划更新
    while queue:
        u = queue.popleft()
        processed_count += 1
        for v in adj[u]:
            if dp[u] + T[v] > dp[v]:
                dp[v] = dp[u] + T[v]
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
                
    # 判断是否存在环
    if processed_count < N:
        print(-1)
    else:
        print(max(dp))

if __name__ == '__main__':
    solve()
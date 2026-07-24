# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
import heapq
import sys

def solve():
    # 读取所有输入数据
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    ptr = 0
    
    # 1. 处理地点部分
    P = int(input_data[ptr])
    ptr += 1
    place_names = []
    name_to_idx = {}
    for i in range(P):
        name = input_data[ptr]
        place_names.append(name)
        name_to_idx[name] = i
        ptr += 1
        
    # 2. 处理道路部分 (无向图)
    Q = int(input_data[ptr])
    ptr += 1
    adj = [[] for _ in range(P)]
    for _ in range(Q):
        u_name = input_data[ptr]
        v_name = input_data[ptr+1]
        dist = int(input_data[ptr+2])
        ptr += 3
        
        u, v = name_to_idx[u_name], name_to_idx[v_name]
        adj[u].append((v, dist))
        adj[v].append((u, dist))
        
    # 3. 处理查询部分
    R = int(input_data[ptr])
    ptr += 1
    for _ in range(R):
        start_name = input_data[ptr]
        end_name = input_data[ptr+1]
        ptr += 2
        
        if start_name == end_name:
            print(start_name)
            continue
            
        start_idx = name_to_idx[start_name]
        end_idx = name_to_idx[end_name]
        
        # Dijkstra 算法
        distances = [float('inf')] * P
        parent = [-1] * P
        edge_to_dist = [0] * P # 记录到达该节点时的那段路程
        
        distances[start_idx] = 0
        pq = [(0, start_idx)]
        
        while pq:
            d, u = heapq.heappop(pq)
            
            if d > distances[u]:
                continue
            if u == end_idx:
                break
                
            for v, weight in adj[u]:
                if distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    parent[v] = u
                    edge_to_dist[v] = weight
                    heapq.heappush(pq, (distances[v], v))
        
        # 路径回溯
        path_nodes = []
        path_edges = []
        curr = end_idx
        while curr != -1:
            path_nodes.append(place_names[curr])
            if parent[curr] != -1:
                path_edges.append(edge_to_dist[curr])
            curr = parent[curr]
            
        path_nodes.reverse()
        path_edges.reverse()
        
        # 格式化输出
        output = []
        for i in range(len(path_nodes)):
            output.append(path_nodes[i])
            if i < len(path_edges):
                output.append(f"->({path_edges[i]})->")
        
        print("".join(output))

if __name__ == "__main__":
    solve()

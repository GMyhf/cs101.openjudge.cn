import random
import os
import sys

# 增加递归深度以处理深度并查集（虽然本题用了路径压缩，但保险起见）
sys.setrecursionlimit(200000)

# 确保 data 目录存在
os.makedirs("data", exist_ok=True)

def solve_logic(input_data):
    """
    ac.py 的逻辑实现，用于生成标准输出。
    input_data 格式为: [(n, m, [(x1, y1), (x2, y2), ...]), ...]
    """
    output_lines = []
    
    for n, m, queries in input_data:
        parent = list(range(n + 1))
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(x, y):
            root_x = find(x)
            root_y = find(y)
            if root_x != root_y:
                parent[root_y] = root_x
                return True
            return False

        for x, y in queries:
            if find(x) == find(y):
                output_lines.append("Yes")
            else:
                output_lines.append("No")
                union(x, y)
        
        # 获取所有当前作为根节点的杯子（即剩下的有阔落的杯子）
        # 注意：需要对所有节点执行一次 find 以确保路径压缩完成，
        # 或者直接检查 parent[i] == i
        ans = []
        for i in range(1, n + 1):
            if parent[i] == i:
                ans.append(i)
        
        output_lines.append(str(len(ans)))
        output_lines.append(" ".join(map(str, sorted(ans))))
        
    return "\n".join(output_lines)

# 生成 10 组测试文件（可根据需要调整）
for epoch in range(10):
    # 随机确定这组数据中有多少个 test cases (少于 5 组)
    num_cases = random.randint(1, 4)
    all_cases_data = []
    
    # 构造输入文件内容
    input_content = ""
    
    for _ in range(num_cases):
        # 根据 epoch 逐渐增加规模
        if epoch < 3:
            n = random.randint(1, 10)
            m = random.randint(1, 10)
        elif epoch < 7:
            n = random.randint(100, 1000)
            m = random.randint(100, 1000)
        else:
            n = 50000
            m = 50000
            
        queries = []
        input_content += f"{n} {m}\n"
        for _ in range(m):
            x = random.randint(1, n)
            y = random.randint(1, n)
            queries.append((x, y))
            input_content += f"{x} {y}\n"
        
        all_cases_data.append((n, m, queries))

    # 写入 .in 文件
    with open(f"data/{epoch}.in", "w") as f:
        f.write(input_content)

    # 得到标准输出
    result_output = solve_logic(all_cases_data)

    # 写入 .out 文件
    with open(f"data/{epoch}.out", "w") as f:
        f.write(result_output + "\n")

    print(f"[{epoch}] Generated. Cases: {num_cases}")

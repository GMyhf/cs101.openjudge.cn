# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
import sys

def find_lca_of_two(a, b):
    """查找两个节点 a 和 b 的最近公共祖先"""
    while a != b:
        if a > b:
            a //= 2  # 较大者向上爬
        else:
            b //= 2  # 较大者向上爬
    return a

def solve():
    # 使用 sys.stdin.read().split() 处理所有空格/换行符分割的输入
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    ptr = 0
    t_str = input_data[ptr]
    ptr += 1
    t = int(t_str)
    
    for _ in range(t):
        n = int(input_data[ptr])
        ptr += 1
        
        # 读取当前组的 n 个节点
        nodes = []
        for _ in range(n):
            nodes.append(int(input_data[ptr]))
            ptr += 1
            
        if not nodes:
            continue
        
        # 迭代处理：先取第一个数作为初始 LCA，然后不断与后面的数求 LCA
        res_lca = nodes[0]
        for i in range(1, n):
            res_lca = find_lca_of_two(res_lca, nodes[i])
        
        # 输出结果
        print(res_lca)

if __name__ == "__main__":
    solve()

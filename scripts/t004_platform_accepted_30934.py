# External reference: /practice/30934/statistics/
# Accepted submission: 52760566
# Source: http://cs101.openjudge.cn/practice/solution/52760566/
# License: not declared on the submission page; no license is inferred.

import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    it = iter(input_data)
    T = int(next(it))
    results = []
    
    for _ in range(T):
        N = int(next(it))
        # 使用数组存储每个节点的左右孩子，索引从 1 到 N
        left_child = [0] * (N + 1)
        right_child = [0] * (N + 1)
        
        for i in range(1, N + 1):
            l = int(next(it))
            r = int(next(it))
            left_child[i] = l
            right_child[i] = r
            
        # 定义递归检查镜像的函数
        def is_mirror(n1, n2):
            # 两个节点都为空，说明这部分是对称的
            if n1 == -1 and n2 == -1:
                return True
            # 只有一个为空，不对称
            if n1 == -1 or n2 == -1:
                return False
            # 都不为空，继续递归检查：
            # n1的左孩子 对应 n2的右孩子
            # n1的右孩子 对应 n2的左孩子
            return (is_mirror(left_child[n1], right_child[n2]) and 
                    is_mirror(right_child[n1], left_child[n2]))
        
        # 如果只有根节点，天然对称；否则比较根的左右孩子
        if N == 1:
            results.append("YES")
        else:
            if is_mirror(left_child[1], right_child[1]):
                results.append("YES")
            else:
                results.append("NO")
                
    print("\n".join(results))

if __name__ == "__main__":
    solve()
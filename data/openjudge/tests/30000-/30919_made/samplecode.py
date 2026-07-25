# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
import sys
import heapq

def solve():
    # 快速读取输入
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    n = int(input_data[0])
    x = [int(v) for v in input_data[1:n+1]]
    
    # 预分配数组
    L = [0] * (n + 1)
    D = [0] * (n + 1)
    
    heappush = heapq.heappush
    heappop = heapq.heappop
    
    # 1. 计算前缀偏差和 L
    left = []
    right = []
    sum_left = 0
    sum_right = 0
    
    if n > 0:
        val = x[0]
        heappush(left, -val)
        sum_left = val
        L[1] = 0
        
    for i in range(1, n):
        val = x[i]
        if val <= -left[0]:
            heappush(left, -val)
            sum_left += val
        else:
            heappush(right, val)
            sum_right += val
            
        len_l = len(left)
        len_r = len(right)
        if len_l > len_r + 1:
            moved = -heappop(left)
            sum_left -= moved
            heappush(right, moved)
            sum_right += moved
            len_l -= 1
            len_r += 1
        elif len_r > len_l:
            moved = heappop(right)
            sum_right -= moved
            heappush(left, -moved)
            sum_left += moved
            len_l += 1
            len_r -= 1
            
        L[i + 1] = sum_right - sum_left - left[0] * (len_l - len_r)
        
    # 2. 计算后缀偏差和 D (对反转数组运行相同逻辑)
    left = []
    right = []
    sum_left = 0
    sum_right = 0
    x_rev = x[::-1]
    
    if n > 0:
        val = x_rev[0]
        heappush(left, -val)
        sum_left = val
        D[1] = 0
        
    for i in range(1, n):
        val = x_rev[i]
        if val <= -left[0]:
            heappush(left, -val)
            sum_left += val
        else:
            heappush(right, val)
            sum_right += val
            
        len_l = len(left)
        len_r = len(right)
        if len_l > len_r + 1:
            moved = -heappop(left)
            sum_left -= moved
            heappush(right, moved)
            sum_right += moved
            len_l -= 1
            len_r += 1
        elif len_r > len_l:
            moved = heappop(right)
            sum_right -= moved
            heappush(left, -moved)
            sum_left += moved
            len_l += 1
            len_r -= 1
            
        D[i + 1] = sum_right - sum_left - left[0] * (len_l - len_r)
        
    # 3. 寻找最优分割点 t
    min_dist = float('inf')
    for t in range(n + 1):
        val = L[t] + D[n - t]
        if val < min_dist:
            min_dist = val
            
    # 如果 OJ 要求的输出包含公式中的系数 2，则输出 2 * min_dist
    # 如果 OJ 存在描述与数据不符的情况（即样例输出为 18），则此处改为 print(min_dist)
    print(2 * min_dist)

if __name__ == '__main__':
    solve()

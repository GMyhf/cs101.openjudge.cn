# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
import sys

def solve():
    # 一次性读取所有输入，提升读取效率
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    # 将发言数转换为整数列表
    x = [int(v) for v in input_data[1:n+1]]
    
    # 将发言数量从大到小排序
    x.sort(reverse=True)
    
    h_index = 0
    # 遍历排序后的数组，寻找最大的满足条件的 k
    for i in range(n):
        if x[i] >= i + 1:
            h_index = i + 1
        else:
            break
            
    print(h_index)

if __name__ == '__main__':
    solve()

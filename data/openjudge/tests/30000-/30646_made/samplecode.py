# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
import sys

def solve():
    # 读取所有输入并按空格切分
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    # 第一行是 n，后面是 n 个整数
    n = int(input_data[0])
    # 将数组元素转为整数并放入集合中
    nums = set(map(int, input_data[1:n+1]))
    
    # 从最小的正整数 1 开始查找
    res = 1
    while res in nums:
        res += 1
    
    # 输出结果
    print(res)

if __name__ == "__main__":
    solve()

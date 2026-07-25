# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
def min_houses_to_buy(W, n, prices):
    min_length = n + 1  # 初始化为最大长度+1，表示不可能的情况
    current_sum = 0     # 当前窗口的价格总和
    left = 0            # 窗口的左边界

    # 遍历房屋价格数组
    for right in range(n):
        current_sum += prices[right]  # 扩展窗口的右边界

        # 当当前总和大于等于W时，尝试缩小窗口的大小
        while current_sum >= W and left <= right:
            min_length = min(min_length, right - left + 1)
            current_sum -= prices[left]  # 缩小窗口的左边界
            left += 1

    # 如果min_length没有更新，说明没有找到满足条件的窗口
    return min_length if min_length <= n else 0

# 读取输入
W, n = map(int, input().split())
prices = list(map(int, input().split()))

# 计算结果并打印
print(min_houses_to_buy(W, n, prices))


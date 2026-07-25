# Source: /home/ubuntu/hongfei/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
def kadane(nums):
    max_ending_here = max_so_far = nums[0]
    for x in nums[1:]:
        max_ending_here = max(x, max_ending_here + x)
        max_so_far = max(max_so_far, max_ending_here)
    return max_so_far

def max_sum_shopping(values):
    # 不放回商品的情况下的最大价值总和
    max_without_deletion = kadane(values)

    # 如果整个数列的和都是负的，则土豪只能选择一个价值最大的商品
    if max_without_deletion < 0:
        return max(values)

    # 准备两个数组来存储从左到右和从右到左的最大子数组和
    left_max_sums = [0] * len(values)
    right_max_sums = [0] * len(values)

    # 从左到右的最大子数组和
    current = 0
    for i in range(len(values)):
        current = max(0, current + values[i])
        left_max_sums[i] = current

    # 从右到左的最大子数组和
    current = 0
    for i in range(len(values) - 1, -1, -1):
        current = max(0, current + values[i])
        right_max_sums[i] = current

    # 放回一个商品时的最大价值总和
    max_with_deletion = 0
    for i in range(1, len(values) - 1):
        max_with_deletion = max(max_with_deletion, left_max_sums[i - 1] + right_max_sums[i + 1])

    # 返回放回一个商品和不放回一个商品两种情况下的最大价值
    return max(max_with_deletion, max_without_deletion)

# 读取输入并处理
values_str = input().strip()
values = list(map(int, values_str.split(',')))
print(max_sum_shopping(values))

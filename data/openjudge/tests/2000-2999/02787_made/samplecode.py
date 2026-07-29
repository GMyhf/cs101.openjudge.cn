# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 2787: 算24
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/02787/
# License: not declared; no license is inferred.
import sys
#gpt
'''
在这个优化的代码中，我们使用了递归和剪枝策略。首先按照题目的要求，输入的4个数字保持不变，
不进行排序。在每一次运算中，我们首先尝试加法和乘法，因为它们的运算结果更少受到数字大小的影响。
然后，我们根据数字的大小关系尝试减法和除法，只进行必要的组合运算，避免重复运算。

值得注意的是，这种优化策略可以减少冗余计算，但对于某些输入情况仍需要遍历所有可能的组合。
因此，在最坏情况下仍然可能需要较长的计算时间。
'''

def find(nums):
    if len(nums) == 1:
        return abs(nums[0] - 24) <= 0.000001

    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            a = nums[i]
            b = nums[j]
            remaining_nums = []

            for k in range(len(nums)):
                if k != i and k != j:
                    remaining_nums.append(nums[k])

            # 尝试加法和乘法运算
            if find(remaining_nums + [a + b]) or find(remaining_nums + [a * b]):
                return True

            # 尝试减法运算
            if a > b and find(remaining_nums + [a - b]):
                return True
            if b > a and find(remaining_nums + [b - a]):
                return True

            # 尝试除法运算
            if b != 0 and find(remaining_nums + [a / b]):
                return True
            if a != 0 and find(remaining_nums + [b / a]):
                return True

    return False

while True:
    card = [int(x) for x in input().split()]
    if sum(card) == 0:
        break

    print("YES" if find(card) else "NO")

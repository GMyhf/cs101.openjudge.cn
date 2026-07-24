# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
def minMaxMonthlyExpense(N, M, expenses):
    def can_split(max_expense):
        """ 判断是否能合并至多 M 个花费，使最大花费不超过 max_expense """
        months = 1  # 记录当前使用的月份数
        current_sum = 0 # 当前月的开销
        for cost in expenses:
            if current_sum + cost > max_expense:
                months += 1
                if months > M:
                    return False
                current_sum = cost
            else:
                current_sum += cost
        return True

    # 可能的最小开销范围。所以二分是在 [left, right) 区间内进行的
    left, right = max(expenses), sum(expenses) + 1
    ans = -1
    while left < right: # 二分查找最小的 "最大月度开销"
        mid = (left + right) // 2
        if can_split(mid):
            ans = mid   # 记录可行的 `mid`
            right = mid # 继续尝试更小的值
        else:
            left = mid + 1
    return ans

# 读取输入
N, M = map(int, input().split())
expenses = [int(input()) for _ in range(N)]

# 计算并输出答案
print(minMaxMonthlyExpense(N, M, expenses))

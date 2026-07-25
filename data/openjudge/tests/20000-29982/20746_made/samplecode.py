# Source: /home/ubuntu/hongfei/2024spring-cs201/2024spring_dsa_problems.md
def min_employees(tasks, t):
    left, right = 1, max(tasks)
    while left < right:
        mid = (left + right) // 2
        total_hours = sum((task + mid - 1) // mid for task in tasks)
        if total_hours > t:
            left = mid + 1
        else:
            right = mid
    return left

# 读取输入并处理
tasks = list(map(int, input().split(',')))
t = int(input())
print(min_employees(tasks, t))

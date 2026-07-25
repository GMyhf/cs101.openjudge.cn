# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
def count_combinations(numbers, index, current_sum, count):
    if index >= len(numbers):
        if current_sum % 7 == 0:
            return count + 1
        else:
            return count
    
    # 选择取当前位置的数
    count = count_combinations(numbers, index + 1, current_sum + numbers[index], count)
    
    # 选择不取当前位置的数
    count = count_combinations(numbers, index + 1, current_sum, count)
    
    return count


# 主程序
t = int(input())
for _ in range(t):
    data = list(map(int, input().split()))
    n = data[0]
    numbers = data[1:]
    
    result = count_combinations(numbers, 0, 0, 0)
    print(result)

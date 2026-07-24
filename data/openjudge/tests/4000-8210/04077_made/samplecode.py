# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
def count_sequences(n):
    def dfs(push_num, stack, popped):
        nonlocal count
        # 如果已经弹出了 n 个数，说明这个出栈序列是合法的
        if popped == n:
            count += 1
            return
        # 尝试进栈：如果还有数字没进栈
        if push_num <= n:
            stack.append(push_num)
            dfs(push_num + 1, stack, popped)
            stack.pop()
        # 尝试出栈：如果栈不空
        if stack:
            top = stack.pop()
            dfs(push_num, stack, popped + 1)
            stack.append(top)

    count = 0
    dfs(1, [], 0)
    return count

# 读取输入
n = int(input())
print(count_sequences(n))

# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
def is_robot_making_loop(commands):
    # 初始位置和方向
    x, y = 0, 0
    direction = 'N'

    # 方向变换的规则，用字典表示
    left_turns = {'N': 'W', 'W': 'S', 'S': 'E', 'E': 'N'}
    right_turns = {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'}

    # 模拟机器人的移动
    for command in commands:
        if command == 'G':
            if direction == 'N':
                y += 1
            elif direction == 'S':
                y -= 1
            elif direction == 'E':
                x += 1
            elif direction == 'W':
                x -= 1
        elif command == 'L':
            direction = left_turns[direction]
        elif command == 'R':
            direction = right_turns[direction]

    # 如果机器人回到原点，或者不是面向北方（说明它会改变方向然后可能回到原点）
    return (x == 0 and y == 0) or direction != 'N'

# 读取输入并输出结果
commands = input().strip()
print(1 if is_robot_making_loop(commands) else 0)


# Source: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
import sys
from collections import deque


def solve():
    # 使用 sys.stdin.read 快速读取输入，适合处理 N = 10^5 的情况
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    N = int(input_data[0])
    players = input_data[1:]

    # 初始化存储结果的数组，未组队默认为 0
    ans = [0] * N

    # 定义三个队列存储不同职责玩家的索引
    T_q = deque()
    H_q = deque()
    D_q = deque()

    team_count = 0

    for i in range(N):
        role = players[i]
        if role == "T":
            T_q.append(i)
        elif role == "H":
            H_q.append(i)
        elif role == "D":
            D_q.append(i)

        # 检查是否满足组队条件：1 T, 1 H, 3 D
        if len(T_q) >= 1 and len(H_q) >= 1 and len(D_q) >= 3:
            team_count += 1
            # 取出最早进入队列的 5 名符合条件的玩家
            t_idx = T_q.popleft()
            h_idx = H_q.popleft()
            d1_idx = D_q.popleft()
            d2_idx = D_q.popleft()
            d3_idx = D_q.popleft()

            # 标记他们的队伍编号
            ans[t_idx] = team_count
            ans[h_idx] = team_count
            ans[d1_idx] = team_count
            ans[d2_idx] = team_count
            ans[d3_idx] = team_count

    # 输出结果，以空格分隔
    print(*(ans))


if __name__ == "__main__":
    solve()

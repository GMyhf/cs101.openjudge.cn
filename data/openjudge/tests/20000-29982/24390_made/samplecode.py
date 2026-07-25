# Source: /home/ubuntu/hongfei/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
from collections import deque


def solve():
    N = int(input().strip())
    s = input().strip()

    # 初始状态转成整数（二进制掩码）
    start = int(s, 2)
    #print(f"start = {start}")
    target1 = 0  # 全 0
    target2 = (1 << N) - 1  # 全 1

    # 预先计算每个位置的翻转掩码
    masks = []
    for i in range(N):
        mask = 1 << i
        if i > 0:
            mask |= 1 << (i - 1)
        if i < N - 1:
            mask |= 1 << (i + 1)
        masks.append(mask)

    # BFS
    q = deque([(start, 0)])
    visited = {start}

    while q:
        state, step = q.popleft()
        if state == target1 or state == target2:
            print(step)
            return
        for mask in masks:
            nxt = state ^ mask  # 翻转操作，就是「0→1，1→0」，等价于 XOR 1
            if nxt not in visited:
                visited.add(nxt)
                q.append((nxt, step + 1))


if __name__ == "__main__":
    solve()


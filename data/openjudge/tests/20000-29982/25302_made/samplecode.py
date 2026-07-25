# Source: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
def max_concurrent_connections(n, intervals):
    events = []
    for start, end in intervals:
        events.append((start, 1))  # 开始 +1
        events.append((end, -1))   # 结束 -1

    # 按时间排序，时间相同时结束事件在前
    events.sort(key=lambda x: (x[0], x[1]))

    current = 0
    max_concurrent = 0
    for time, delta in events:
        current += delta
        max_concurrent = max(max_concurrent, current)

    return max_concurrent

# 主程序处理多组数据
t = int(input())
for _ in range(t):
    n = int(input())
    intervals = [tuple(map(int, input().split())) for _ in range(n)]
    print(max_concurrent_connections(n, intervals))



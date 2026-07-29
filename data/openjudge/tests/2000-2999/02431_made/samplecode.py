# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 2431: Expedition
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/pctbook/02431/
# License: not declared in source collection; no license is inferred.
import sys
import heapq

N = int(input())
rawL = [list(map(int, input().split())) for _ in range(N)]
rawL.append([0, 0])
rawL.sort()

L, P = map(int, input().split())

N += 1

que = []
ans = 0
pos = L
tank = P

for i in range(N - 1, -1, -1):
    d = pos - rawL[i][0]  # 接下去要前进的距离

    while tank - d < 0:  # 不断加油直到油量足够行驶到下一个加油站
        if not que:
            print(-1)
            exit()

        tank += -heapq.heappop(que)
        ans += 1

    tank -= d
    pos = rawL[i][0]
    heapq.heappush(que, -rawL[i][1])

print(ans)

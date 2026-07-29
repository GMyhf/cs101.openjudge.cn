# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# Heading: 1042: Gone Fishing
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/01042/
# License: not declared in source collection; no license is inferred.
import sys
# 蒋子轩23工学院
from heapq import heappush, heappop
while True:
    n = int(input())
    if n == 0:
        break
    h = int(input()) * 12
    ans = -1 #最大钓鱼数量
    res = [0] * n #每个湖上所花费的时间
    f = list(map(int, input().split()))
    d = list(map(int, input().split()))
    t = [0] + (list(map(int, input().split())) if n > 1 else [])
    #枚举第几个湖泊结束
    #对于每种情况贪心算法，它在每个湖上都试图钓尽可能多的鱼，并始终优先考虑鱼的数量多的湖。
    for i in range(n):
        now = 0 #该情况钓鱼数量
        q = []  #优先队列
        lakes = [{'id': j, 'f': f[j], 'd': d[j]} for j in range(i + 1)]
        for lake in lakes:
            # 使得鱼的数量多的湖排在优先队列的前面（取负实现）。如果鱼的数量相同，那么ID小的湖会排在前面。
            heappush(q, (-lake['f'], lake['id']))
        tmp = [0] * n #该情况每个湖钓鱼时间
        time_left = h - sum(t[:i + 1]) #湖上剩余的时间
        while time_left > 0:
            fish_count, idx = heappop(q)
            fish_count = -fish_count #变回正数
            tmp[idx] += 1
            now += fish_count
            lakes[idx]['f'] -= lakes[idx]['d']
            if lakes[idx]['f'] < 0:
                lakes[idx]['f'] = 0
            heappush(q, (-lakes[idx]['f'], idx))
            time_left -= 1
        if now > ans:
            ans = now
            res = tmp.copy()
    print(", ".join(str(val * 5) for val in res))
    print("Number of fish expected:", ans)
    print()

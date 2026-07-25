# Source: /home/ubuntu/hongfei/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
from collections import deque
#import heapq

def bfs(s, e):
    q = deque()
    q.append((0, s, ''))
    vis = set()
    vis.add(s)
    # q = []
    #heapq.heappush(q, (0, s, ''))

    while q:
        step, pos, path = q.popleft()
        #step, pos, path = heapq.heappop(q)
        if pos == e:
            return step, path

        if pos * 3 not in vis:
            q.append((step+1, pos*3, path+'H'))
            vis.add(pos*3)
            #heapq.heappush(q, (step+1, pos*3, path+'H'))
        if int(pos // 2) not in vis:
            vis.add(int(pos//2))
            q.append((step+1, int(pos//2), path+'O'))
            #heapq.heappush(q, (step+1, int(pos//2), path+'O'))

while True:
    n, m = map(int, input().split())
    if n == 0 and m == 0:
        break
    step, path = bfs(n, m)
    print(step)
    print(path)

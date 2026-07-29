# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
# Heading: 1724: ROADS
# Fenced code block index: 8
# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md
# Upstream problem: http://cs101.openjudge.cn/2024sp_routine/01724/
# License: not declared in source collection; no license is inferred.
import sys
class Road:
    def __init__(self,d,L,t):
       self.d,self.L,self.t = d,L,t


def dfs(s, total_cost, total_length, visited, city_map, min_lengths, k):
    global min_length
    if s == n:
        min_length = min(min_length, total_length)
        return
    for i in range(len(city_map[s])):
        d, L, t = city_map[s][i].d, city_map[s][i].L, city_map[s][i].t
        if visited[d]:
            continue
        cost = t + total_cost
        length = L + total_length
        if cost > k :   # 可行性剪枝：超过预算
            continue
        if (length >= min_length or # 最优性剪枝：超过当前最优解
                length >= min_lengths[d][cost]): # 处处最优性剪枝：超过已经搜索到的最优解
            continue
        min_lengths[d][cost] = length
        visited[d] = True
        dfs(d, cost, length, visited, city_map, min_lengths, k)
        visited[d] = False


k,n,r = int(input()),int(input()),int(input())
city_map = [[] for i in range(n+1)] #邻接表。city_map[i]是从点i有路连到的城市集合
for _ in range(r):
    r = Road(0, 0, 0)
    s, r.d, r.L, r.t = map(int, input().split())
    if s != r.d:
        city_map[s].append(r)
INF = float('inf')
min_length = INF

#min_lengths[i][j]表示从1到i点，花销为j的最短路径的长度
min_lengths = [[INF] * (k + 1) for _ in range(n + 1)]
visited = [False] * (n + 1)
visited[1] = True
dfs(1, 0, 0, visited, city_map, min_lengths, k)
if min_length < INF:
    print(min_length)
else:
    print(-1)

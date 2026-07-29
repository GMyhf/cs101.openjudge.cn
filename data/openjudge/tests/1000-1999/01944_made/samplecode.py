# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
# Heading: 1944: Fiber Communications
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/01944/
# License: not declared in source collection; no license is inferred.
import sys
# https://www.cnblogs.com/lightspeedsmallson/p/4785834.html
N, P = map(int, input().split())
node_one = []

for i in range(P):
    Q1, Q2 = map(int, input().split())
    node_one.append({'start': min(Q1, Q2), 'end': max(Q1, Q2)})

node_one.sort(key=lambda x: (x['start'], x['end']))

INF = float('inf')
ans = INF

for i in range(1, N + 1):
    to = [0] * (N + 1)

    for j in range(P):
        if node_one[j]['end'] >= i + 1 and node_one[j]['start'] <= i:
            to[1] = max(to[1], node_one[j]['start'])
            to[node_one[j]['end']] = N + 1
        else:
            to[node_one[j]['start']] = max(to[node_one[j]['start']], node_one[j]['end'])

    duandian = 0
    result = 0

    for j in range(1, N + 1):
        if to[j] == 0:
            continue

        if to[j] > duandian:
            if j >= duandian:
                result += (to[j] - j)
            else:
                result += (to[j] - duandian)

            duandian = to[j]

    ans = min(ans, result)

print(ans)

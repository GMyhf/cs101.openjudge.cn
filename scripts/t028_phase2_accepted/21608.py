# External reference: http://cs101.openjudge.cn/practice/21608/statistics/
# Accepted submission: 51475686
# Source: http://cs101.openjudge.cn/practice/solution/51475686/
# License: not declared on the submission page; no license is inferred.

def fun(graph, start):
    friends = [start]
    def dfs(graph,start):
        if start in graph:
            for node in graph[start]:
                if node not in friends:
                    friends.append(node)
                    dfs(graph, node)
        return len(friends)
    return dfs(graph,start)
n = int(input())
graph = {}
start_l = []
for _ in range(n):
    l = input().split()
    if l[2] == '-1':
        continue
    else:
        graph[l[0]] = l[2:]
    start_l.append(l[0])
res = [fun(graph, x) for x in start_l]
print(max(res))

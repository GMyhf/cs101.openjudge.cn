"""仓库自产参考：按配方依赖拓扑计算最小串行制备时间；非外部提交。"""
from collections import deque

def solve(text):
    values=iter(map(int,text.split())); n=next(values); recipes=[]; parents=[[] for _ in range(n)]; degree=[]
    for u in range(n):
        row=[]; dependencies=set()
        for _ in range(next(values)):
            t=next(values); x=next(values); ingredients=[next(values) for _ in range(x)]
            row.append((t,ingredients)); dependencies.update(ingredients)
        recipes.append(row); degree.append(len(dependencies))
        for v in dependencies: parents[v].append(u)
    queue=deque(u for u in range(n) if degree[u]==0); costs=[0]*n
    while queue:
        u=queue.popleft()
        costs[u]=min(t+sum(costs[v] for v in ingredients) for t,ingredients in recipes[u])
        for parent in parents[u]:
            degree[parent]-=1
            if degree[parent]==0: queue.append(parent)
    return str(costs[0])

if __name__=='__main__':
    import sys
    print(solve(sys.stdin.read()))

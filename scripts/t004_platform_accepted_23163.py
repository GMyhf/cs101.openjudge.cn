# External reference: statistics page /practice/23163/
# Accepted submission: 52702740
# Source: http://cs101.openjudge.cn/practice/solution/52702740/
# License: not declared on the submission page; no license is inferred.

n, m = map(int, input().split())
parent = list(range(n))
rank = [0] * n

def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x

def union(x, y):
    rx, ry = find(x), find(y)
    if rx == ry:
        return False
    if rank[rx] < rank[ry]:
        parent[rx] = ry
    elif rank[rx] > rank[ry]:
        parent[ry] = rx
    else:
        parent[ry] = rx
        rank[rx] += 1
    return True

has_cycle = False
for _ in range(m):
    u, v = map(int, input().split())
    if not union(u, v):
        has_cycle = True

# 检查连通性：所有点是否属于同一集合
root = find(0)
connected = all(find(i) == root for i in range(n))

print("connected:yes" if connected else "connected:no")
print("loop:yes" if has_cycle else "loop:no")
# Source: /home/ubuntu/hongfei/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
n, m = map(int, input().split())
parent=[i for i in range(n)]
edges=[]
diff=[]
for _ in range(m):
    a, b, c = map(int, input().split())
    if c!=1:
        edges.append((a, b))
    else:
        diff.append((a, b))

def find(x):
    if parent[x] != x:
        parent[x] = find(parent[x])
    return parent[x]
def union(x, y):
    nx, ny = find(x), find(y)
    if nx != ny:
        parent[ny] = nx
        #return True
    #return False

for a, b in edges:
    union(a, b)

for a, b in diff:
    if find(a) == find(b):
        print('NO')
        exit()
print('YES')

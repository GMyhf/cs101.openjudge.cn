# External reference: statistics page /practice/27385/
# Accepted submission: 48288982
# Source: http://cs101.openjudge.cn/practice/solution/48288982/
# License: not declared on the submission page; no license is inferred.

k = int(input())
n = 1 << k
arr = list(map(int, input().split()))
max_tree = [0] * (n << 1)
min_tree = [0] * (n << 1)
inf = float('inf')

for i in range(n):
    max_tree[n + i] = arr[i]
    min_tree[n + i] = arr[i]
for i in range(n - 1, 0, -1):
    max_tree[i] = max(max_tree[i << 1], max_tree[i << 1 | 1])
    min_tree[i] = min(min_tree[i << 1], min_tree[i << 1 | 1])

def update(index, value):
    cur = index + n
    max_tree[cur] = value
    min_tree[cur] = value
    while cur > 1:
        max_tree[cur >> 1] = max(max_tree[cur], max_tree[cur ^ 1])
        min_tree[cur >> 1] = min(min_tree[cur], min_tree[cur ^ 1])
        cur >>= 1

def query(l, r):
    res_max, res_min = -inf, inf
    left, right = l + n, r + n
    while left < right:
        if left & 1:
            res_max = max(res_max, max_tree[left])
            res_min = min(res_min, min_tree[left])
            left += 1
        if right & 1:
            right -= 1
            res_max = max(res_max, max_tree[right])
            res_min = min(res_min, min_tree[right])
        left >>= 1
        right >>= 1
    return res_max, res_min

for _ in range(int(input())):
    t, x, y = map(int, input().split())
    if t == 1:
        max_num, min_num = query(x, y + 1)
        if max_num <= 0:
            ans = max_num * max_num
        elif min_num >= 0:
            ans = min_num * min_num
        else:
            ans = min_num * max_num
        print(ans)
    else:
        update(x, y)
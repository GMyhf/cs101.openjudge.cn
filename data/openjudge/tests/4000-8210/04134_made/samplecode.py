# External reference: statistics page /practice/04134/
# Accepted submission: 51059237
# Source: http://cs101.openjudge.cn/practice/solution/51059237/
# License: not declared on the submission page; no license is inferred.

n = int(input())
arr = list(map(int, input().split()))
m = int(input())

for _ in range(m):
    x = int(input())

    # --- 手写二分（不能使用函数） ---
    l, r = 0, n-1
    while l <= r:
        mid = (l + r) // 2
        if arr[mid] < x:
            l = mid + 1
        else:
            r = mid - 1
    pos = l
    # --- 二分结束 ---

    candidates = []
    if pos < n:
        candidates.append(arr[pos])
    if pos > 0:
        candidates.append(arr[pos - 1])

    # 选和 x 最接近的，如果差一样，取较小的
    best = min(candidates, key=lambda v: (abs(v - x), v))

    print(best)
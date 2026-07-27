# External reference: statistics page /practice/21508/
# Accepted submission: 52213688
# Source: http://cs101.openjudge.cn/practice/solution/52213688/
# License: not declared on the submission page; no license is inferred.

import sys
from collections import deque

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return

    n, m = map(int, data[:2])
    a = list(map(int, data[2:2+n]))

    # 计算前缀和
    S = [0] * (n + 1)
    for i in range(1, n + 1):
        S[i] = S[i-1] + a[i-1]

    # 单调队列维护候选左端点
    q = deque()
    q.append(0)  # 初始左端点 S[0] = 0
    ans = -float('inf')

    for r in range(1, n + 1):
        # 移除超出窗口的左端点
        while q and q[0] < r - m:
            q.popleft()

        # 更新答案
        if q:
            ans = max(ans, S[r] - S[q[0]])

        # 维护队列单调递增
        while q and S[q[-1]] >= S[r]:
            q.pop()
        q.append(r)

    print(ans)

if __name__ == "__main__":
    main()
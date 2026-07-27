# External reference: /practice/30370/statistics/
# Accepted submission: 52723545
# Source: http://cs101.openjudge.cn/practice/solution/52723545/
# License: not declared on the submission page; no license is inferred.

import bisect

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    a = list(map(int, data[1:n+1]))
    
    ans = 0
    # 遍历所有可能的选中人数k
    for k in range(0, n + 1):
        # 二分查找：第一个 >=k 的位置 = 小于k的元素个数
        cnt = bisect.bisect_left(a, k)
        # 条件1：小于k的元素数量恰好等于k
        # 条件2：数组中没有元素等于k
        if cnt == k and (cnt == n or a[cnt] != k):
            ans += 1
    print(ans)

if __name__ == "__main__":
    main()
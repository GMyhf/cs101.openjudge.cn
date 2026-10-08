# External reference: http://cs101.openjudge.cn/practice/02549/statistics/
# Accepted submission: 51482198
# Source: http://cs101.openjudge.cn/practice/solution/51482198/
# License: not declared on the submission page; no license is inferred.
# 2026-10-08 本地修正：上面引用的原始代码在题面范围内有缺陷，已按题面改过，与原提交不再逐字一致（见 CHANGELOG）。
# 原写法对每组 (d, c) 都重新扫一遍 a 找 a+b=d-c，O(n^3)，n=1000 时超时。
# 新写法先把所有数对和 a+b 预处理进哈希表，再从大到小枚举 d、枚举 c 直接查表，O(n^2)。
import sys


def solve():
    input_data = sys.stdin.read().split()
    idx = 0
    results = []
    while True:
        n = int(input_data[idx]); idx += 1
        if n == 0:
            break
        S = sorted(map(int, input_data[idx:idx + n])); idx += n

        # 数对和 -> 第一对下标（编码成 i*n+j 省内存）；同和的其余数对放 more。
        # 元素互不相同，所以同一个和的数对两两不相交，最多 2 对会和 c、d 冲突，留 3 对就够。
        first = {}
        more = {}
        for i in range(n):
            a = S[i]
            for j in range(i + 1, n):
                t = a + S[j]
                if t not in first:
                    first[t] = i * n + j
                else:
                    lst = more.setdefault(t, [])
                    if len(lst) < 2:
                        lst.append(i * n + j)

        ans = None
        # 从大到小枚举d（作为答案）
        for d_idx in range(n - 1, -1, -1):
            d = S[d_idx]
            # 枚举c（作为减数）
            for c_idx in range(n):
                if c_idx == d_idx:
                    continue
                target = d - S[c_idx]
                p = first.get(target)
                if p is None:
                    continue
                for code in [p] + more.get(target, []):
                    a_idx, b_idx = divmod(code, n)
                    if a_idx not in (c_idx, d_idx) and b_idx not in (c_idx, d_idx):
                        ans = d
                        break
                if ans is not None:
                    break
            if ans is not None:
                break
        results.append("no solution" if ans is None else str(ans))
    print("\n".join(results))


if __name__ == "__main__":
    solve()

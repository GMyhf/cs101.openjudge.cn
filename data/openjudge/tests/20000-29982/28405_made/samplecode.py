# External reference: statistics page /practice/28405/
# Accepted submission: 52736793
# Source: http://cs101.openjudge.cn/practice/solution/52736793/
# License: not declared on the submission page; no license is inferred.
# 2026-10-08 本地重写：上面引用的原始代码在题面范围内有缺陷，下面已换成按题面重写的实现，不再是原提交（原因见下方注释与 CHANGELOG）。
# 28405 小明的刷题计划 参考解（二分答案 + 贪心）。
# 原外部参考（提交 52736793）切天后把 maxn 置为 -1，丢掉了新一天第一题的耗时作为最大值候选，
# 例如 4 / 7 1 718 1 / 2 应输出 1 却输出 8，已弃用。
# 判定 T 可行：从左到右贪心，当天「总和 - 最大值」超过 T 就另起一天；
# 子区间的「总和 - 最大值」不超过原区间，所以贪心尽量延长当天是最优的。
import sys


def main():
    d = sys.stdin.buffer.read().split()
    n = int(d[0])
    a = list(map(int, d[1:1 + n]))
    m = int(d[1 + n])
    if n <= m:
        print(0)
        return

    def ok(T):
        cnt = 1
        s = 0
        mx = 0
        for x in a:
            if x > mx:
                ns = s + mx
                nm = x
            else:
                ns = s + x
                nm = mx
            if ns > T:
                cnt += 1
                if cnt > m:
                    return False
                s = 0
                mx = x
            else:
                s = ns
                mx = nm
        return True

    lo, hi = 0, sum(a) - max(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid
        else:
            lo = mid + 1
    print(lo)


main()

# External reference: http://cs101.openjudge.cn/practice/02744/statistics/
# Accepted submission: 46688613
# Source: http://cs101.openjudge.cn/practice/solution/46688613/
# License: not declared on the submission page; no license is inferred.
# 2026-10-08 本地重写：上面引用的原始代码在题面范围内有缺陷，下面已换成按题面重写的实现，不再是原提交（原因见下方注释与 CHANGELOG）。
# 暴力参考解：枚举最短串的全部子串（由长到短），检查它或其反串是否为每个串的子串。
import sys
def main():
    data = sys.stdin.read().split()
    p = 0; t = int(data[p]); p += 1; out = []
    for _ in range(t):
        n = int(data[p]); p += 1
        ss = data[p:p + n]; p += n
        s = min(ss, key=len); best = 0
        for L in range(len(s), 0, -1):
            if any(all(x in y or x[::-1] in y for y in ss) for x in (s[i:i + L] for i in range(len(s) - L + 1))):
                best = L; break
        out.append(str(best))
    print("\n".join(out))
main()

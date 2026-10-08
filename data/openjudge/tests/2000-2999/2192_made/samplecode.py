# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
# Heading: 2192: Zipper
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md
# Upstream problem: http://cs101.openjudge.cn/2024sp_routine/02192/
# License: not declared in source collection; no license is inferred.
# 袁籁2300010728
# 2026-10-08 本地重写：上面引用的原始代码在题面范围内有缺陷，下面已换成按题面重写的实现，不再是原提交（原因见下方注释与 CHANGELOG）。
# 参考解（本仓重写）：按 c 的前缀推进，维护可达的 a 已用长度集合，最坏 O(|a||b|)。
import sys
def main():
    data = sys.stdin.read().split()
    n = int(data[0]); out = []
    for t in range(n):
        a, b, c = data[1 + 3 * t: 4 + 3 * t]
        ok = len(c) == len(a) + len(b)
        cur = {0}
        if ok:
            for k, ch in enumerate(c):
                nxt = set()
                for i in cur:
                    j = k - i
                    if i < len(a) and a[i] == ch: nxt.add(i + 1)
                    if j < len(b) and b[j] == ch: nxt.add(i)
                cur = nxt
                if not cur: break
        out.append("Data set %d: %s" % (t + 1, "yes" if ok and cur else "no"))
    print("\n".join(out))
main()

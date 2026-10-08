# External reference: http://cs101.openjudge.cn/practice/01308/statistics/
# Accepted submission: 52642572
# Source: http://cs101.openjudge.cn/practice/solution/52642572/
# License: not declared on the submission page; no license is inferred.
# 2026-10-08 本地重写：上面引用的原始代码在题面范围内有缺陷，下面已换成按题面重写的实现，不再是原提交（原因见下方注释与 CHANGELOG）。
# 修正版参考解（审计时替换）：原 Accepted 提交 52642572 在首组于 BFS 前判否时
# 引用未定义的 visited 而崩溃，且发现重复访问只跳出内层循环；这里按定义重写：
# 空集是树；否则入度均 <=1、恰一个入度 0 的根、且从根可达全部点。
import sys
from collections import defaultdict


def main():
    t = list(map(int, sys.stdin.read().split()))
    out = []
    case = 0
    edges = []
    for i in range(0, len(t) - 1, 2):
        u, v = t[i], t[i + 1]
        if u < 0 and v < 0:
            break
        if u == 0 and v == 0:
            case += 1
            ok = True
            if edges:
                indeg = defaultdict(int)
                adj = defaultdict(list)
                nodes = set()
                for a, b in edges:
                    indeg[b] += 1
                    adj[a].append(b)
                    nodes.add(a)
                    nodes.add(b)
                roots = [x for x in nodes if indeg[x] == 0]
                if len(roots) != 1 or any(indeg[x] > 1 for x in nodes):
                    ok = False
                else:
                    seen = {roots[0]}
                    stack = [roots[0]]
                    while stack:
                        x = stack.pop()
                        for y in adj[x]:
                            if y not in seen:
                                seen.add(y)
                                stack.append(y)
                    ok = len(seen) == len(nodes)
            out.append(f"Case {case} is {'a' if ok else 'not a'} tree.")
            edges = []
        else:
            edges.append((u, v))
    print("\n".join(out))


if __name__ == "__main__":
    main()

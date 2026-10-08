# Source: /home/ubuntu/hongfei/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md
# 2026-10-08 本地重写：上面引用的原始代码在题面范围内有缺陷，下面已换成按题面重写的实现，不再是原提交（原因见下方注释与 CHANGELOG）。
# 原 samplecode（来源 2020fall_cs101.openjudge.cn_problems.md）在同权值内部节点比较时抛 TypeError，
# 且没有按「字符集最小字符」打破平局；以下为按题面规则重写的版本，与 producecase.py 的 REFERENCE_SOURCE 相同。
# 修正版参考解：按题面规则比较节点——先比权值，权值相同比「字符集里最小字符」，小者作左子。
# 2026-10-08 本地修正：上面引用的原始代码在题面范围内有缺陷，已按题面改过，与原提交不再逐字一致（见 CHANGELOG）。
import heapq
import sys

def main():
    lines = sys.stdin.read().split("\n")
    n = int(lines[0])
    heap = []
    for i in range(1, n + 1):
        c, w = lines[i].split()
        heapq.heappush(heap, (int(w), c, c))          # (权值, 最小字符, 子树)
    while len(heap) > 1:
        w1, m1, t1 = heapq.heappop(heap)
        w2, m2, t2 = heapq.heappop(heap)
        heapq.heappush(heap, (w1 + w2, min(m1, m2), (t1, t2)))
    root = heap[0][2]
    codes = {}
    def walk(t, path):
        if isinstance(t, str):
            codes[t] = path
        else:
            walk(t[0], path + "0"); walk(t[1], path + "1")
    walk(root, "")
    out = []
    for line in lines[n + 1:]:
        s = line.strip()
        if not s:
            continue
        if s[0] in "01":
            res, t = [], root
            for b in s:
                t = t[0] if b == "0" else t[1]
                if isinstance(t, str):
                    res.append(t); t = root
            out.append("".join(res))
        else:
            out.append("".join(codes[c] for c in s))
    print("\n".join(out))

main()

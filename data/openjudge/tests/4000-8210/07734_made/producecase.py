"""7734 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001c
生成器与循环取自 scripts/build_001c.py（批次 001c），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import re
import subprocess
import tempfile
from pathlib import Path

NUMBER = 7734
SAMPLE_IN = '2\n3 3\n1 2\n2 3\n1 3\n4 2\n1 2\n3 4\n'
SAMPLE_OUT = 'Scenario #1:\nSuspicious bugs found!\n\nScenario #2:\nNo suspicious bugs found!\n'
REFERENCE_SOURCE = 'import sys\nsys.setrecursionlimit(1000000)\n\n\ndef solve():\n    T = int(input())\n\n    for case in range(1, T + 1):\n        n, m = map(int, input().split())\n\n        # 扩展域：1~n 表示性别A，n+1~2n 表示性别B\n        parent = list(range(2 * n + 1))\n\n        def find(i):\n            if parent[i] == i:\n                return i\n            parent[i] = find(parent[i])\n            return parent[i]\n\n        def union(i, j):\n            root_i = find(i)\n            root_j = find(j)\n            if root_i != root_j:\n                parent[root_i] = root_j\n\n        suspicious = False\n        for _ in range(m):\n            u, v = map(int, input().split())\n            if suspicious: continue\n\n            # 如果 u 和 v 已经在同一个性别域里，说明他们是同性！\n            if find(u) == find(v):\n                suspicious = True\n            else:\n                # u 恋爱对象必须是 v 的异性分身\n                union(u, v + n)\n                # v 恋爱对象必须是 u 的异性分身\n                union(v, u + n)\n\n        print(f"Scenario #{case}:")\n        if suspicious:\n            print("Suspicious bugs found!")\n        else:\n            print("No suspicious bugs found!")\n        print()\n\n\nsolve()\n'

def valid(text):
    """题面：第一行组数 T；每组首行「虫子数 n（1≤n≤2000） 交互数 m（≤1000000）」；随后 m 行「u v」，
    为两只（不同的）虫子的标号，编号 1..n。"""
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    num = r"[1-9][0-9]*"
    if not lines or not re.fullmatch(num, lines[0]):
        return False
    t = int(lines[0]); pos = 1
    for _ in range(t):
        if pos >= len(lines):
            return False
        m0 = re.fullmatch(r"([1-9][0-9]*) (0|[1-9][0-9]*)", lines[pos])
        if not m0:
            return False
        n, m = int(m0.group(1)), int(m0.group(2)); pos += 1
        if not (1 <= n <= 2000 and m <= 1000000) or pos + m > len(lines):
            return False
        for line in lines[pos:pos + m]:
            e = re.fullmatch(r"([1-9][0-9]*) ([1-9][0-9]*)", line)
            if not e:
                return False
            u, v = int(e.group(1)), int(e.group(2))
            if not (u <= n and v <= n and u != v):
                return False
        pos += m
    return pos == len(lines)


def scenario(r, n, m, odd, odd_pos=None):
    """n 只虫子、m 次交互；odd=False 时按随机二染色只连异色（无可疑），
    odd=True 时在第 odd_pos 条处插入一条同色且已连通的边（形成奇环，可疑）。"""
    color = [r.randint(0, 1) for _ in range(n + 1)]
    order = list(range(1, n + 1)); r.shuffle(order)
    edges = []
    # 先连一棵生成树（异色边），保证大连通块；颜色不足时补上
    for i in range(1, len(order)):
        u = order[i]; v = order[r.randint(max(0, i - r.choice([1, 3, i])), i - 1)]
        if color[u] == color[v]:
            color[u] ^= 1
            # 只在当前树之外的点才可翻色，这里 u 是新加点，翻色安全
        edges.append((u, v) if r.random() < .5 else (v, u))
    edges = edges[:m]
    while len(edges) < m:
        u = r.randint(1, n); v = r.randint(1, n)
        if u != v and color[u] != color[v]:
            edges.append((u, v))
        elif n == 2 or all(c == color[1] for c in color[1:]):
            break
    r.shuffle(edges) if r.random() < .3 else None
    if odd and n >= 3:
        same = [x for x in range(1, n + 1) if color[x] == color[order[0]]]
        if len(same) >= 2:
            u, v = r.sample(same, 2)
            pos = len(edges) if odd_pos is None else min(odd_pos, len(edges))
            # 奇边放在 pos 处；若 pos 处尚未连通，则后续的生成树边会把它连成奇环
            edges.insert(pos, (u, v))
            if edges: edges.pop()            # 保持总数为 m
            if (u, v) not in edges: edges.append((u, v))
    return f"{n} {len(edges)}\n" + "".join(f"{a} {b}\n" for a, b in edges)

def odd_cycle(n):
    # 1-2-3-...-n-1 的环：n 为奇数时可疑，偶数时无可疑
    return f"{n} {n}\n" + "".join(f"{i} {i % n + 1}\n" for i in range(1, n + 1))

def g7734(r, idx):
    parts = []
    if idx == 1:      # 最小规模：1 只虫子 0 次交互；2 只虫子 1 次交互；同一对重复交互
        parts = ["1 0\n", "2 1\n1 2\n", "2 3\n1 2\n2 1\n1 2\n", odd_cycle(3)]
    elif idx == 2:    # 奇/偶长环
        parts = [odd_cycle(4), odd_cycle(5), odd_cycle(2000), odd_cycle(1999)]
    elif idx <= 9:    # 多组小数据，可疑/不可疑混合（前一组可疑时后续须重置状态）
        for _ in range(r.randint(2, 10)):
            n = r.randint(2, 30); m = r.randint(0, 60)
            parts.append(scenario(r, n, m, r.random() < .5, r.randint(0, m)))
    elif idx <= 14:   # 中等规模
        for _ in range(r.randint(1, 4)):
            n = r.randint(100, 2000); m = r.randint(n, 15000)
            parts.append(scenario(r, n, m, r.random() < .5, r.randint(0, m)))
    else:             # 大规模：n=2000，交互数受 1MB 文件上限约束取 ~9 万
        if idx in (15, 16):     # 单组，无可疑 / 奇边藏在最后
            parts = [scenario(r, 2000, 90000, idx == 16)]
        elif idx == 17:         # 奇边一开始就出现，之后仍有大量交互需读完，后面再跟一组无可疑
            parts = [scenario(r, 2000, 45000, True, 5), scenario(r, 2000, 44000, False)]
        elif idx == 18:
            parts = [scenario(r, 2000, 44000, False), scenario(r, 2000, 45000, True, 30000)]
        else:
            parts = [scenario(r, r.randint(1500, 2000), 9000, r.random() < .5, r.randint(0, 9000)) for _ in range(10)]
    return f"{len(parts)}\n" + "".join(parts)

def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        cases.append(g7734(random.Random(NUMBER + i), i))
    assert all(valid(c) for c in cases), "有数据越出题面约束"
    assert len(set(cases)) == len(cases), "有重复数据"
    assert all(len(c.encode()) <= 10**6 for c in cases), "输入超过 1MB"
    return cases

def solve_reference(content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE)
        handle.flush()
        result = subprocess.run(["python3", handle.name], input=content, text=True,
                                capture_output=True, timeout=120, check=True)
    return result.stdout


def main():
    cases = build_cases()
    assert cases[0] == SAMPLE_IN, "第 0 组必须是题面样例"
    assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split(), "参考解法跑不出样例输出"
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for index, content in enumerate(cases):
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")


if __name__ == "__main__":
    main()

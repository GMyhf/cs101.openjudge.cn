import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'import sys\nfrom operator import itemgetter\n\ndef solve():\n    # 使用生成器逐个读取输入，节省内存\n    def get_tokens():\n        for line in sys.stdin:\n            for word in line.split():\n                yield word\n    \n    tokens = get_tokens()\n    \n    try:\n        n = int(next(tokens))\n        m = int(next(tokens))\n    except (StopIteration, ValueError):\n        return\n    \n    size = n * m\n    # 特判：如果只有一个区块，海拔差最大值为0\n    if size <= 1:\n        if size == 1:\n            print(0)\n        return\n\n    # 读取所有海拔高度，存储在扁平化的1D列表中\n    h = [0] * size\n    for i in range(size):\n        h[i] = int(next(tokens))\n    \n    # 构造所有的边 (权重, 点u, 点v)\n    edges = []\n    for r in range(n):\n        offset = r * m\n        for c in range(m):\n            u = offset + c\n            # 添加向右的边\n            if c + 1 < m:\n                v = u + 1\n                diff = h[u] - h[v]\n                edges.append((diff if diff >= 0 else -diff, u, v))\n            # 添加向下的边\n            if r + 1 < n:\n                v = u + m\n                diff = h[u] - h[v]\n                edges.append((diff if diff >= 0 else -diff, u, v))\n    \n    # 释放海拔列表以节省内存\n    h = None\n    \n    # 按权重从小到大排序\n    edges.sort(key=itemgetter(0))\n    \n    # 并查集初始化\n    parent = list(range(size))\n    \n    # 路径压缩的并查集查找函数\n    def find(i):\n        root = i\n        while parent[root] != root:\n            root = parent[root]\n        curr = i\n        while parent[curr] != root:\n            # 路径压缩：直接指向根节点\n            parent[curr], curr = root, parent[curr]\n        return root\n\n    start_node = 0\n    end_node = size - 1\n    \n    # 依次加入边，直到起点和终点连通\n    for diff, u, v in edges:\n        root_u = find(u)\n        root_v = find(v)\n        \n        if root_u != root_v:\n            parent[root_u] = root_v\n            # 检查起点(0,0)和终点(n-1,m-1)是否连通\n            if find(start_node) == find(end_node):\n                print(diff)\n                return\n\nif __name__ == "__main__":\n    solve()\n'
SAMPLE_IN = '4 5\n5 3 3 7 9\n5 5 4 2 8\n9 1 1 7 10\n9 8 10 1 7\n'
import re
SEED_BASE = 28972
_INT = re.compile(r'-?(0|[1-9][0-9]*)$')

def _ints(line):
    t = line.split(' ')
    if any(not _INT.match(x) for x in t): return None
    return [int(x) for x in t]

def valid(text):
    """题面：第一行 n m（1 ≤ n, m ≤ 400），接下来 n 行每行 m 个正整数 h，1 ≤ h ≤ 10^9。"""
    if not text.endswith('\n'): return False
    L = text[:-1].split('\n')
    h = _ints(L[0])
    if h is None or len(h) != 2: return False
    n, m = h
    if not (1 <= n <= 400 and 1 <= m <= 400) or len(L) != n + 1: return False
    for line in L[1:]:
        a = _ints(line)
        if a is None or len(a) != m or any(not 1 <= x <= 10**9 for x in a): return False
    return True

def generate_case(r):
    n, m = r.randint(1, 12), r.randint(1, 12)
    rows = [[r.randint(1, 100) for _ in range(m)] for _ in range(n)]
    assert len(rows) == n and all(len(row) == m and min(row) >= 1 for row in rows)
    return f"{n} {m}\n" + "\n".join(" ".join(map(str, row)) for row in rows) + "\n"

def _fmt(rows):
    return f"{len(rows)} {len(rows[0])}\n" + "\n".join(" ".join(map(str, row)) for row in rows) + "\n"

def _snake(r, n, m, low, high, step):
    # 蛇形走廊：走廊上相邻差 ≤ step，其余格随机（多为大落差），最优路径必须向上/向左折返
    g = [[r.randint(*high) for _ in range(m)] for _ in range(n)]
    cells = []
    for i in range(0, n, 2):
        cols = list(range(m)) if (i // 2) % 2 == 0 else list(range(m - 1, -1, -1))
        cells += [(i, j) for j in cols]
        if i + 1 < n:
            j = cols[-1]
            cells.append((i + 1, j))
            if i + 1 == n - 1:
                cells += [(i + 1, c) for c in (range(1, m) if j == 0 else [])]
    cells = cells[:cells.index((n - 1, m - 1)) + 1]
    v = r.randint(*low)
    for (i, j) in cells:
        g[i][j] = v
        v = min(max(v + r.randint(-step, step), 1), 10**9)
    return g

def extra_cases():
    r = random.Random(289720)
    out = []
    out.append("1 1\n7\n")                                          # 单格，答案 0
    out.append("1 2\n1 1000000000\n")                               # 极值差 999999999
    out.append(_fmt([[r.randint(1, 10**9)] for _ in range(400)]))     # 400×1，路径唯一
    out.append(_fmt([[r.randint(1, 10**9) for _ in range(400)]]))     # 1×400
    out.append(_fmt([[123456789] * 37 for _ in range(53)]))          # 全相等，答案 0
    out.append(_fmt([[1 if (i + j) % 2 else 10**9 for j in range(30)] for i in range(30)]))  # 棋盘极值
    # 满规模 400×400（值域压到 5 位以内以控制文件大小）
    out.append(_fmt([[r.randint(1, 99999) for _ in range(400)] for _ in range(400)]))
    out.append(_fmt(_snake(r, 400, 400, (40000, 60000), (1, 99999), 30)))
    # 300×300 满值域
    out.append(_fmt([[r.randint(1, 10**9) for _ in range(300)] for _ in range(300)]))
    out.append(_fmt(_snake(r, 299, 300, (10**8, 9 * 10**8), (1, 10**9), 1000)))
    # 中等规模蛇形 / 随机长条
    out.append(_fmt(_snake(r, 41, 37, (1000, 2000), (1, 10**9), 5)))
    out.append(_fmt(_snake(r, 2, 400, (1, 100), (1, 10**9), 3)))
    out.append(_fmt([[r.randint(1, 10**9) for _ in range(200)] for _ in range(3)]))
    out.append(_fmt([[r.randint(1, 10) for _ in range(250)] for _ in range(250)]))
    return out

def build_cases():
    seen = [SAMPLE_IN]
    cases = []
    for index in range(40):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(SEED_BASE + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content); cases.append(content)
    for content in extra_cases():
        assert content not in cases, "duplicate extra case"
        cases.append(content)
    for content in cases:
        assert valid(content), content[:80]
    return cases

def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        for index, content in enumerate(build_cases()):
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=60, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

if __name__ == "__main__":
    main()

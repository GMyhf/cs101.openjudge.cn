import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'import sys\nfrom operator import itemgetter\n\ndef solve():\n    # 使用生成器逐个读取输入，节省内存\n    def get_tokens():\n        for line in sys.stdin:\n            for word in line.split():\n                yield word\n    \n    tokens = get_tokens()\n    \n    try:\n        n = int(next(tokens))\n        m = int(next(tokens))\n    except (StopIteration, ValueError):\n        return\n    \n    size = n * m\n    # 特判：如果只有一个区块，海拔差最大值为0\n    if size <= 1:\n        if size == 1:\n            print(0)\n        return\n\n    # 读取所有海拔高度，存储在扁平化的1D列表中\n    h = [0] * size\n    for i in range(size):\n        h[i] = int(next(tokens))\n    \n    # 构造所有的边 (权重, 点u, 点v)\n    edges = []\n    for r in range(n):\n        offset = r * m\n        for c in range(m):\n            u = offset + c\n            # 添加向右的边\n            if c + 1 < m:\n                v = u + 1\n                diff = h[u] - h[v]\n                edges.append((diff if diff >= 0 else -diff, u, v))\n            # 添加向下的边\n            if r + 1 < n:\n                v = u + m\n                diff = h[u] - h[v]\n                edges.append((diff if diff >= 0 else -diff, u, v))\n    \n    # 释放海拔列表以节省内存\n    h = None\n    \n    # 按权重从小到大排序\n    edges.sort(key=itemgetter(0))\n    \n    # 并查集初始化\n    parent = list(range(size))\n    \n    # 路径压缩的并查集查找函数\n    def find(i):\n        root = i\n        while parent[root] != root:\n            root = parent[root]\n        curr = i\n        while parent[curr] != root:\n            # 路径压缩：直接指向根节点\n            parent[curr], curr = root, parent[curr]\n        return root\n\n    start_node = 0\n    end_node = size - 1\n    \n    # 依次加入边，直到起点和终点连通\n    for diff, u, v in edges:\n        root_u = find(u)\n        root_v = find(v)\n        \n        if root_u != root_v:\n            parent[root_u] = root_v\n            # 检查起点(0,0)和终点(n-1,m-1)是否连通\n            if find(start_node) == find(end_node):\n                print(diff)\n                return\n\nif __name__ == "__main__":\n    solve()\n'
SAMPLE_IN = '4 5\n5 3 3 7 9\n5 5 4 2 8\n9 1 1 7 10\n9 8 10 1 7\n'
def generate_case(r):
    n, m = r.randint(1, 12), r.randint(1, 12)
    rows = [[r.randint(1, 100) for _ in range(m)] for _ in range(n)]
    assert len(rows) == n and all(len(row) == m and min(row) >= 1 for row in rows)
    return f"{n} {m}\n" + "\n".join(" ".join(map(str, row)) for row in rows) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(21):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(28972 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

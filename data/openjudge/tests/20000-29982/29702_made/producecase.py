import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'import sys\nfrom collections import defaultdict, deque\n\n\ndef solve():\n    data = sys.stdin.readline().strip().split()\n    if not data:\n        return\n    m, n = map(int, data)\n\n    # 1) 读入所有 “A > B” 关系，建图\n    edges = defaultdict(list)\n    indegree = [0] * (m + 1)\n    for _ in range(n):\n        line = sys.stdin.readline().strip()\n        if not line:\n            continue\n        left_str, right_str = line.split(\'>\')\n        A = int(left_str.strip())\n        B = int(right_str.strip())\n        edges[A].append(B)\n        indegree[B] += 1\n\n    # 2) 拓扑排序：检查矛盾（环）和是否唯一\n    q = deque()\n    for u in range(1, m + 1):\n        if indegree[u] == 0:\n            q.append(u)\n\n    topo_list = []\n    multiple = False\n    while q:\n        if len(q) > 1:\n            multiple = True\n        u = q.popleft()\n        topo_list.append(u)\n        for v in edges[u]:\n            indegree[v] -= 1\n            if indegree[v] == 0:\n                q.append(v)\n\n    if len(topo_list) < m:\n        print("Device error.")\n        return\n    if multiple:\n        print("Not determined.")\n        return\n\n    # 3) 生成“位置从大到小”的序列 pos_order（前序 根→右→左）\n    pos_order = []\n\n    def dfs(u):\n        if u > m:\n            return\n        pos_order.append(u)\n        dfs(2 * u + 1)\n        dfs(2 * u)\n\n    dfs(1)\n\n    # 4) 给这些位置分配流量编号（topo_list 为从大到小的编号）\n    assigned = [0] * (m + 1)\n    for i in range(m):\n        assigned[pos_order[i]] = topo_list[i]\n\n    # 5) 使用递归方式中序遍历 assigned[]\n    res = []\n\n    def inorder(u):\n        if u > m:\n            return\n        inorder(2 * u)\n        res.append(str(assigned[u]))\n        inorder(2 * u + 1)\n\n    inorder(1)\n    print(" ".join(res))\n\n\nif __name__ == "__main__":\n    solve()\n'
SAMPLE_IN = '3 3\n1 > 2\n2 > 3\n1 > 3\n'
def generate_case(r):
    m = r.choice([2, 3, 3, 5, 7, 7, 10, 15, r.randint(2, 15)])
    order = list(range(1, m + 1)); r.shuffle(order)
    chain = [(order[i], order[i + 1]) for i in range(m - 1)]
    kind = r.random()
    if kind < .38:                                     # 唯一全序 -> 中序遍历
        edges = list(chain)
        for _ in range(r.randint(0, m)):               # 冗余传递边，不破坏唯一性
            i = r.randrange(m); j = r.randrange(m)
            if i < j: edges.append((order[i], order[j]))
    elif kind < .69:                                   # 成环 -> Device error.
        edges = list(chain) + [(order[-1], order[0])]
    else:                                              # 缺一条关系 -> Not determined.
        edges = [e for k, e in enumerate(chain) if k != r.randrange(len(chain))] if chain else []
    r.shuffle(edges)
    body = "".join(f"{a} > {b}\n" for a, b in edges)
    return f"{m} {len(edges)}\n" + body

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(21):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(29702 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

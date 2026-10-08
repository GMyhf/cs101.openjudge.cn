import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'import sys\nfrom collections import defaultdict, deque\n\ndef min_bonus(n, m, matches):\n    # 图结构：记录谁打败了谁（反向边）\n    graph = defaultdict(list)\n    indegree = [0] * n\n    \n    for a, b in matches:\n        graph[b].append(a)  # a > b，所以 b 是 a 的前驱\n        indegree[a] += 1\n\n    # 初始化奖金为 100\n    bonus = [100] * n\n\n    # 拓扑排序队列\n    queue = deque([i for i in range(n) if indegree[i] == 0])\n\n    while queue:\n        curr = queue.popleft()\n        for neighbor in graph[curr]:\n            # 如果邻居的奖金不大于当前的，就调整它\n            if bonus[neighbor] <= bonus[curr]:\n                bonus[neighbor] = bonus[curr] + 1\n            indegree[neighbor] -= 1\n            if indegree[neighbor] == 0:\n                queue.append(neighbor)\n\n    return sum(bonus)\n\n# 读取输入\nif __name__ == "__main__":\n    input = sys.stdin.read\n    data = input().split()\n    \n    n = int(data[0])\n    m = int(data[1])\n    \n    matches = []\n    idx = 2\n    for _ in range(m):\n        a = int(data[idx])\n        b = int(data[idx+1])\n        matches.append((a, b))\n        idx += 2\n\n    result = min_bonus(n, m, matches)\n    print(result)\n'
SAMPLE_IN = '5 6\n1 0\n2 0\n3 0\n4 1\n4 2\n4 3\n'
SAMPLE_OUT = '505\n'
def generate_case(r):
    n = r.randint(2, 20); edges = [(i, j) for i in range(n) for j in range(i) if r.random() < .18]
    assert len(edges) == len(set(edges)) and all(0 <= b < a < n for a, b in edges)
    return f"{n} {len(edges)}\n" + "\n".join(f"{a} {b}" for a, b in edges) + ("\n" if edges else "")

def valid(text):
    """题面：第一行 n（1≤n≤1000）和 m（0≤m≤2000）；接下来 m 行 a b（编号 0..n-1），a 打败 b。
    保证胜负关系不形成有向环（自环 a==b 也算环）。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    def ints(line):
        parts = line.split(" ")
        if not all(t.isdigit() and t == str(int(t)) for t in parts):
            return None
        return list(map(int, parts))
    head = ints(lines[0])
    if head is None or len(head) != 2:
        return False
    n, m = head
    if not (1 <= n <= 1000 and 0 <= m <= 2000) or len(lines) != m + 1:
        return False
    adj = [[] for _ in range(n)]; indeg = [0] * n
    for line in lines[1:]:
        e = ints(line)
        if e is None or len(e) != 2 or not all(0 <= x < n for x in e) or e[0] == e[1]:
            return False
        adj[e[0]].append(e[1]); indeg[e[1]] += 1
    q = [i for i in range(n) if indeg[i] == 0]; seen = 0
    while q:
        u = q.pop(); seen += 1
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0: q.append(v)
    return seen == n


def dag_case(r, n, m, kind):
    """在随机拓扑序上造 DAG，再把编号随机打乱（不再总是大号打败小号）。"""
    order = list(range(n)); r.shuffle(order)
    edges = []
    if kind == "chain":            # 一条长链：order[i+1] 打败 order[i]
        edges = [(i + 1, i) for i in range(n - 1)]
        pool = set(edges)
        while len(edges) < m:
            i, j = sorted(r.sample(range(n), 2))
            if (j, i) not in pool: pool.add((j, i)); edges.append((j, i))
    elif kind == "dup":            # 允许同一对队伍多次 PK（同方向）
        for _ in range(m):
            i, j = sorted(r.sample(range(n), 2)); edges.append((j, i))
    elif kind == "layered":        # 分层：只有相邻层之间有边，最长路与 BFS 层数不同的写法会被卡
        pool = set()
        while len(edges) < m:
            i = r.randrange(n - 1); j = min(n - 1, i + r.choice([1, 1, 2, 5, 50]))
            if (j, i) not in pool: pool.add((j, i)); edges.append((j, i))
    else:                          # 随机 DAG，无重边
        pool = set()
        while len(edges) < m:
            i, j = sorted(r.sample(range(n), 2))
            if (j, i) not in pool: pool.add((j, i)); edges.append((j, i))
    r.shuffle(edges)
    lines = [f"{order[a]} {order[b]}" for a, b in edges]
    return f"{n} {m}\n" + "".join(x + "\n" for x in lines)


EXTRA = [(1, 0, "rand"), (1000, 0, "rand"), (2, 1, "rand"), (1000, 999, "chain"), (1000, 2000, "chain"),
         (1000, 2000, "rand"), (1000, 2000, "layered"), (1000, 2000, "dup"), (100, 2000, "rand"),
         (64, 2000, "rand"), (500, 1500, "layered"), (1000, 1200, "rand")]


def main():
    assert SAMPLE_IN == '5 6\n1 0\n2 0\n3 0\n4 1\n4 2\n4 3\n'
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        cases = []
        for index in range(20):
            if index == 0:
                content = SAMPLE_IN
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(22508 + index + attempt * 1000))
                    if content not in seen: break
                else: raise AssertionError('insufficient diversity')
            seen.append(content)
            cases.append(content)
        for k, (n, m, kind) in enumerate(EXTRA):
            content = dag_case(random.Random(22508 * 100 + k), n, m, kind)
            assert content not in cases, k
            cases.append(content)
        for index, content in enumerate(cases):
            assert valid(content), index
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()

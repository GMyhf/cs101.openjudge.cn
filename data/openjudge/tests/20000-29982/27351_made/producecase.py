import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'from collections import deque\n\nn, m = map(int, input().split())\ngraph1 = [set() for _ in range(n+1)]\nfor _ in range(m):\n    a, b = map(int, input().split())\n    graph1[a].add(b)\n    graph1[b].add(a)\n\nunvisited = set(range(1, n+1))\ncomponents = 0\n\nwhile unvisited:\n    start = unvisited.pop()\n    components += 1\n    queue = deque([start])\n    while queue:\n        u = queue.popleft()\n        good = unvisited - graph1[u]  # 所有未访问且与 u 有 0-边的点\n        for v in good:\n            queue.append(v)\n        unvisited -= good\n\nprint(components - 1)\n'
SAMPLE_IN = '6 11\n1 3\n1 4\n1 5\n1 6\n2 3\n2 4\n2 5\n2 6\n3 4\n3 5\n3 6\n===========\n3 0\n'
def generate_case(r):
    n = r.randint(2, 12); all_edges = [(i, j) for i in range(1, n + 1) for j in range(i + 1, n + 1)]
    r.shuffle(all_edges); m = r.randint(0, min(30, len(all_edges))); edges = sorted(all_edges[:m])
    assert len(edges) == len(set(edges)) and all(1 <= a < b <= n for a, b in edges)
    return f"{n} {m}\n" + "\n".join(f"{a} {b}" for a, b in edges) + ("\n" if edges else "")

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(21):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(27351 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

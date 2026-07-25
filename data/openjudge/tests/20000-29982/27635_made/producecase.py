import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = '#王昊 光华管理学院\nn, m = list(map(int, input().split()))\nedge = [[]for _ in range(n)]\nfor _ in range(m):\n    a, b = list(map(int, input().split()))\n    edge[a].append(b)\n    edge[b].append(a)\ncnt, flag = set(), False\n\n\ndef dfs(x, y):\n    global cnt, flag\n    cnt.add(x)\n    for i in edge[x]:\n        if i not in cnt:\n            dfs(i, x)\n        elif y != i:\n            flag = True\n\n\nfor i in range(n):\n    cnt.clear()\n    dfs(i, -1)\n    if len(cnt) == n:\n        break\n    if flag:\n        break\n\nprint("connected:"+("yes" if len(cnt) == n else "no"))\nprint("loop:"+("yes" if flag else \'no\'))\n'
SAMPLE_IN = '3 2\n0 1\n0 2\n'
SAMPLE_OUT = 'connected:yes\nloop:no\n'
def generate_case(r):
    n = r.randint(2, 25); edges = [(i, i + 1) for i in range(n - 1)]
    if r.random() < .35: edges.append((0, 1))
    if r.random() < .35: edges = edges[:max(1, n // 3)]
    assert all(0 <= u < n and 0 <= v < n and u != v for u, v in edges)
    return f"{n} {len(edges)}\n" + "\n".join(f"{u} {v}" for u, v in edges) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(27635 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

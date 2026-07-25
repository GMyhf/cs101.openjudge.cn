import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = "n, m = map(int, input().split())\nparent=[i for i in range(n)]\nedges=[]\ndiff=[]\nfor _ in range(m):\n    a, b, c = map(int, input().split())\n    if c!=1:\n        edges.append((a, b))\n    else:\n        diff.append((a, b))\n\ndef find(x):\n    if parent[x] != x:\n        parent[x] = find(parent[x])\n    return parent[x]\ndef union(x, y):\n    nx, ny = find(x), find(y)\n    if nx != ny:\n        parent[ny] = nx\n        #return True\n    #return False\n\nfor a, b in edges:\n    union(a, b)\n\nfor a, b in diff:\n    if find(a) == find(b):\n        print('NO')\n        exit()\nprint('YES')\n"
SAMPLE_IN = '3 3\n0 1 0\n1 2 1\n0 2 1\n'
def generate_case(r):
    n = r.randint(3, 15); labels = [r.randrange(2) for _ in range(n)]; edges = []
    for _ in range(r.randint(2, min(20, n * (n - 1) // 2))):
        a, b = r.sample(range(n), 2); edges.append((a, b, labels[a] ^ labels[b]))
    if r.random() < .5:
        a, b = r.sample(range(n), 2); edges.append((a, b, 1 - (labels[a] ^ labels[b])))
    assert all(0 <= a < n and 0 <= b < n and c in (0, 1) for a, b, c in edges)
    return f"{n} {len(edges)}\n" + "\n".join(f"{a} {b} {c}" for a, b, c in edges) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(21):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(27306 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

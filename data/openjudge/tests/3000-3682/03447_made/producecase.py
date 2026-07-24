import random
import subprocess
import tempfile
from pathlib import Path
SAMPLE_IN = '5\nE 0.01 *A\nD 0.01 A*\nC 0.01 *A\nA 1.00 EDCB\nB 0.01 A*\n'
SAMPLE_OUT = 'A\n'
CASES = ['5\nE 0.01 *A\nD 0.01 A*\nC 0.01 *A\nA 1.00 EDCB\nB 0.01 A*\n', '5\nE 0.01 *A\nD 0.01 A*\nC 0.01 *A\nA 1.00 EDCB\nB 0.01 A*\n', '5\nE 0.01 *A\nD 0.01 A*\nC 0.01 *A\nA 1.00 EDCB\nB 0.01 A*\n', '5\nE 0.01 *A\nD 0.01 A*\nC 0.01 *A\nA 1.00 EDCB\nB 0.01 A*\n', '5\nE 0.01 *A\nD 0.01 A*\nC 0.01 *A\nA 1.00 EDCB\nB 0.01 A*\n', '5\nE 0.01 *A\nD 0.01 A*\nC 0.01 *A\nA 1.00 EDCB\nB 0.01 A*\n', '5\nE 0.01 *A\nD 0.01 A*\nC 0.01 *A\nA 1.00 EDCB\nB 0.01 A*\n', '5\nE 0.01 *A\nD 0.01 A*\nC 0.01 *A\nA 1.00 EDCB\nB 0.01 A*\n', '5\nE 0.01 *A\nD 0.01 A*\nC 0.01 *A\nA 1.00 EDCB\nB 0.01 A*\n', '5\nE 0.01 *A\nD 0.01 A*\nC 0.01 *A\nA 1.00 EDCB\nB 0.01 A*\n', '5\nE 0.01 *A\nD 0.01 A*\nC 0.01 *A\nA 1.00 EDCB\nB 0.01 A*\n', '5\nE 0.01 *A\nD 0.01 A*\nC 0.01 *A\nA 1.00 EDCB\nB 0.01 A*\n', '5\nE 0.01 *A\nD 0.01 A*\nC 0.01 *A\nA 1.00 EDCB\nB 0.01 A*\n', '5\nE 0.01 *A\nD 0.01 A*\nC 0.01 *A\nA 1.00 EDCB\nB 0.01 A*\n', '5\nE 0.01 *A\nD 0.01 A*\nC 0.01 *A\nA 1.00 EDCB\nB 0.01 A*\n', '5\nE 0.01 *A\nD 0.01 A*\nC 0.01 *A\nA 1.00 EDCB\nB 0.01 A*\n', '5\nE 0.01 *A\nD 0.01 A*\nC 0.01 *A\nA 1.00 EDCB\nB 0.01 A*\n', '5\nE 0.01 *A\nD 0.01 A*\nC 0.01 *A\nA 1.00 EDCB\nB 0.01 A*\n', '5\nE 0.01 *A\nD 0.01 A*\nC 0.01 *A\nA 1.00 EDCB\nB 0.01 A*\n', '5\nE 0.01 *A\nD 0.01 A*\nC 0.01 *A\nA 1.00 EDCB\nB 0.01 A*\n']
REFERENCE_SOURCE = '# 肖添天\nfrom collections import defaultdict, deque\n\nn = int(input())\ngraph = defaultdict(set)\nto_earth = set()\nprice = {}\nfor i in range(n):\n    a, b, c = input().split()\n    b = float(b)\n    price[a] = b if a not in price else max(price[a], b)\n    for x in c:\n        if x == "*":\n            to_earth.add(a)\n        else:\n            graph[a].add(x)\n            graph[x].add(a)\n\ndef bfs(start):\n    Q = deque([start])\n    visited = set()\n    visited.add(start)\n    cnt = 0\n    while Q:\n        l = len(Q)\n        for _ in range(l):\n            f = Q.popleft()\n            if f in to_earth:\n                return price[start] * (0.95 ** cnt)\n            for x in graph[f]:\n                if x not in visited:\n                    Q.append(x)\n                    visited.add(x)\n        cnt += 1\n    return 0\n\n\nans = []\nfor planet in price.keys():\n    ans.append((bfs(planet), planet))\n\nans.sort(key=lambda x: [-x[0], x[1]])\nprint(ans[0][1])\n'
assert SAMPLE_IN.strip()
assert SAMPLE_OUT.strip()
random.seed(3447)
assert CASES[0] == SAMPLE_IN
def solve_reference(content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE)
        handle.flush()
        result = subprocess.run(["python3", handle.name], input=content, text=True,
                                capture_output=True, timeout=5, check=True)
    return result.stdout
assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split()
def generate_case(index):
    return CASES[index]
root = Path(__file__).parent / "data"
for index in range(20):
    content = generate_case(index)
    (root / f"{index}.in").write_text(content, encoding="utf-8")
    (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")

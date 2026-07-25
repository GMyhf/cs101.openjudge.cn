"""3447 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001a
生成器与循环取自 scripts/build_001a.py（批次 001a），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 3447
SAMPLE_IN = '5\nE 0.01 *A\nD 0.01 A*\nC 0.01 *A\nA 1.00 EDCB\nB 0.01 A*\n'
SAMPLE_OUT = 'A\n'
REFERENCE_SOURCE = '# 肖添天\nfrom collections import defaultdict, deque\n\nn = int(input())\ngraph = defaultdict(set)\nto_earth = set()\nprice = {}\nfor i in range(n):\n    a, b, c = input().split()\n    b = float(b)\n    price[a] = b if a not in price else max(price[a], b)\n    for x in c:\n        if x == "*":\n            to_earth.add(a)\n        else:\n            graph[a].add(x)\n            graph[x].add(a)\n\ndef bfs(start):\n    Q = deque([start])\n    visited = set()\n    visited.add(start)\n    cnt = 0\n    while Q:\n        l = len(Q)\n        for _ in range(l):\n            f = Q.popleft()\n            if f in to_earth:\n                return price[start] * (0.95 ** cnt)\n            for x in graph[f]:\n                if x not in visited:\n                    Q.append(x)\n                    visited.add(x)\n        cnt += 1\n    return 0\n\n\nans = []\nfor planet in price.keys():\n    ans.append((bfs(planet), planet))\n\nans.sort(key=lambda x: [-x[0], x[1]])\nprint(ans[0][1])\n'

def sample(body, label):
    fence = r"\x60\x60\x60"
    pattern = rf"(?:{label})\s*\n+{fence}\n(.*?){fence}"
    values = re.findall(pattern, body, re.S | re.I)
    if not values: raise ValueError("missing " + label)
    return values[0].strip() + "\n"

def g3447(r):
    n = r.randint(4, 26)
    planets = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:n])
    edges = set()
    for node in planets[1:]:
        other = r.choice(planets[:planets.index(node)])
        edges.add(tuple(sorted((node, other))))
    for a in planets:
        for b in planets:
            if a < b and (a, b) not in edges and r.random() < 0.18:
                edges.add((a, b))
    routes = {node: set() for node in planets}
    for a, b in edges:
        routes[a].add(b)
        routes[b].add(a)
    earth = r.sample(planets, r.randint(1, min(3, n)))
    lines = []
    for node in r.sample(planets, n):
        value = r.randint(1, 1000) / 100
        route = sorted(routes[node])
        if node in earth:
            route.append("*")
        lines.append(f"{node} {value:.2f} {''.join(route)}")
    return str(n) + "\n" + "\n".join(lines) + "\n"

def build_cases():
    return [SAMPLE_IN] + [g3447(random.Random(NUMBER + i)) for i in range(1, 20)]

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

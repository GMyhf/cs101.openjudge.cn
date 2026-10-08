"""3447 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的数据（0..19 为原批次，20 起为边界/平局/不连通组）。

出处：build_001a
生成器与循环取自 scripts/build_001a.py（批次 001a），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import re
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

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LINE_RE = re.compile(r"([A-Z]) (\d\.\d\d) ([A-Z*]+)")


def valid(text):
    """题面契约：若干银河；每个银河首行 n（1..26），随后 n 行「字母 空格 d.dd 空格 由字母/*组成的串」。
    行星字母在银河内互异；价值为不超过 10 的正实数；每个银河至少一个行星带 *。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    i = 0
    if not lines or lines == [""]:
        return False
    while i < len(lines):
        if not re.fullmatch(r"\d+", lines[i]):
            return False
        n = int(lines[i])
        if not 1 <= n <= 26 or i + 1 + n > len(lines):
            return False
        seen, star = set(), False
        for line in lines[i + 1:i + 1 + n]:
            m = LINE_RE.fullmatch(line)
            if not m or m.group(1) in seen:
                return False
            seen.add(m.group(1))
            if not 0 < float(m.group(2)) <= 10:
                return False
            star = star or "*" in m.group(3)
        if not star:
            return False
        i += 1 + n
    return True


def exact_answer(content):
    """精确 oracle：价值按分为整数、通行费按 95/100 有理数比较，与浮点参考解互证。"""
    from fractions import Fraction
    from collections import deque
    lines = content.split("\n")
    n = int(lines[0])
    price, graph, earth = {}, {}, set()
    for line in lines[1:1 + n]:
        a, v, s = line.split()
        price[a] = Fraction(int(v.replace(".", "")), 100)
        for x in s:
            if x == "*":
                earth.add(a)
            else:
                graph.setdefault(a, set()).add(x)
                graph.setdefault(x, set()).add(a)
    dist = {e: 0 for e in earth}
    q = deque(earth)
    while q:
        u = q.popleft()
        for w in graph.get(u, ()):
            if w not in dist:
                dist[w] = dist[u] + 1
                q.append(w)
    best = max(price[a] * Fraction(95, 100) ** dist[a] if a in dist else 0 for a in price)
    return min(a for a in price if a in dist and price[a] * Fraction(95, 100) ** dist[a] == best)


def galaxy(rows):
    return str(len(rows)) + "\n" + "\n".join(rows) + "\n"


def chain26():
    """26 个行星连成链，只有 A 通地球，Z 价值最高但折损 0.95^25；Y 略低于 Z 的折后值以外的值。"""
    rows = []
    for i, c in enumerate(LETTERS):
        nb = ([LETTERS[i - 1]] if i else []) + ([LETTERS[i + 1]] if i < 25 else [])
        rows.append(f"{c} {'9.99' if c == 'Z' else '0.27'} {''.join(nb)}{'*' if c == 'A' else ''}")
    return galaxy(rows)


def extra_cases(r):
    cases = []
    cases.append(galaxy(["Q 3.14 *"]))                                   # n=1
    cases.append(galaxy(["B 1.90 *", "A 2.00 B"]))                       # 精确相等：2.00*0.95=1.90，取字母序小的 A
    cases.append(galaxy(["A 1.90 *", "B 2.00 A"]))                       # 相等，取 A（不能取后读入/折后的）
    cases.append(galaxy(["C 5.00 *D", "D 5.00 C*", "B 5.00 *"]))         # 三者同值都直连，取 B
    cases.append(galaxy(["Z 0.01 *", "A 9.99 B", "B 9.98 A"]))           # A、B 不连通地球，价值视为 0，答案 Z
    cases.append(galaxy(["M 1.00 N", "N 1.00 MO", "O 1.00 NP", "P 1.00 O*", "X 1.05 P"]))  # 中转数=路径上中间站数
    cases.append(chain26())                                              # 最长路径 25 次中转
    # n=26 的稠密图，全部行星都带 *：答案就是最大价值中字母序最小者
    rows = []
    vals = [r.randint(1, 999) for _ in range(26)]
    vals[r.randrange(26)] = vals[r.randrange(26)] = 999
    for c, v in zip(LETTERS, vals):
        nb = "".join(x for x in LETTERS if x != c and r.random() < 0.5) or ("A" if c != "A" else "B")
        rows.append(f"{c} {v / 100:.2f} *{nb}")
    r.shuffle(rows)
    cases.append(galaxy(rows))
    # n=26，两个连通块：价值最高的块里没有 *；另一块 BFS 层数较深
    rows = []
    left, right = LETTERS[:13], LETTERS[13:]
    for k, c in enumerate(left):
        nb = (left[k - 1] if k else "") + (left[k + 1] if k < 12 else "")
        rows.append(f"{c} 9.{r.randint(50, 99)} {nb}")
    for k, c in enumerate(right):
        nb = (right[k - 1] if k else "") + (right[k + 1] if k < 12 else "")
        rows.append(f"{c} {r.randint(100, 900) / 100:.2f} {nb}{'*' if k == 6 else ''}")
    r.shuffle(rows)
    cases.append(galaxy(rows))
    # 只单向列出航线（另一端的串里不写回来），对称性要靠程序自己补
    rows = ["A 0.50 *", "B 0.60 A", "C 0.70 B", "D 0.80 C", "E 1.00 D"]
    cases.append(galaxy(rows))
    for _ in range(4):
        cases.append(g3447(r))
    return cases


def build_cases():
    return ([SAMPLE_IN] + [g3447(random.Random(NUMBER + i)) for i in range(1, 20)]
            + extra_cases(random.Random(NUMBER * 1000 + 1)))

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
        out = solve_reference(content)
        assert valid(content), index
        assert out.strip() == exact_answer(content), (index, out)
        (root / f"{index}.out").write_text(out, encoding="utf-8")


if __name__ == "__main__":
    main()

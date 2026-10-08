import random, re, subprocess, tempfile
from pathlib import Path
# 原参考解只检查“相同”连通块内有无“不同”结论，漏判由“不同”组成的奇环（如三株两两不同），已改为带权并查集。
REFERENCE_SOURCE = "import sys\nsys.setrecursionlimit(10000)\ndata = sys.stdin.read().split()\nn, m = int(data[0]), int(data[1])\nparent = list(range(n))\nrel = [0] * n  # rel[x]: x 与 parent[x] 是否不同种类\n\n\ndef find(x):\n    if parent[x] == x:\n        return x\n    root = find(parent[x])\n    rel[x] ^= rel[parent[x]]\n    parent[x] = root\n    return root\n\n\nok = True\nfor k in range(m):\n    a, b, c = int(data[2 + 3 * k]), int(data[3 + 3 * k]), int(data[4 + 3 * k])\n    ra, rb = find(a), find(b)\n    if ra == rb:\n        if rel[a] ^ rel[b] != c:\n            ok = False\n            break\n    else:\n        parent[rb] = ra\n        rel[rb] = rel[a] ^ rel[b] ^ c\nprint('YES' if ok else 'NO')\n"
SAMPLE_IN = '3 3\n0 1 0\n1 2 1\n0 2 1\n'
def valid(text):
    """题面：第一行 n m（n<=100，m<=10000）；接下来 m 行 a b c，0<=a,b<=n-1，c∈{0,1}。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    head = lines[0].split(" ")
    if len(head) != 2 or not all(re.fullmatch(r"0|[1-9][0-9]*", x) for x in head):
        return False
    n, m = map(int, head)
    if not (1 <= n <= 100 and 0 <= m <= 10000) or len(lines) != m + 1:
        return False
    for line in lines[1:]:
        parts = line.split(" ")
        if len(parts) != 3 or not all(re.fullmatch(r"0|[1-9][0-9]*", x) for x in parts):
            return False
        a, b, c = map(int, parts)
        if not (0 <= a < n and 0 <= b < n and c in (0, 1)):
            return False
    return True


def _fmt(n, edges):
    return f"{n} {len(edges)}\n" + "\n".join(f"{a} {b} {c}" for a, b, c in edges) + "\n"


def _consistent(r, n, m, labels):
    edges = []
    for _ in range(m):
        a, b = r.sample(range(n), 2); edges.append((a, b, labels[a] ^ labels[b]))
    return edges


def generate_case(r, index):
    if index == 1:
        return "3 3\n0 1 0\n1 2 1\n0 2 0\n"
    if index == 2:
        return "3 3\n0 1 1\n1 2 1\n0 2 1\n"  # “不同”构成奇环：NO
    if index == 3:
        return "4 4\n0 1 1\n1 2 1\n2 3 1\n3 0 1\n"  # 偶环：YES
    if index == 4:
        return "2 1\n0 1 1\n"
    if index == 5:
        return "1 0\n"
    if index <= 14:
        # 小规模随机，一半插入一条矛盾结论
        n = r.randint(3, 15); labels = [r.randrange(2) for _ in range(n)]
        edges = _consistent(r, n, r.randint(2, min(20, n * (n - 1) // 2)), labels)
        if index % 2:
            # 经由 x 把 a、b 连通后再给出矛盾结论
            a, b, x = r.sample(range(n), 3)
            extra = [(a, x, labels[a] ^ labels[x]), (x, b, labels[x] ^ labels[b]), (a, b, 1 - (labels[a] ^ labels[b]))]
            for e in extra:
                edges.insert(r.randint(0, len(edges)), e)
        return _fmt(n, edges)
    if index <= 20:
        # 纯“不同”结论构成的长环：奇环 NO / 偶环 YES，打乱顺序
        n = r.randint(50, 100)
        k = n if index % 2 else n - 1
        k -= (k % 2) if index % 2 else (1 - k % 2)  # 奇数 index 偶环，偶数 index 奇环
        perm = r.sample(range(n), k)
        edges = [(perm[i], perm[(i + 1) % k], 1) for i in range(k)]
        r.shuffle(edges)
        return _fmt(n, edges)
    if index <= 26:
        n = r.randint(30, 100); labels = [r.randrange(2) for _ in range(n)]
        edges = _consistent(r, n, r.randint(100, 3000), labels)
        if index % 2:
            # 矛盾放在最后，且只靠“不同”边闭合出的奇环才能发现
            a, b = r.sample(range(n), 2); edges.append((a, b, 1 - (labels[a] ^ labels[b])))
        return _fmt(n, edges)
    # 满规模 n=100，m=10000
    n = 100; labels = [r.randrange(2) for _ in range(n)]
    if index >= 34:
        # 全是“不同”结论（二分图），矛盾也是“不同”：卡只用并查集合并“相同”的写法
        labels = [i % 2 for i in range(n)]; r.shuffle(labels)
        side = [[i for i in range(n) if labels[i] == t] for t in (0, 1)]
        edges = []
        for _ in range(10000):
            a, b = r.choice(side[0]), r.choice(side[1])
            edges.append((a, b, 1) if r.random() < .5 else (b, a, 1))
        if index % 2 == 0:
            t = r.randrange(2); a, b = r.sample(side[t], 2)
            edges[r.randrange(5000, 10000)] = (a, b, 1)
        return _fmt(n, edges)
    edges = _consistent(r, n, 10000, labels)
    if index % 2 == 0:
        a, b = r.sample(range(n), 2)
        edges[r.randrange(5000, 10000)] = (a, b, 1 - (labels[a] ^ labels[b]))
    return _fmt(n, edges)


def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        for index in range(40):
            if index == 0: content = SAMPLE_IN
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(27306 + index + attempt * 1000), index)
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
            assert valid(content)
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()

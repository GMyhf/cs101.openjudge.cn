import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = "def main():\n    # Read the input\n    n, w = map(int, input().split())\n    P, Q = map(int, input().split())\n    # The amplified skill damage\n    damage = P + Q\n\n    monsters = []\n    for i in range(n):\n        x, y = map(int, input().split())\n        if damage >= x:\n            monsters.append(y)\n\n    # Sort monsters by the magic cost (y) in ascending order\n    monsters.sort()\n\n    # Count how many monsters we can defeat\n    count = 0\n    for cost in monsters:\n        if w >= cost:\n            w -= cost\n            count += 1\n        else:\n            break\n\n    print(count)\n\n\nif __name__ == '__main__':\n    main()\n\n"
SAMPLE_IN = '10 13\n108 76\n33 6\n36 18\n102 19\n98 5\n114 11\n0 5\n39 12\n108 6\n99 0\n34 4\n'
SAMPLE_OUT = '3\n'
def generate_case(r):
    n = r.randint(2, 30); w = r.randint(0, 100); p, q = r.randint(0, 200), r.randint(0, 200)
    monsters = [(r.randint(0, 1000), r.randint(0, 70)) for _ in range(n)]
    assert n >= 1 and w >= 0 and p >= 0 and q >= 0 and all(x >= 0 and y >= 0 for x, y in monsters)
    return f"{n} {w}\n{p} {q}\n" + "\n".join(f"{x} {y}" for x, y in monsters) + "\n"

def valid(text):
    """题面：第一行 n w；第二行 P Q；接下来 n 行 xi yi。
    0<=n,w<=5000，0<=P,Q<=200，0<=x<=1000，0<=y<=70。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")

    def ints(line, k):
        toks = line.split(" ")
        if len(toks) != k or any(not t.isdigit() or (len(t) > 1 and t[0] == "0") for t in toks):
            return None
        return list(map(int, toks))

    if len(lines) < 2:
        return False
    a = ints(lines[0], 2); b = ints(lines[1], 2)
    if a is None or b is None:
        return False
    n, w = a; p, q = b
    if not (0 <= n <= 5000 and 0 <= w <= 5000 and 0 <= p <= 200 and 0 <= q <= 200):
        return False
    if len(lines) != n + 2:
        return False
    for line in lines[2:]:
        xy = ints(line, 2)
        if xy is None or not (0 <= xy[0] <= 1000 and 0 <= xy[1] <= 70):
            return False
    return True

def fmt(n, w, p, q, monsters):
    assert len(monsters) == n
    return f"{n} {w}\n{p} {q}\n" + "".join(f"{x} {y}\n" for x, y in monsters)

def extra_case(k):
    """追加组：边界与满规模。"""
    r = random.Random(215350 + k)
    if k == 0:   # n=0
        return fmt(0, r.randint(0, 5000), r.randint(0, 200), r.randint(0, 200), [])
    if k == 1:   # w=0，只有 y=0 且护盾够的能打
        n = 50; p, q = 100, 50
        ms = [(r.randint(0, 300), r.choice([0, 0, r.randint(1, 70)])) for _ in range(n)]
        return fmt(n, 0, p, q, ms)
    if k == 2:   # P=Q=0，只有 x=0 的能打
        n = 40
        ms = [(r.choice([0, r.randint(1, 1000)]), r.randint(0, 70)) for _ in range(n)]
        return fmt(n, r.randint(50, 300), 0, 0, ms)
    if k == 3:   # x 恰等于 P+Q 的边界
        p, q = r.randint(0, 200), r.randint(0, 200)
        ms = [(p + q + r.choice([-1, 0, 0, 1]), r.randint(0, 70)) for _ in range(60)]
        ms = [(min(1000, max(0, x)), y) for x, y in ms]
        return fmt(60, r.randint(100, 600), p, q, ms)
    if k == 4:   # w 恰好等于若干最小 y 之和（>= 而不是 >）
        p, q = 200, 200
        ys = [r.randint(1, 70) for _ in range(30)]
        w = sum(sorted(ys)[:12])
        return fmt(30, w, p, q, [(r.randint(0, 400), y) for y in ys])
    if k == 5:   # 护盾都打不过
        p, q = r.randint(0, 100), r.randint(0, 100)
        ms = [(r.randint(p + q + 1, 1000), r.randint(0, 70)) for _ in range(100)]
        return fmt(100, 5000, p, q, ms)
    if k == 6:   # 全部可打且魔法值足够
        ms = [(r.randint(0, 400), r.randint(0, 1)) for _ in range(5000)]
        return fmt(5000, 5000, 200, 200, ms)
    if k == 7:   # 便宜的怪兽护盾高（按 x 排序或不过滤会错）
        p, q = r.randint(100, 200), r.randint(100, 200)
        d = p + q
        ms = []
        for _ in range(5000):
            if r.random() < 0.5:
                ms.append((r.randint(d + 1, 1000), r.randint(0, 10)))
            else:
                ms.append((r.randint(0, d), r.randint(5, 70)))
        r.shuffle(ms)
        return fmt(5000, r.randint(1000, 5000), p, q, ms)
    if k == 8:   # 单只怪兽，恰好够 / 差一点
        y = r.randint(1, 70)
        return fmt(1, y, 10, 10, [(20, y)])
    if k == 9:
        y = r.randint(1, 70)
        return fmt(1, y - 1, 10, 10, [(20, y)])
    if k == 10:  # 输入顺序无序的满规模（不排序直接贪心会错）
        ms = [(r.randint(0, 1000), r.randint(0, 70)) for _ in range(5000)]
        return fmt(5000, 5000, r.randint(0, 200), r.randint(0, 200), ms)
    # 其余：满规模/大规模随机
    n = r.choice([5000, r.randint(1000, 5000)])
    w = r.choice([5000, r.randint(0, 5000)])
    ms = [(r.randint(0, 1000), r.randint(0, 70)) for _ in range(n)]
    return fmt(n, w, r.randint(0, 200), r.randint(0, 200), ms)

def main():
    assert SAMPLE_IN == '10 13\n108 76\n33 6\n36 18\n102 19\n98 5\n114 11\n0 5\n39 12\n108 6\n99 0\n34 4\n'
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        for index in range(40):
            if index == 0:
                content = SAMPLE_IN
            elif index < 20:
                for attempt in range(100):
                    content = generate_case(random.Random(21535 + index + attempt * 1000))
                    if content not in seen: break
                else: raise AssertionError('insufficient diversity')
            else:
                content = extra_case(index - 20)
                assert content not in seen, index
            assert valid(content), index
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

if __name__ == "__main__":
    main()

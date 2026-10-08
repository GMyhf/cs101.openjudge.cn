"""04102 宠物小精灵之收服 测试数据生成器（固定种子，可复现）。

题面约束：0<N<1000，0<M<500，0<K<100；每只小精灵两个整数（球数、伤害），
题面未给范围，这里取 1..N+10 与 0..M+10（含收不了的）。
答案由 samplecode.py 给出，并用另一种 DP（按收服个数与伤害求最少球数）逐组核对。
"""
import random
import subprocess
import sys
from pathlib import Path

SEED = 4102
SAMPLES = [
    ("10 100 5\n7 10\n2 40\n2 50\n1 20\n4 20\n", "3 30\n"),
    ("10 100 5\n8 110\n12 10\n20 10\n5 200\n1 110\n", "0 100\n"),
]


def valid(text):
    """严格核输入格式与取值。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    def ints(line, cnt):
        parts = line.split(" ")
        if len(parts) != cnt or any(not p.isdigit() or (len(p) > 1 and p[0] == "0") for p in parts):
            return None
        return [int(p) for p in parts]
    head = ints(lines[0], 3)
    if head is None:
        return False
    n, m, k = head
    if not (0 < n < 1000 and 0 < m < 500 and 0 < k < 100) or len(lines) != k + 1:
        return False
    for line in lines[1:]:
        v = ints(line, 2)
        if v is None or v[0] < 1 or v[0] > 2000 or v[1] > 2000:
            return False
    return True


def fmt(n, m, items):
    return f"{n} {m} {len(items)}\n" + "".join(f"{a} {b}\n" for a, b in items)


def check(text):
    """另一种 DP：best[c][d] = 收服 c 只、总伤害 d 时最少用球数。"""
    v = list(map(int, text.split()))
    n, m, k = v[:3]
    items = [(v[3 + 2 * i], v[4 + 2 * i]) for i in range(k)]
    inf = 10 ** 9
    best = [[inf] * m for _ in range(k + 1)]
    best[0][0] = 0
    for t, (a, b) in enumerate(items):
        if a > n or b >= m:
            continue
        for c in range(t, -1, -1):
            row, nxt = best[c], best[c + 1]
            for d in range(m - 1 - b, -1, -1):
                if row[d] + a < nxt[d + b]:
                    nxt[d + b] = row[d] + a
    for c in range(k, -1, -1):
        for d in range(m):
            if best[c][d] <= n:
                return f"{c} {m - d}\n"


def rand_items(r, n, m, k, ball_hi, dmg_hi, hard=0.1, zero_dmg=False):
    items = []
    for _ in range(k):
        if r.random() < hard:
            items.append((r.randint(max(1, n // 2), n + 10), r.randint(m // 2, m + 10)))
        else:
            items.append((r.randint(1, max(1, ball_hi)), r.randint(0 if zero_dmg else 1, max(1, dmg_hi))))
    return items


def build():
    r = random.Random(SEED)
    cases = [s for s, _ in SAMPLES]
    # 最小规模与边界
    cases.append("1 1 1\n1 0\n")                 # 0 伤害可收服 -> 1 1
    cases.append("1 1 1\n1 1\n")                 # 伤害等于体力，不能收 -> 0 1
    cases.append("1 2 1\n2 1\n")                 # 球不够 -> 0 2
    cases.append(fmt(10, 10, [(1, 5), (1, 5)]))  # 伤害和恰为 M 不允许 -> 1 5
    cases.append(fmt(10, 10, [(5, 1), (5, 1), (6, 1)]))  # 球恰好用完可以 -> 2 8
    cases.append(fmt(10, 100, [(1, 60), (4, 10), (5, 10), (6, 1)]))  # 球恰好用完收 3 只 -> 3 20
    cases.append(fmt(20, 50, [(3, 10), (3, 20), (4, 5), (2, 30), (8, 9), (8, 3)]))  # 同数量取最小伤害
    cases.append(fmt(999, 499, [(1000, 1)] * 50 + [(1, 499)] * 49))  # 全都收不了 -> 0 499
    cases.append(fmt(500, 300, [(5, 3)] * 99))  # 全部能收 -> 99 3
    # 小规模随机
    for _ in range(4):
        n, m, k = r.randint(5, 50), r.randint(10, 100), r.randint(1, 10)
        cases.append(fmt(n, m, rand_items(r, n, m, k, n // 2, m // 2, zero_dmg=True)))
    # 中等规模随机
    for _ in range(5):
        n, m, k = r.randint(100, 999), r.randint(100, 499), r.randint(50, 99)
        cases.append(fmt(n, m, rand_items(r, n, m, k, n // 2, m // 2)))
    # 满规模：N、M、K 都取上限
    cases.append(fmt(999, 499, rand_items(r, 999, 499, 99, 499, 249)))
    cases.append(fmt(600, 400, rand_items(r, 600, 400, 99, 60, 30, hard=0.0)))   # 便宜的多，答案很大
    cases.append(fmt(999, 499, rand_items(r, 999, 499, 99, 999, 499, hard=0.0)))
    for _ in range(2):
        n, m = r.randint(900, 999), r.randint(450, 499)
        cases.append(fmt(n, m, rand_items(r, n, m, 99, n // 2, m // 2)))
    return cases


def main():
    cases = build()
    assert len(set(cases)) == len(cases)
    out = Path("data")
    out.mkdir(exist_ok=True)
    for p in out.glob("*"):
        p.unlink()
    for i, text in enumerate(cases):
        assert valid(text), i
        res = subprocess.run([sys.executable, "-I", "samplecode.py"], input=text, text=True,
                             capture_output=True, timeout=60, check=True).stdout.rstrip() + "\n"
        assert res == check(text), (i, res, check(text))
        if i < len(SAMPLES):
            assert res == SAMPLES[i][1], i
        (out / f"{i}.in").write_text(text)
        (out / f"{i}.out").write_text(res)


if __name__ == "__main__":
    main()

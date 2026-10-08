"""28307 老鼠和奶酪 测试数据生成器。

题面：第一行 n（1 <= n <= 10000）；第二、三行各 n 个整数 reward1、reward2，取值 1..1000；
第四行 k（0 <= k <= n）。第 0 组为样例。
"""
import random
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SEED = 28307


def valid(text):
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if len(lines) != 4:
        return False
    num = re.compile(r"[1-9][0-9]*|0")
    if not num.fullmatch(lines[0]) or not num.fullmatch(lines[3]):
        return False
    n, k = int(lines[0]), int(lines[3])
    if not (1 <= n <= 10000 and 0 <= k <= n):
        return False
    for row in lines[1:3]:
        parts = row.split(" ")
        if len(parts) != n or not all(num.fullmatch(p) and 1 <= int(p) <= 1000 for p in parts):
            return False
    return True


def fmt(a, b, k):
    return f"{len(a)}\n{' '.join(map(str, a))}\n{' '.join(map(str, b))}\n{k}\n"


def build_cases():
    r = random.Random(SEED)
    R = lambda n, lo=1, hi=1000: [r.randint(lo, hi) for _ in range(n)]
    N = 10000
    cases = ["4\n1 1 3 4\n4 4 1 1\n2\n"]
    cases.append(fmt(R(N), R(N), r.randint(1, N - 1)))
    cases.append(fmt(R(N), R(N), 0))
    cases.append(fmt(R(N), R(N), N))
    cases.append(fmt([1000] * N, [1000] * N, N // 2))
    # reward1 大但差值小的项与 reward1 小但差值大的项混合：卡“按 reward1 排序”
    a, b = [], []
    for _ in range(N):
        if r.random() < 0.5:
            x = r.randint(900, 1000); a.append(x); b.append(x - r.randint(0, 5) if x > 5 else x)
        else:
            x = r.randint(300, 600); a.append(x); b.append(r.randint(1, 50))
    cases.append(fmt(a, [max(1, v) for v in b], N // 3))
    cases.append(fmt(R(N, 1, 10), R(N, 990, 1000), N - 1))
    cases += ["1\n5\n7\n0\n", "1\n5\n7\n1\n", "1\n1000\n1\n0\n", "2\n1 1000\n1000 1\n1\n"]
    cases.append(fmt([1] * 50, [1] * 50, 25))
    for _ in range(6):
        n = r.randint(1, 30)
        cases.append(fmt(R(n), R(n), r.randint(0, n)))
    for _ in range(6):
        n = r.randint(31, 3000)
        cases.append(fmt(R(n), R(n), r.choice([0, n, r.randint(0, n)])))
    return cases


def run(text):
    x = subprocess.run([sys.executable, str(HERE / "samplecode.py")], input=text,
                       text=True, capture_output=True, timeout=120)
    if x.returncode:
        raise SystemExit(x.stderr)
    return x.stdout


def main():
    d = HERE / "data"
    d.mkdir(exist_ok=True)
    for i, c in enumerate(build_cases()):
        assert valid(c), i
        (d / f"{i}.in").write_text(c)
        (d / f"{i}.out").write_text(run(c))


if __name__ == "__main__":
    main()

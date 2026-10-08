"""28321 电影排片 测试数据生成器。

题面：第一行 t（1 <= t <= 10000）；每组：一行 n（1 <= n <= 100），一行 n 个非降整数 a（0..100），
一行 n 个非降整数 b（0..100）。第 0 组为样例。
每组 .in 须 <= 1MB，所以“t=10000”的组用小 n，“n=100”的组 t 控制在 1MB 以内。
"""
import random
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SEED = 28321
NUM = re.compile(r"[1-9][0-9]*|0")


def valid(text):
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if not NUM.fullmatch(lines[0]):
        return False
    t = int(lines[0])
    if not 1 <= t <= 10000 or len(lines) != 1 + 3 * t:
        return False
    for i in range(t):
        ns = lines[1 + 3 * i]
        if not NUM.fullmatch(ns) or not 1 <= int(ns) <= 100:
            return False
        n = int(ns)
        for row in lines[2 + 3 * i:4 + 3 * i]:
            parts = row.split(" ")
            if len(parts) != n or not all(NUM.fullmatch(p) and 0 <= int(p) <= 100 for p in parts):
                return False
            v = list(map(int, parts))
            if any(v[j] > v[j + 1] for j in range(n - 1)):
                return False
    return True


def one(r, n, mode):
    if mode == "rand":
        a = sorted(r.randint(0, 100) for _ in range(n)); b = sorted(r.randint(0, 100) for _ in range(n))
    elif mode == "close":  # a 在 b 附近浮动，答案多为小值
        b = sorted(r.randint(0, 100) for _ in range(n))
        a = sorted(min(100, max(0, x + r.randint(-3, 3))) for x in b)
    elif mode == "zero":   # 答案 0
        b = sorted(r.randint(0, 100) for _ in range(n))
        a = sorted(min(100, x + r.randint(0, 5)) for x in b)
    else:                  # "shift"：a 整体偏小
        a = sorted(r.randint(0, 60) for _ in range(n)); b = sorted(r.randint(30, 100) for _ in range(n))
    return a, b


def fmt(items):
    rows = [str(len(items))]
    for a, b in items:
        rows += [str(len(a)), " ".join(map(str, a)), " ".join(map(str, b))]
    return "\n".join(rows) + "\n"


MODES = ["rand", "close", "zero", "shift"]


def build_cases():
    r = random.Random(SEED)
    cases = ["2\n6\n10 20 30 40 50 60\n8 21 35 35 55 65\n6\n9 9 9 30 40 50\n10 20 30 40 50 60\n"]
    # t=10000，小 n
    cases.append(fmt([one(r, r.randint(1, 8), r.choice(MODES)) for _ in range(10000)]))
    # n=100，t 取到约 1MB
    cases.append(fmt([one(r, 100, r.choice(MODES)) for _ in range(1650)]))
    # t=10000，n 混合（含 n=100）
    items = [one(r, 100 if r.random() < 0.05 else r.randint(1, 12), r.choice(MODES)) for _ in range(10000)]
    cases.append(fmt(items))
    # 边界
    cases.append("1\n1\n0\n100\n")
    cases.append("1\n1\n100\n0\n")
    cases.append("1\n1\n50\n50\n")
    cases.append(fmt([([0] * 100, [100] * 100)]))          # 答案 100
    cases.append(fmt([([100] * 100, [0] * 100)]))          # 答案 0
    cases.append(fmt([(list(range(100)), list(range(1, 101)))]))  # 答案 1
    cases.append(fmt([([0] * 99 + [100], [100] * 100)]))  # 答案 99
    # a 的最大值卡在 b 的某处，测试提前 break 之类的写法
    cases.append(fmt([([1, 1, 1, 100], [0, 2, 2, 2]), ([5, 5, 5], [5, 5, 6]), ([0, 0, 7], [1, 1, 1])]))
    for mode in MODES:
        for _ in range(2):
            cases.append(fmt([one(r, r.randint(1, 100), mode) for _ in range(r.randint(1, 300))]))
    for _ in range(3):
        cases.append(fmt([one(r, r.randint(1, 5), r.choice(MODES)) for _ in range(r.randint(1, 50))]))
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
        assert len(c.encode()) <= 1_000_000, (i, len(c))
        (d / f"{i}.in").write_text(c)
        (d / f"{i}.out").write_text(run(c))


if __name__ == "__main__":
    main()

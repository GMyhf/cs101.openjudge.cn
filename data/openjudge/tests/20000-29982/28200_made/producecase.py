"""28200 超大二叉树 测试数据生成器。

题面：2 <= N <= 10^6，1 <= D <= 2*10^6；输入一行两个整数 N D。
树上最大距离为 2N-2，D 大部分取在 [1, 2N-2] 内，只留少量 D > 2N-2（答案 0）的组。
第 0 组为样例 1，第 1 组为样例 2；含 N=10^6 满规模组。
"""
import random
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SEED = 28200


def valid(text):
    if not re.fullmatch(r"[0-9]+ [0-9]+\n", text):
        return False
    n, d = map(int, text.split())
    return 2 <= n <= 10**6 and 1 <= d <= 2 * 10**6 and str(n) + " " + str(d) + "\n" == text


def build_cases():
    r = random.Random(SEED)
    pairs = [
        (3, 2),             # 样例 1
        (14142, 17320),     # 样例 2
        (10**6, 10**6),     # 满规模
        (10**6, 1999998),   # 满规模，D 恰为最大距离
        (999983, 2 * 10**6),  # 接近满规模且 D 取上限（D > 2N-2，答案 0）
        (10**6, 1),
        (2, 1), (2, 2), (2, 3),
        (3, 4), (5, 7), (10, 18),
        (20, 30), (31, 60),
        (2, 2 * 10**6),
    ]
    # 中等规模：卡 O(N*D) 写法
    for _ in range(4):
        n = r.randint(20000, 200000)
        pairs.append((n, r.randint(1, 2 * n - 2)))
    for _ in range(6):
        n = r.randint(2, 3000)
        pairs.append((n, r.randint(1, 2 * n - 2)))
    for _ in range(3):
        n = r.randint(300000, 999999)
        pairs.append((n, r.randint(n // 2, min(2 * 10**6, 2 * n - 2))))
    seen, out = set(), []
    for p in pairs:
        if p not in seen:
            seen.add(p)
            out.append(f"{p[0]} {p[1]}\n")
    return out


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

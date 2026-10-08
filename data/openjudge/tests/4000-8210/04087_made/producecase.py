"""4087 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的数据。

第 0 组是题面样例；1..39 组沿用原生成器（n<=60）；40 组起补大规模、k 的边界、
重复值、值域上界 1e9、多行与多空格分隔。
题面上限 n=1e6，但值域到 1e9 时单组 .in 会远超 1MB，故大组按 1MB 封顶取 n：
大值域约 9 万个数，小值域约 30 万个数，k 取到上限 1e5。
"""
import random
import subprocess
from pathlib import Path

I = '10 5\n1  3  8 20 2 \n9 10 12  8 9\n'


def valid(text):
    """题面契约：第一行 n k（10<=n<=1e6, 1<=k<=1e5，且 k<=n）；
    其后 n 个正整数 T（1<=T<=1e9），以空格或换行分隔。"""
    if not text.endswith("\n"):
        return False
    first, _, rest = text.partition("\n")
    head = first.split()
    if len(head) != 2:
        return False
    if set(rest) - set("0123456789 \n"):
        return False
    try:
        n, k = int(head[0]), int(head[1])
        vals = [int(t) for t in rest.split()]
    except ValueError:
        return False
    if not (10 <= n <= 10 ** 6 and 1 <= k <= 10 ** 5 and k <= n):
        return False
    return len(vals) == n and all(1 <= v <= 10 ** 9 for v in vals)


def g4087(r):
    n = r.randint(10, 60)
    return f"{n} {r.randint(1, n)}\n" + " ".join(str(r.randint(1, 10 ** 6)) for _ in range(n)) + "\n"


def fmt(k, vals, r, per_line=20, double=0.0):
    lines = []
    for i in range(0, len(vals), per_line):
        chunk = vals[i:i + per_line]
        parts = []
        for v in chunk:
            parts.append(str(v))
            parts.append("  " if r.random() < double else " ")
        lines.append("".join(parts[:-1]))
    return f"{len(vals)} {k}\n" + "\n".join(lines) + "\n"


def extra_cases():
    r = random.Random(4087 * 7 + 1)
    B = 10 ** 9
    cases = []
    cases.append(fmt(1, [B] * 10, r))                                    # 最小 n、全为上界
    cases.append(fmt(10, list(range(10, 0, -1)), r, 3, 0.5))             # k=n
    cases.append(fmt(1, [r.randint(1, B) for _ in range(10)], r, 1))     # 每行一个
    # 大值域、约 9 万个数
    for k in (1, 100000 // 2, 85000):
        n = 85000
        cases.append(fmt(k, [r.randint(1, B) for _ in range(n)], r, 25, 0.05))
    # 上界附近：第 k 小落在大量重复的 1e9 上
    vals = [B] * 80000 + [r.randint(1, B) for _ in range(5000)]
    r.shuffle(vals)
    cases.append(fmt(82000, vals, r, 30))
    # 小值域、约 30 万个数，k 取上限 1e5，大量重复
    for hi in (99, 9, 1):
        n = 300000
        cases.append(fmt(10 ** 5, [r.randint(1, hi) for _ in range(n)], r, 40))
    # 降序输入：维护大小为 k 的堆时每个数都要替换堆顶
    n = 100000
    vals = sorted((r.randint(1, 10 ** 5) for _ in range(n)), reverse=True)
    cases.append(fmt(10 ** 5, vals, r, 50))
    cases.append(fmt(99999, vals[::-1], r, 50))
    # 升序输入、k=1；以及 k 恰好落在一段重复值的首/尾
    cases.append(fmt(1, sorted(r.randint(1, 10 ** 5) for _ in range(n)), r, 50))
    vals = [5] * 10 + [8] * 10 + [3] * 10
    r.shuffle(vals)
    cases.append(fmt(20, vals, r, 7, 0.3))
    cases.append(fmt(21, vals, r, 7, 0.3))
    return cases


def build_cases():
    return [I if i == 0 else g4087(random.Random(4087 + i)) for i in range(40)] + extra_cases()


def main():
    root = Path(__file__).parent
    binary = root / "reference"
    subprocess.run(["g++", "-std=c++17", "-O2", str(root / "samplecode.cpp"), "-o", str(binary)], check=True)
    try:
        for i, c in enumerate(build_cases()):
            assert valid(c), i
            p = subprocess.run([str(binary)], input=c, text=True, capture_output=True, check=True)
            (root / "data" / f"{i}.in").write_text(c)
            (root / "data" / f"{i}.out").write_text(p.stdout)
    finally:
        binary.unlink()


if __name__ == "__main__":
    main()

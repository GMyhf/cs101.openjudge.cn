#!/usr/bin/env python3
"""2209C Find the Zero：交互题隐藏数据（固定数组 F / 自适应对手 A），参考解逐组经 judge.run_interactive 验证。

隐藏数据格式见 interactor.py 文档串。.out 只是占位（每组一行 n），交互器不读。
第 0 组 = 题面样例：两组固定数组 [0 1 0 2] 与 [3 2 0 1 0 0]，逐字复现 Note 的回应。
"""
from __future__ import annotations

import itertools
import random
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(ROOT))
import judge  # noqa: E402

INTERACTOR = "tests/codeforces/2209C_made/interactor.py"
REFERENCE = HERE / "samplecode.py"
MAX_T, MAX_N, MAX_SUM = 1000, 10000, 10000


def F(a):
    return ("F", list(a))


def A(n, q, s):
    return ("A", n, q, s)


def size(test):
    return len(test[1]) // 2 if test[0] == "F" else test[1]


def render(tests):
    lines = [str(len(tests))]
    for test in tests:
        if test[0] == "F":
            lines.append(" ".join(map(str, [len(test[1]) // 2, "F", *test[1]])))
        else:
            lines.append(" ".join(map(str, [test[1], "A", test[2], test[3]])))
    return "\n".join(lines) + "\n"


SAMPLE = render([F([0, 1, 0, 2]), F([3, 2, 0, 1, 0, 0])])


def valid(text):
    try:
        rows = text.split("\n")
        if rows[-1] != "" or not 1 <= int(rows[0]) <= MAX_T or len(rows) != int(rows[0]) + 2:
            return False
        total = 0
        for row in rows[1:-1]:
            v = row.split(" ")
            n = int(v[0])
            if not 2 <= n <= MAX_N:
                return False
            total += n
            if v[1] == "F":
                a = list(map(int, v[2:]))
                if len(a) != 2 * n or sorted(a) != [0] * n + list(range(1, n + 1)):
                    return False
            elif v[1] == "A":
                if len(v) != 4 or not 0 <= int(v[2]) <= 100 or int(v[3]) < 0:
                    return False
            else:
                return False
        return total <= MAX_SUM and render_back(text) == text
    except (IndexError, ValueError):
        return False


def render_back(text):
    tests = []
    for row in text.split("\n")[1:-1]:
        v = row.split(" ")
        tests.append(F(map(int, v[2:])) if v[1] == "F" else A(int(v[0]), int(v[2]), int(v[3])))
    return render(tests)


# ---- 数组形状 ---------------------------------------------------------------

def rand_array(r, n):
    a = list(range(1, n + 1)) + [0] * n
    r.shuffle(a)
    return a


def with_zero_positions(r, n, zeros):
    zeros = set(zeros)
    values = list(range(1, n + 1))
    r.shuffle(values)
    it = iter(values)
    return [0 if i in zeros else next(it) for i in range(2 * n)]


def last_two_zero(r, n):
    """0-based 位置 2n-2、2n-1 为 0，前面 n-1 对里恰有一对没有 0。"""
    empty = r.randrange(n - 1) if n > 1 else None
    zeros = {2 * n - 2, 2 * n - 1}
    for p in range(n - 1):
        if p != empty and len(zeros) < n:
            zeros.add(2 * p + r.randrange(2))
    return with_zero_positions(r, n, zeros)


def one_zero_per_pair(r, n, last):
    """每对 (2p-1, 2p) 恰一个 0；last ∈ {0,1} 决定最后一对里哪个是 0。"""
    zeros = {2 * p + r.randrange(2) for p in range(n - 1)} | {2 * n - 2 + last}
    return with_zero_positions(r, n, zeros)


def fill_adaptive(r, total, lo, hi, qs, t_max=MAX_T):
    tests = []
    while total >= 2 and len(tests) < t_max:
        n = min(total, r.randint(lo, hi))
        if total - n == 1:
            n = total
        tests.append(A(n, r.choice(qs), r.randrange(10**9)))
        total -= n
    return tests


def generate(seed):
    r = random.Random(2209_0300 + seed * 6007)
    if seed == 1:      # n = 2 的全部 12 个数组 + 其余 n = 2 自适应
        arrays = sorted(set(itertools.permutations([0, 0, 1, 2])))
        tests = [F(a) for a in arrays] + [A(2, (0, 0, 30, 100)[k % 4], k) for k in range(MAX_T - len(arrays))]
    elif seed == 2:    # 单组最大 n，自适应，只答 0
        tests = [A(MAX_N, 0, 1)]
    elif seed == 3:    # 单组最大 n，固定随机数组
        tests = [F(rand_array(r, MAX_N))]
    elif seed == 4:    # t = 1000，n = 10，自适应只答 0
        tests = [A(10, 0, k) for k in range(MAX_T)]
    elif seed == 5:    # n = 3 的全部 120 个数组 + n = 3 自适应
        arrays = sorted(set(itertools.permutations([0, 0, 0, 1, 2, 3])))
        tests = [F(a) for a in arrays] + [A(3, 0, k) for k in range(880)]
        tests = tests[:1000]
        while sum(map(size, tests)) > MAX_SUM:
            tests.pop()
    elif seed == 6:    # 自适应，一半概率答 1，各种 n
        tests = fill_adaptive(r, MAX_SUM, 2, 60, (50,))
    elif seed == 7:    # 固定：最后两个都是 0（前面恰有一对没有 0）
        tests = [F(last_two_zero(r, n)) for n in [2, 3, 4, 5] * 25 + [80] * 110]
    elif seed == 8:    # 固定：每对恰一个 0，最后一对 0 在前/在后
        tests = [F(one_zero_per_pair(r, n, k % 2)) for k, n in enumerate([2, 3, 4, 7] * 40 + [150] * 55)]
    elif seed == 9:    # 固定：0 全在前一半 / 全在后一半 / 奇数位 / 偶数位（1-based）
        tests = []
        for k, n in enumerate([2, 3, 4, 5, 6, 50, 500, 2000, 2430] + [2] * 3):
            pattern = k % 4
            zeros = (range(n) if pattern == 0 else range(n, 2 * n) if pattern == 1
                     else range(0, 2 * n, 2) if pattern == 2 else range(1, 2 * n, 2))
            tests.append(F(with_zero_positions(r, n, zeros)))
    elif seed == 10:   # 自适应，能答 1 就答 1
        tests = fill_adaptive(r, MAX_SUM, 2, 200, (100,))
    elif seed == 11:   # 自适应，低概率答 1，n 跨度大
        tests = fill_adaptive(r, MAX_SUM, 2, 3000, (5, 10, 0))
    elif seed == 12:   # t = 1000，小 n，自适应与固定混合
        tests = []
        for k in range(MAX_T):
            n = r.randint(2, 18)
            tests.append(A(n, r.choice((0, 0, 20)), r.randrange(10**9)) if k % 3 else F(rand_array(r, n)))
        while sum(map(size, tests)) > MAX_SUM:
            tests.pop()
    elif seed == 13:   # 两组 n = 5000
        tests = [A(5000, 0, 13), A(5000, 30, 14)]
    elif seed == 14:   # 自适应只答 0，n = 2, 3, 4, ... 递增
        tests, n, total = [], 2, 0
        while total + n <= MAX_SUM:
            tests.append(A(n, 0, n)); total += n; n += 1
    elif seed == 15:   # 固定：0 在第 2n 位、2n-1 非 0，每对一个 0（专挑「猜 2n-1」）
        tests = [F(one_zero_per_pair(r, n, 1)) for n in [2] * 200 + [3] * 200 + [5] * 200 + [9] * 200 + [11] * 200]
        while sum(map(size, tests)) > MAX_SUM:
            tests.pop()
    elif seed == 16:   # t = 1000，全部 n = 2，自适应各种 q
        tests = [A(2, (0, 10, 50, 90)[k % 4], k * 7) for k in range(MAX_T)]
    elif seed == 17:   # 固定随机数组，很多小 n
        tests = [F(rand_array(r, r.randint(2, 25))) for _ in range(700)]
        while sum(map(size, tests)) > MAX_SUM:
            tests.pop()
    elif seed == 18:   # 两组接近最大：4999 + 5001
        tests = [A(4999, 0, 18), A(5001, 0, 19)]
    elif seed == 19:   # 大 n 的 A/F/A 三组 + 一组 n = 2，总和恰为 10000
        tests = [A(3333, 0, 21), F(rand_array(r, 3333)), A(3332, 60, 22), A(2, 0, 23)]
    else:              # 自适应中等 n，多数只答 0
        tests = fill_adaptive(r, MAX_SUM, 50, 800, (0, 0, 0, 25))
    return render(tests)


def run_reference(case):
    source = REFERENCE.read_text()
    with tempfile.TemporaryDirectory(prefix="cf2209c-") as tmp:
        cmd, fail = judge.prepare_program(Path(tmp), "python3", source)
        if fail:
            raise SystemExit(f"reference failed to prepare: {fail}")
        return judge.run_interactive(cmd, INTERACTOR, case.encode(), b"", Path(tmp),
                                     cpu_seconds=4, address_space_bytes=768 * 1024 * 1024,
                                     file_size_bytes=2 * 1024 * 1024)


def build():
    out = HERE / "data"
    out.mkdir(exist_ok=True)
    cases = [SAMPLE] + [generate(seed) for seed in range(1, 21)]
    if len(set(cases)) != len(cases):
        raise SystemExit("duplicate cases")
    for index, case in enumerate(cases):
        if not valid(case) or len(case) > 1_000_000:
            raise SystemExit(f"invalid case {index}")
        result = run_reference(case)
        if result["outcome"] != "accepted":
            raise SystemExit(f"reference not accepted on case {index}: {result['outcome']} {result['message']}")
        print(f"case {index}: {result['time_ms']} ms", file=sys.stderr)
        answer = "\n".join(row.split(" ")[0] for row in case.split("\n")[1:-1]) + "\n"
        (out / f"{index}.in").write_text(case, encoding="utf-8")
        (out / f"{index}.out").write_text(answer, encoding="utf-8")


if __name__ == "__main__":
    build()

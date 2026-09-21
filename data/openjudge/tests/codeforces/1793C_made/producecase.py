#!/usr/bin/env python3
"""Codeforces 1793C Dora and Search —— 生成器、输入契约与数据构建（配 checker.py 特判）。

2026-09-17 新建。题面：t（1≤t≤10^4）组，每组一个长为 n（1≤n≤2·10^5）的排列，Σn ≤ 2·10^5；
找 l ≤ r 使 a_l、a_r 都不是 a[l..r] 的最小/最大值，输出 l r 或 -1；答案不唯一，由 checker.py 判。

「剥壳」构造：从一个核心排列出发，反复在左端或右端添一个「新最小值」或「新最大值」。
核心本身无解（长度 1）则整个排列无解；核心是合法区间（如 2 1 4 3）则有解且解藏在核心处。
判别力按「这题会怎么错」排（seed → 形状）：
  1      n=1
  2      n=1..6 的全部排列（873 组），暴力 oracle 逐组核对
  3      10^4 组 n∈[1,20] 随机排列
  4-5    n=2·10^5 升序 / 降序：无解
  6      n=2·10^5 从单点随机剥壳：无解（只看全局 1、n 位置的挂）
  7      10^4 组 n=20 剥壳无解
  8      n=2·10^5 剥壳，核心 2 1 4 3 藏在随机深处
  9      2 1 3 4 … n-2 n n-1：唯一合法区间是 [1, n]
  10     n=2·10^5 随机排列
  11     10^4 组 n=20 随机排列
  12     100 组、长度不一，一半剥壳无解、一半核心随机（4..10 长的合法核心）
  13     10^4 组 n∈[1,3]：全是 -1（对 n<4 也输出区间的挂）
  14     1 n 2 n-1 3 …（之字形）：无解
  15     两组 n=10^5：只有 [1,n] 合法 + 剥壳无解
  16     两组 n=10^5：核心贴着最左端（只往右剥）/ 贴着最右端（只往左剥）
  17     10^4 组 n∈[4,8] 随机排列
  18     n=2·10^5 左右交替剥壳，核心在正中
  19     之字形中间两对交换：左边剥到正中卡住，解是 [n/2-1, n]（不是整段也不是核心）
  20     10^4 组 n=20：一半剥壳无解、一半有核心
参考解 samplecode.py 是双指针收缩。构建时独立复核：参考给出的区间直接按定义求 min/max 验证；
参考给出 -1 的组，n ≤ 60 用 O(n²) 暴力枚举全部区间确认，更大的组必须是「剥壳无解」构造出来的。
然后逐文件调用 checker：参考解通过，两份不同的合法区间（把区间收紧到内部最值两侧）通过，
几份错误输出被拒。
"""
from __future__ import annotations
import itertools
import random
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REFERENCE = HERE / "samplecode.py"
CHECKER = HERE / "checker.py"
INPUT_DOMAIN = "The first line contains a single integer t (1 ≤ t ≤ 10^4). For each test case, the first line contains one integer n (1 ≤ n ≤ 2·10^5); the second line contains n distinct integers a_1..a_n (1 ≤ a_i ≤ n). The sum of n over all test cases doesn't exceed 2·10^5."
SAMPLE = "4\n3\n1 2 3\n4\n2 1 4 3\n7\n1 3 2 4 6 5 7\n6\n2 3 6 5 4 1\n"
SAMPLE_OUT = "-1\n1 4\n2 6\n-1\n"
MAX_T, MAX_N = 10_000, 200_000
BRUTE_N = 60


def _peel(r, core, total, left_bias=0.5, alternate=False):
    """在核心外反复添「新最小/新最大」到左端或右端，归一化成 1..total 的排列。"""
    left, right = [], []
    lo, hi = 1, len(core)
    for step in range(total - len(core)):
        if r.random() < 0.5:
            lo -= 1; value = lo
        else:
            hi += 1; value = hi
        go_left = (step % 2 == 0) if alternate else (r.random() < left_bias)
        (left if go_left else right).append(value)
    values = left[::-1] + list(core) + right
    return [v - lo + 1 for v in values]


def _valid_core(r, k):
    while True:
        core = list(range(1, k + 1)); r.shuffle(core)
        if _brute(core):
            return core


def _brute(a):
    n = len(a)
    for l in range(n):
        lo = hi = a[l]
        for rr in range(l + 1, n):
            lo = min(lo, a[rr]); hi = max(hi, a[rr])
            if a[l] not in (lo, hi) and a[rr] not in (lo, hi):
                return True
    return False


def _only_whole(n):
    return [2, 1] + list(range(3, n - 1)) + [n, n - 1]


def _zigzag(n):
    out, lo, hi = [], 1, n
    while lo <= hi:
        out.append(lo); lo += 1
        if lo <= hi:
            out.append(hi); hi -= 1
    return out


def generate(seed):
    """返回 [(排列, 构造保证的有无解 True/False/None)]。"""
    r = random.Random(1793_000_003 + seed * 104_729)
    shuffled = lambda n: r.sample(range(1, n + 1), n)
    if seed == 1:
        return [([1], False)]
    if seed == 2:
        return [(list(p), None) for n in range(1, 7) for p in itertools.permutations(range(1, n + 1))]
    if seed == 3:
        return [(shuffled(r.randint(1, 20)), None) for _ in range(MAX_T)]
    if seed == 4:
        return [(list(range(1, MAX_N + 1)), False)]
    if seed == 5:
        return [(list(range(MAX_N, 0, -1)), False)]
    if seed == 6:
        return [(_peel(r, [1], MAX_N), False)]
    if seed == 7:
        return [(_peel(r, [1], 20), False) for _ in range(MAX_T)]
    if seed == 8:
        return [(_peel(r, [2, 1, 4, 3], MAX_N, left_bias=r.uniform(0.3, 0.7)), True)]
    if seed == 9:
        return [(_only_whole(MAX_N), True)]
    if seed == 10:
        return [(shuffled(MAX_N), None)]
    if seed == 11:
        return [(shuffled(20), None) for _ in range(MAX_T)]
    if seed == 12:
        sizes = [MAX_N // 100] * 100
        out = []
        for i, size in enumerate(sizes):
            if i % 2:
                out.append((_peel(r, [1], size), False))
            else:
                out.append((_peel(r, _valid_core(r, r.randint(4, 10)), size, left_bias=r.random()), True))
        return out
    if seed == 13:
        return [(shuffled(r.randint(1, 3)), False) for _ in range(MAX_T)]
    if seed == 14:
        return [(_zigzag(MAX_N), False)]
    if seed == 15:
        return [(_only_whole(MAX_N // 2), True), (_peel(r, [1], MAX_N // 2), False)]
    if seed == 16:
        return [(_peel(r, [2, 1, 4, 3], MAX_N // 2, left_bias=0.0), True),
                (_peel(r, [3, 4, 1, 2], MAX_N // 2, left_bias=1.0), True)]
    if seed == 17:
        return [(shuffled(r.randint(4, 8)), None) for _ in range(MAX_T)]
    if seed == 18:
        return [(_peel(r, [2, 4, 1, 3], MAX_N, alternate=True), True)]
    if seed == 19:
        a = _zigzag(MAX_N)
        # 之字形 1 n 2 n-1 …：把正中 4 个数重排成「次小 最小 最大 次大」，从左剥到这里就卡住
        m = MAX_N // 2
        core_values = sorted(a[m - 2:m + 2])
        a[m - 2:m + 2] = [core_values[1], core_values[0], core_values[3], core_values[2]]
        return [(a, None)]
    return [(_peel(r, [1], 20), False) if i % 2 else (_peel(r, _valid_core(r, 4), 20, left_bias=r.random()), True)
            for i in range(MAX_T)]


def _render(tests):
    return f"{len(tests)}\n" + "".join(f"{len(a)}\n{' '.join(map(str, a))}\n" for a, _ in tests)


def valid(text):
    """题面：t；每组一行 n、一行 n 个互不相同的 1..n；Σn ≤ 2·10^5。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    try:
        t = int(lines[0])
        if not (1 <= t <= MAX_T) or len(lines) != 1 + 2 * t or lines[0] != str(t):
            return False
        total = 0
        for i in range(t):
            n = int(lines[1 + 2 * i]); row = lines[2 + 2 * i].split(" ")
            if lines[1 + 2 * i] != str(n) or not 1 <= n <= MAX_N or len(row) != n:
                return False
            if any(x != str(int(x)) for x in row) or sorted(map(int, row)) != list(range(1, n + 1)):
                return False
            total += n
    except ValueError:
        return False
    return total <= MAX_N


def _parse(text):
    data = list(map(int, text.split())); p = 1; out = []
    for _ in range(data[0]):
        n = data[p]; out.append(data[p + 1:p + 1 + n]); p += 1 + n
    return out


def _segment_ok(a, l, r):
    seg = a[l - 1:r]
    return 1 <= l <= r <= len(a) and a[l - 1] not in (min(seg), max(seg)) and a[r - 1] not in (min(seg), max(seg))


def _answers(output):
    tokens, q, out = output.split(), 0, []
    while q < len(tokens):
        if tokens[q] == "-1":
            out.append(None); q += 1
        else:
            out.append((int(tokens[q]), int(tokens[q + 1]))); q += 2
    return out


def _tighten(a, pair, side):
    """合法区间内部最值的位置 pm、pM 都严格在端点之间；[l, max(pm,pM)+1] 与 [min(pm,pM)-1, r] 仍合法。"""
    l, r = pair
    seg = a[l - 1:r]
    pm = l + seg.index(min(seg)); pM = l + seg.index(max(seg))
    return (l, max(pm, pM) + 1) if side == "right" else (min(pm, pM) - 1, r)


def _alternatives(perms, output):
    answers = _answers(output); alts = []
    for side in ("right", "left"):
        rows = [("-1" if pair is None else "%d %d" % _tighten(a, pair, side)) for a, pair in zip(perms, answers)]
        alts.append("\n".join(rows) + "\n")
    return alts


def _wrongs(perms, output):
    answers = _answers(output)
    rows = ["-1" if p is None else f"{p[0]} {p[1]}" for p in answers]
    bad = ["", "\x00\xff\n", "-1 " * (len(perms) + 1), " ".join(rows + ["-1"]) + "\n",
           "9" * 5000 + "\n", "\n".join(rows[:-1]) + "\n"]
    if any(p is not None for p in answers):
        bad.append("\n".join("-1" for _ in perms) + "\n")                                   # 全输出 -1
        bad.append("\n".join("-1" if p is None else f"{p[0] - 1} {p[1] - 1}" for p in answers) + "\n")   # 0 下标
        bad.append("\n".join("-1" if p is None else f"{p[0]} {p[1]} 0" for p in answers) + "\n")
        bad.append("\n".join("-1" if p is None else f"{p[0]}.0 {p[1]}" for p in answers) + "\n")
    if any(p is None for p in answers):
        bad.append("\n".join(f"1 {len(a)}" if p is None else f"{p[0]} {p[1]}" for a, p in zip(perms, answers)) + "\n")
    return bad


def _check(case, output, answer):
    with tempfile.TemporaryDirectory() as temp:
        paths = []
        for name, data in (("in", case), ("out", output), ("ans", answer)):
            path = Path(temp) / name
            path.write_bytes(data.encode("latin-1"))
            paths.append(str(path))
        code = subprocess.run([sys.executable, "-I", str(CHECKER), *paths], capture_output=True).returncode
    if code not in (0, 42):
        raise SystemExit(f"checker 自身出错（退出码 {code}）")
    return code == 0


def build():
    out = HERE / "data"
    out.mkdir(exist_ok=True)
    for path in out.glob("*"):
        path.unlink()
    sample_tests = [(a, None) for a in _parse(SAMPLE)]
    groups = [sample_tests] + [generate(seed) for seed in range(1, 40)]
    cases = [_render(tests) for tests in groups]
    if cases[0] != SAMPLE or len(set(cases)) != len(cases):
        raise SystemExit("第 0 组不是样例，或两组输入撞了")
    totals = {"pair": 0, "none": 0}
    for index, (tests, case) in enumerate(zip(groups, cases)):
        if not valid(case):
            raise SystemExit(f"case {index} violates the input contract")
        answer = subprocess.run([sys.executable, str(REFERENCE)], input=case, text=True,
                                capture_output=True, timeout=120, check=True).stdout
        if index == 0 and answer != SAMPLE_OUT:
            raise SystemExit(f"第 0 组与题面样例输出不符：{answer!r}")
        answers = _answers(answer)
        if len(answers) != len(tests):
            raise SystemExit(f"case {index}: 参考解输出组数不对")
        for (a, expected), pair in zip(tests, answers):
            if pair is not None:
                totals["pair"] += 1
                if expected is False or not _segment_ok(a, *pair):
                    raise SystemExit(f"case {index}: 参考解给的区间不合法或与构造矛盾")
            else:
                totals["none"] += 1
                if expected is True or (expected is None and len(a) > BRUTE_N):
                    raise SystemExit(f"case {index}: 参考解输出 -1 却无法独立确认")
                if len(a) <= BRUTE_N and _brute(a):
                    raise SystemExit(f"case {index}: 暴力找到了合法区间，参考解却输出 -1")
        if not _check(case, answer, answer):
            raise SystemExit(f"case {index}: checker 不接受参考解")
        for alt in _alternatives([a for a, _ in tests], answer):
            if not _check(case, alt, answer):
                raise SystemExit(f"case {index}: checker 拒绝了另一种合法区间")
        for bad in _wrongs([a for a, _ in tests], answer):
            if _check(case, bad, answer):
                raise SystemExit(f"case {index}: checker 接受了错误输出 {bad[:40]!r}")
        if len(case.encode()) > 3 * 1024 * 1024 or len(answer.encode()) > 1_500_000:
            raise SystemExit(f"case {index} 超出体积上限")
        (out / f"{index}.in").write_text(case, encoding="utf-8")
        (out / f"{index}.out").write_text(answer, encoding="utf-8")
    print(totals)


if __name__ == "__main__":
    build()

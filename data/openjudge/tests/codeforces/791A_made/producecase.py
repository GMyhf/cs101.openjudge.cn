#!/usr/bin/env python3
"""791A Bear and Big Brother —— 单题生成器、输入契约与数据构建。

本文件负责输入，`samplecode.py` 负责答案，两者逻辑独立。构建时先拿参考实现
对一遍**全部官方样例**（`SAMPLES`，抄自 `data/openjudge/statements/791A.json`）。

题面的输入契约（`INPUT_DOMAIN`）：两个整数 `1 ≤ a ≤ b ≤ 10`。合法输入只有 55 种，
所以这里不撒随机，而是**把会挂人的那几类整类收进来**：
  · `tie`    —— 某一年两人恰好一样重（3a = 2b 或 9a = 4b：(2,3) (4,6) (6,9) (4,9)）。
               题面要的是「严格重于」，把 `<=` 写成 `<` 会在这一年提前停下，少算一年；
  · `equal`  —— a = b，答案 1；`while a < b` 的写法一次都不进循环，输出 0；
  · `widest` —— b - a ≥ 7，年数最多（(1,10) 要 6 年），压循环次数；
  · `upper_edge` —— b = 10；`plain` —— 其余合法值。
`tie` 只有 4 种输入、在 20 组里恰好出现 4 次，`_build()` 断言它们一个不漏。
"""
from __future__ import annotations
import random

PROBLEM = "791A"
INPUT_DOMAIN = "1 ≤ a ≤ b ≤ 10"
SAMPLES = (("4 7\n", "2\n"), ("4 9\n", "3\n"), ("1 1\n", "1\n"))
INVALID = "5 4\n"                        # a > b 违反「Limak 不重于 Bob」
DOMAIN = [(a, b) for a in range(1, 11) for b in range(a, 11)]
TIES = [(a, b) for a, b in DOMAIN if any(a * 3 ** y == b * 2 ** y for y in range(1, 8))]
SHAPES = ("tie", "equal", "widest", "upper_edge", "plain")


def generate(problem, seed, attempt=0):
    """固定种子；`attempt` 只在两组撞车时递增，撞车不改形状、只换随机数。"""
    if problem != PROBLEM:
        raise KeyError(problem)
    r = random.Random(0x791A * 1_000_003 + seed * 9_176 + attempt)
    shape = SHAPES[(seed - 1) % len(SHAPES)]
    pool = {
        "tie": TIES,
        "equal": [(a, b) for a, b in DOMAIN if a == b],
        "widest": [(a, b) for a, b in DOMAIN if b - a >= 7],
        "upper_edge": [(a, b) for a, b in DOMAIN if b == 10],
    }.get(shape, DOMAIN)
    if shape == "tie":
        # 平局对只有 4 个，按出现次序轮着取，保证 20 组里一个不漏
        a, b = TIES[((seed - 1) // len(SHAPES) + attempt) % len(TIES)]
    else:
        a, b = r.choice(pool)
    return f"{a} {b}\n"


def valid(problem, text):
    if problem != PROBLEM:
        raise KeyError(problem)
    tokens = text.split()
    if len(tokens) != 2 or not all(token.isdigit() for token in tokens):
        return False
    a, b = map(int, tokens)
    return 1 <= a <= b <= 10


import subprocess as _subprocess, sys as _sys
from pathlib import Path as _Path
REFERENCE = _Path(__file__).with_name("samplecode.py")
LANGUAGE = "Python3"


def _reference(case):
    return _subprocess.run([_sys.executable, str(REFERENCE)], input=case, text=True,
                           capture_output=True, timeout=120, check=True).stdout


def _build():
    if valid(PROBLEM, INVALID):
        raise SystemExit("valid() accepts a known-invalid input")
    if TIES != [(2, 3), (4, 6), (4, 9), (6, 9)]:
        raise SystemExit(f"unexpected tie pairs: {TIES}")
    for sample_in, sample_out in SAMPLES:
        got = _reference(sample_in)
        if not valid(PROBLEM, sample_in) or got.rstrip("\n") != sample_out.rstrip("\n"):
            raise SystemExit(f"reference disagrees with the official sample {sample_in!r}: {got!r}")
    out = _Path(__file__).with_name("data")
    out.mkdir(exist_ok=True)
    for path in out.glob("*"):
        path.unlink()
    cases = [SAMPLES[0][0]]
    for seed in range(1, 21):
        attempt = 0
        case = generate(PROBLEM, seed)
        while case in cases:
            attempt += 1
            if attempt > 10_000:
                raise SystemExit(f"seed {seed}: unable to generate a distinct input")
            case = generate(PROBLEM, seed, attempt)
        cases.append(case)
    missing = [pair for pair in TIES if f"{pair[0]} {pair[1]}\n" not in cases]
    if missing:
        raise SystemExit(f"tie pairs missing from the data: {missing}")
    for index, case in enumerate(cases):
        if not valid(PROBLEM, case):
            raise SystemExit(f"case {index} violates the input contract: {case!r}")
        (out / f"{index}.in").write_text(case, encoding="utf-8")
        (out / f"{index}.out").write_text(_reference(case).rstrip("\n") + "\n", encoding="utf-8")


if __name__ == "__main__":
    _build()

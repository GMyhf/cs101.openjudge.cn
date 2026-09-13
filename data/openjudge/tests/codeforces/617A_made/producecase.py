#!/usr/bin/env python3
"""617A Elephant —— 单题生成器、输入契约与数据构建。

本文件负责输入，`samplecode.py` 负责答案，两者逻辑独立。构建时先拿参考实现
对一遍**全部官方样例**（`SAMPLES`，抄自 `data/openjudge/statements/617A.json`）。

题面的输入契约（`INPUT_DOMAIN`）：一个整数 `1 ≤ x ≤ 1000000`。

`SHAPES` 按「向上取整」的两种典型错法设计，两类必须都有：
  · `multiple_of_5` —— x 是 5 的倍数，`x // 5 + 1` 的写法在这里多算一步；
  · `remainder`     —— x 除以 5 有余数，`x // 5` 的写法在这里少算一步；
  · `below_five`    —— 1 ≤ x ≤ 4，答案 1，`x // 5` 会输出 0；
  · `upper_edge`    —— 贴着题面上界 10^6；
  · `small` / `plain` —— 中小规模的普通值。
"""
from __future__ import annotations
import random

PROBLEM = "617A"
INPUT_DOMAIN = "1 ≤ x ≤ 1000000"
SAMPLES = (("5\n", "1\n"), ("12\n", "3\n"))
INVALID = "1000001\n"
SHAPES = ("multiple_of_5", "remainder", "below_five", "upper_edge", "small", "plain")


def generate(problem, seed, attempt=0):
    """固定种子；`attempt` 只在两组撞车时递增，撞车不改形状、只换随机数。"""
    if problem != PROBLEM:
        raise KeyError(problem)
    r = random.Random(0x617A * 1_000_003 + seed * 9_176 + attempt)
    shape = SHAPES[(seed - 1) % len(SHAPES)]
    if shape == "multiple_of_5":
        x = 5 * r.randint(1, 200_000)
    elif shape == "remainder":
        x = 5 * r.randint(0, 199_999) + r.randint(1, 4)
    elif shape == "below_five":
        x = r.randint(1, 4)
    elif shape == "upper_edge":
        x = r.choice((1_000_000, 999_999, 999_996, 999_995))
    elif shape == "small":
        x = r.randint(6, 30)
    else:
        x = r.randint(1, 1_000_000)
    return f"{x}\n"


def valid(problem, text):
    if problem != PROBLEM:
        raise KeyError(problem)
    tokens = text.split()
    if len(tokens) != 1 or not tokens[0].isdigit():
        return False
    return 1 <= int(tokens[0]) <= 1_000_000


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
    for index, case in enumerate(cases):
        if not valid(PROBLEM, case):
            raise SystemExit(f"case {index} violates the input contract: {case!r}")
        (out / f"{index}.in").write_text(case, encoding="utf-8")
        (out / f"{index}.out").write_text(_reference(case).rstrip("\n") + "\n", encoding="utf-8")


if __name__ == "__main__":
    _build()

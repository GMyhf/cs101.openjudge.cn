#!/usr/bin/env python3
"""977A Wrong Subtraction —— 单题生成器、输入契约与数据构建。

本文件负责输入，`samplecode.py` 负责答案。构建时先拿参考实现对一遍**全部官方样例**
（`SAMPLES`，抄自 `data/openjudge/statements/977A.json`）。

题面的输入契约（`INPUT_DOMAIN`）：`2 ≤ n ≤ 10^9`、`1 ≤ k ≤ 50`，并且**保证结果是正整数**。
最后这条是题面给的保证，不是答案：`valid()` 要按规则走 k 步确认它成立，否则
生成器可能造出结果为 0 的输入（例如 10 减 2 次），而那不是这道题的合法输入。

`SHAPES` 按这题真会挂人的写法设计：
  · `trailing_zeros` —— 末尾一串 0（如 1000000000），要连续「去末位」好几次；
                        写成 `n - k` 的会差得离谱；
  · `zero_inside`    —— 减着减着末位变成 0（如 512 → 510 → 51），规则来回切换，
                        只在开头判断一次末位的写法挂；
  · `max_steps`      —— k = 50 贴上界；
  · `tiny`           —— n 很小（2..20），压「结果恰好为 1」的边；
  · `plain`          —— 普通值。
"""
from __future__ import annotations
import random

PROBLEM = "977A"
INPUT_DOMAIN = "2 ≤ n ≤ 10^9；1 ≤ k ≤ 50；保证结果为正整数"
SAMPLES = (("512 4\n", "50\n"), ("1000000000 9\n", "1\n"))
INVALID = "10 2\n"                       # 10 → 1 → 0：结果不是正整数
SHAPES = ("trailing_zeros", "zero_inside", "max_steps", "tiny", "plain")


def _steps_possible(n, limit):
    """在结果保持为正的前提下，最多能走几步（不超过 limit）。"""
    steps = 0
    while steps < limit:
        n = n - 1 if n % 10 else n // 10
        if n <= 0:
            break
        steps += 1
    return steps


def generate(problem, seed, attempt=0):
    """固定种子；`attempt` 只在两组撞车时递增，撞车不改形状、只换随机数。"""
    if problem != PROBLEM:
        raise KeyError(problem)
    r = random.Random(0x977A * 1_000_003 + seed * 9_176 + attempt)
    shape = SHAPES[(seed - 1) % len(SHAPES)]
    if shape == "trailing_zeros":
        zeros = r.randint(2, 8)
        n = r.randint(1, 10 ** (9 - zeros)) * 10 ** zeros
        n = min(n, 10 ** 9)
    elif shape == "zero_inside":
        n = r.randint(1, 99_999) * 10 + r.randint(1, 9)
    elif shape == "max_steps":
        n = r.randint(10 ** 8, 10 ** 9)
    elif shape == "tiny":
        n = r.randint(2, 20)
    else:
        n = r.randint(2, 10 ** 9)
    most = _steps_possible(n, 50)
    k = most if shape == "max_steps" else r.randint(1, most)
    return f"{n} {k}\n"


def valid(problem, text):
    if problem != PROBLEM:
        raise KeyError(problem)
    tokens = text.split()
    if len(tokens) != 2 or not all(token.isdigit() for token in tokens):
        return False
    n, k = map(int, tokens)
    if not (2 <= n <= 10 ** 9 and 1 <= k <= 50):
        return False
    return _steps_possible(n, k) == k


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

#!/usr/bin/env python3
"""546A Soldier and Bananas —— 单题生成器、输入契约与数据构建。

本文件负责输入，`samplecode.py` 负责答案。构建时先拿参考实现对一遍**全部官方样例**
（`SAMPLES`，抄自 `data/openjudge/statements/546A.json`；官方样例输出末尾没有换行）。

题面的输入契约（`INPUT_DOMAIN`）：一行三个整数 `k n w`，`1 ≤ k, w ≤ 1000`、`0 ≤ n ≤ 10^9`。
注意**顺序是 k、n、w**，按 k、w、n 读的写法在大多数组上都会挂。

`SHAPES` 按这题真会挂人的写法设计：
  · `rich`         —— 钱比总价多，答案 0；**忘了和 0 取 max** 的写法输出负数；
  · `exact`        —— 钱恰好等于总价，答案 0；
  · `short_by_one` —— 差 1 块钱，答案 1；把总价算成 k·w·(w-1)/2（少算一根）的写法在这组露馅；
  · `broke`        —— n = 0，答案就是总价；
  · `maximum`      —— k = w = 1000，总价 500500000，压 32 位整数的中间量；
  · `plain`        —— 普通值。
"""
from __future__ import annotations
import random

PROBLEM = "546A"
INPUT_DOMAIN = "1 ≤ k, w ≤ 1000；0 ≤ n ≤ 10^9（输入顺序 k n w）"
SAMPLES = (("3 17 4\n", "13"),)
INVALID = "0 5 3\n"                      # k = 0 越过下界
SHAPES = ("rich", "exact", "short_by_one", "broke", "maximum", "plain")


def generate(problem, seed, attempt=0):
    """固定种子；`attempt` 只在两组撞车时递增，撞车不改形状、只换随机数。"""
    if problem != PROBLEM:
        raise KeyError(problem)
    r = random.Random(0x546A * 1_000_003 + seed * 9_176 + attempt)
    shape = SHAPES[(seed - 1) % len(SHAPES)]
    k, w = r.randint(1, 1000), r.randint(1, 1000)
    if shape == "maximum":
        k = w = 1000
    total = k * w * (w + 1) // 2
    if shape == "rich":
        n = r.randint(total + 1, 10 ** 9)
    elif shape == "exact":
        n = total
    elif shape == "short_by_one":
        n = total - 1
    elif shape == "broke":
        n = 0
    elif shape == "maximum":
        n = r.choice((0, r.randint(1, total - 1)))
    else:
        n = r.randint(0, 10 ** 9)
    return f"{k} {n} {w}\n"


def valid(problem, text):
    if problem != PROBLEM:
        raise KeyError(problem)
    tokens = text.split()
    if len(tokens) != 3 or not all(token.isdigit() for token in tokens):
        return False
    k, n, w = map(int, tokens)
    return 1 <= k <= 1000 and 1 <= w <= 1000 and 0 <= n <= 10 ** 9


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
    for seed in range(1, 40):
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

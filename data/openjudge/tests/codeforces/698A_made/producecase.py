#!/usr/bin/env python3
"""698A Vacations —— 单题生成器、输入契约与数据构建。

**为什么重写**：这题原先由中央批量生成器 `scripts/build_codeforces_basic_data.py`
产出，那里的递推求的是「最少活动天数」（全休息就是 0），21 组期望答案因此全是 0；
一次修补把它改成 `len(days) - min(...)`，又变成恒等于 `len(days)`。两版都不判别，
真正的正解反而 Wrong Answer。所以这题从中央生成器里摘出来，改走单题流水线：
本文件负责输入，`samplecode.py` 负责答案，两者逻辑独立。

题面的输入契约（`INPUT_DOMAIN` 是逐字原话）：`1 ≤ n ≤ 100`、`0 ≤ a_i ≤ 3`。
`valid()` 是同一条契约的反向校验，不满足就不许落盘。

`SHAPES` 摆的是这题真会挂人的几种形状，不是「多来点随机」：
  · `contest_only` / `sport_only` —— 整段只有一种活动可做，必须隔天休息，
       写成「能做就做」的贪心在这里不挂，但它是下面几种的对照组；
  · `greedy_trap` —— 交替出现「只能写题」与「两样都行」，
       **固定优先写题的贪心会被逼出多余的休息天**，这是最常见的错法；
  · `all_closed`  —— 全 0，答案就是 n（也顺带压 n 的上界）；
  · `all_open`    —— 全 3，答案 0；
  · `shortest` / `longest` —— 题面允许的两端（n = 1 和 n = 100）。
"""
from __future__ import annotations
import random

PROBLEM = "698A"
INPUT_DOMAIN = "1 ≤ n ≤ 100；0 ≤ a_i ≤ 3"
LABEL = "first line n (1..100), second line n integers in 0..3"
INVALID = "3\n0 1 4\n"                 # a_i = 4 越过题面的 3
SAMPLE = "4\n1 3 2 0\n"                # 题面样例：答案 2
SHAPES = ("greedy_trap", "contest_only", "sport_only", "all_closed",
          "all_open", "shortest", "longest", "plain")


def _days(r, shape):
    if shape == "shortest":
        return [r.randint(0, 3)]
    if shape == "longest":
        return [r.randint(0, 3) for _ in range(100)]
    if shape == "all_closed":
        return [0] * r.randint(1, 100)
    if shape == "all_open":
        return [3] * r.randint(1, 100)
    if shape == "contest_only":
        return [1] * r.randint(2, 60)
    if shape == "sport_only":
        return [2] * r.randint(2, 60)
    if shape == "greedy_trap":
        # 「只能写题」与「两样都行」交替：贪心若固定先写题，
        # 到下一个只能写题的日子就只好休息，而先运动的排法不用。
        block = r.randint(3, 20)
        days = []
        for index in range(block):
            days += [1, 3] if index % 2 == 0 else [3, 1]
        return days[:100]
    return [r.randint(0, 3) for _ in range(r.randint(1, 100))]


def generate(problem, seed, attempt=0):
    """固定种子；`attempt` 只在两组撞车时递增，撞车不改形状、只换随机数。"""
    if problem != PROBLEM:
        raise KeyError(problem)
    r = random.Random(0x698A * 1_000_003 + seed * 9_176 + attempt)
    days = _days(r, SHAPES[(seed - 1) % len(SHAPES)])
    return f"{len(days)}\n{' '.join(map(str, days))}\n"


def valid(problem, text):
    if problem != PROBLEM:
        raise KeyError(problem)
    tokens = text.split()
    if not tokens:
        return False
    try:
        n = int(tokens[0])
        days = list(map(int, tokens[1:]))
    except ValueError:
        return False
    return 1 <= n <= 100 and len(days) == n and all(0 <= value <= 3 for value in days)


import subprocess as _subprocess, sys as _sys
from pathlib import Path as _Path
REFERENCE = _Path(__file__).with_name("samplecode.py")
LANGUAGE = "Python3"


def _build():
    out = _Path(__file__).with_name("data")
    out.mkdir(exist_ok=True)
    for path in out.glob("*"):
        path.unlink()
    cases = [SAMPLE]
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
        result = _subprocess.run([_sys.executable, str(REFERENCE)], input=case, text=True,
                                 capture_output=True, timeout=120, check=True)
        (out / f"{index}.in").write_text(case, encoding="utf-8")
        (out / f"{index}.out").write_text(result.stdout.rstrip("\n") + "\n", encoding="utf-8")


if __name__ == "__main__":
    _build()

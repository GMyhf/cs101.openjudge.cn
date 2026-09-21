#!/usr/bin/env python3
"""734A Anton and Danik —— 单题生成器、输入契约与数据构建。

本文件负责输入，`samplecode.py` 负责答案。构建时先拿参考实现对一遍**全部官方样例**
（`SAMPLES`，抄自 `data/openjudge/statements/734A.json`）。

题面的输入契约（`INPUT_DOMAIN`）：第一行 `1 ≤ n ≤ 100000`，第二行是恰好 n 个
大写字母、只含 'A' 和 'D'。

`SHAPES` 按这题真会挂人的写法设计：三种输出**每种都要出现好几次**，否则
「永远输出 Anton」之类的写法会蒙对一大片：
  · `tie`         —— 平局，输出 Friendship；只写了两个分支的会挂；
  · `anton_by_one` / `danik_by_one` —— 只差一局，把 `>` 写成 `>=` 或名字写反的会挂；
  · `tiny`        —— n = 1..3；
  · `longest`     —— n 贴上界 100000，逐字符 `input()` 或 O(n²) 的写法在这里超时；
  · `plain`       —— 普通随机。
"""
from __future__ import annotations
import random

PROBLEM = "734A"
INPUT_DOMAIN = "1 ≤ n ≤ 100000；第二行恰好 n 个字符，只含 'A' 与 'D'"
SAMPLES = (("6\nADAAAA\n", "Anton\n"), ("7\nDDDAADA\n", "Danik\n"), ("6\nDADADA\n", "Friendship\n"))
INVALID = "3\nADX\n"                     # 出现了 A/D 以外的字母
SHAPES = ("tie", "anton_by_one", "danik_by_one", "tiny", "longest", "plain")


def _games(r, anton, danik):
    games = ["A"] * anton + ["D"] * danik
    r.shuffle(games)
    return "".join(games)


def generate(problem, seed, attempt=0):
    """固定种子；`attempt` 只在两组撞车时递增，撞车不改形状、只换随机数。"""
    if problem != PROBLEM:
        raise KeyError(problem)
    r = random.Random(0x734A * 1_000_003 + seed * 9_176 + attempt)
    shape = SHAPES[(seed - 1) % len(SHAPES)]
    if shape == "tie":
        half = r.randint(1, 2000)
        games = _games(r, half, half)
    elif shape == "anton_by_one":
        half = r.randint(0, 2000)
        games = _games(r, half + 1, half)
    elif shape == "danik_by_one":
        half = r.randint(0, 2000)
        games = _games(r, half, half + 1)
    elif shape == "tiny":
        games = "".join(r.choice("AD") for _ in range(r.randint(1, 3)))
    elif shape == "longest":
        # 上界附近再细分三种结局，免得 10 万级的数据全是同一个答案
        n = 100_000 - r.randint(0, 1)
        anton = n // 2 + r.choice((-1, 0, 1)) if n % 2 == 0 else n // 2 + r.randint(0, 1)
        games = _games(r, anton, n - anton)
    else:
        games = "".join(r.choice("AD") for _ in range(r.randint(1, 500)))
    return f"{len(games)}\n{games}\n"


def valid(problem, text):
    if problem != PROBLEM:
        raise KeyError(problem)
    lines = text.split("\n")
    if len(lines) < 2 or not lines[0].isdigit() or "".join(lines[2:]).strip():
        return False
    n, games = int(lines[0]), lines[1]
    return 1 <= n <= 100_000 and len(games) == n and set(games) <= {"A", "D"}


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
    answers = [_reference(case).strip() for case in cases]
    for verdict in ("Anton", "Danik", "Friendship"):
        if answers.count(verdict) < 4:
            raise SystemExit(f"only {answers.count(verdict)} cases answer {verdict}")
    for index, case in enumerate(cases):
        if not valid(PROBLEM, case):
            raise SystemExit(f"case {index} violates the input contract: {case[:80]!r}")
        (out / f"{index}.in").write_text(case, encoding="utf-8")
        (out / f"{index}.out").write_text(answers[index] + "\n", encoding="utf-8")


if __name__ == "__main__":
    _build()

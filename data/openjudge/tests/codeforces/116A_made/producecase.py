#!/usr/bin/env python3
"""116A Tram —— 单题生成器、输入契约与数据构建。

本文件负责输入，`samplecode.py` 负责答案，两者逻辑独立。构建时先拿参考实现
对一遍**全部官方样例**（`SAMPLES`，抄自 `data/openjudge/statements/116A.json`），
对不上就不许落盘 —— 那是这题唯一的仓外事实。

题面的输入契约（`INPUT_DOMAIN`）：`2 ≤ n ≤ 1000`、`0 ≤ a_i, b_i ≤ 1000`；
每站下车人数不超过到站前车上人数（于是 a_1 = 0）；末站所有人下车（a_n 等于
到站前人数）且 b_n = 0。`valid()` 逐条反向校验，不满足就不许落盘。

`SHAPES` 按这题真会挂人的写法设计：
  · `turnover`   —— 每站几乎全员下车、又上来一大批。**先上后下**（把 b_i 加上去
                   再减 a_i 取最大值）的写法在这里会把容量算大，这是最常见的错法；
  · `peak_middle` —— 先涨后落，最大值在中途，「输出最后一站 / 第一站」的写法挂；
  · `peak_first` —— 第一站就是峰值，之后只减不增；
  · `all_zero`   —— 全程空车，答案 0（题面明写 0 是允许的）；
  · `shortest` / `longest` —— n 取题面两端 2 和 1000。
"""
from __future__ import annotations
import random

PROBLEM = "116A"
INPUT_DOMAIN = "2 ≤ n ≤ 1000；0 ≤ a_i, b_i ≤ 1000；a_i ≤ 到站前人数；a_n = 到站前人数，b_n = 0"
SAMPLES = (("4\n0 3\n2 5\n4 2\n4 0\n", "6\n"),)
INVALID = "3\n1 2\n1 0\n1 0\n"          # a_1 = 1：空车到站却有人下车
SHAPES = ("turnover", "peak_middle", "peak_first", "all_zero", "shortest", "longest", "plain")
CAP = 1000                               # 车上人数封顶 1000，保证末站 a_n ≤ 1000


def _stops(r, shape, n):
    stops, inside = [], 0
    for index in range(n - 1):
        if shape == "all_zero":
            leave, enter = 0, 0
        elif shape == "turnover":
            leave = inside if r.randrange(3) else r.randint(inside // 2, inside)
            enter = r.randint(0, CAP)
        elif shape == "peak_middle":
            rising = index < (n - 1) // 2
            leave = r.randint(0, inside // 4) if rising else r.randint(inside // 2, inside)
            enter = r.randint(50, 400) if rising else r.randint(0, 20)
        elif shape == "peak_first":
            leave = 0 if index == 0 else r.randint(0, inside)
            enter = r.randint(600, CAP) if index == 0 else 0
        else:
            leave = r.randint(0, inside)
            enter = r.randint(0, CAP)
        enter = min(enter, CAP - (inside - leave))
        inside += enter - leave
        stops.append((leave, enter))
    stops.append((inside, 0))
    return stops


def generate(problem, seed, attempt=0):
    """固定种子；`attempt` 只在两组撞车时递增，撞车不改形状、只换随机数。"""
    if problem != PROBLEM:
        raise KeyError(problem)
    r = random.Random(0x116A * 1_000_003 + seed * 9_176 + attempt)
    shape = SHAPES[(seed - 1) % len(SHAPES)]
    n = {"shortest": 2, "longest": 1000}.get(shape) or r.randint(3, 200)
    stops = _stops(r, shape, n)
    return f"{n}\n" + "".join(f"{leave} {enter}\n" for leave, enter in stops)


def valid(problem, text):
    if problem != PROBLEM:
        raise KeyError(problem)
    lines = text.split("\n")
    try:
        n = int(lines[0])
        rows = [tuple(map(int, line.split())) for line in lines[1:1 + n]]
    except (ValueError, IndexError):
        return False
    if not 2 <= n <= 1000 or len(rows) != n or any(len(row) != 2 for row in rows):
        return False
    if "".join(lines[1 + n:]).strip():
        return False
    inside = 0
    for leave, enter in rows:
        if not (0 <= leave <= 1000 and 0 <= enter <= 1000) or leave > inside:
            return False
        inside += enter - leave
    return rows[-1][1] == 0 and inside == 0


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
            raise SystemExit(f"case {index} violates the input contract: {case[:80]!r}")
        (out / f"{index}.in").write_text(case, encoding="utf-8")
        (out / f"{index}.out").write_text(_reference(case).rstrip("\n") + "\n", encoding="utf-8")


if __name__ == "__main__":
    _build()

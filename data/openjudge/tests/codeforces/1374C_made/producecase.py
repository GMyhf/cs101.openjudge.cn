#!/usr/bin/env python3
"""1374C Move Brackets —— 单题生成器、输入契约与数据构建。

**为什么重写**：这题原先由中央批量生成器 `scripts/build_codeforces_basic_data.py`
产出，那里犯了两处错：① 输入写成 `t` + 括号串，**漏掉题面要求的 n 行**，
按题面读的正解直接 Runtime Error；② 括号串长度随机、左右不等，违反题面
「n 为偶数、左右各 n/2」的保证。一次修补补上了 n 行与均衡串，但答案仍是
`removed + opened` —— 在均衡串上它恒等于 `2 × removed`，而答案就是 `removed`
（`")("` 应为 1，它给 2）。所以这题摘出中央生成器，改走单题流水线。

题面的输入契约（`INPUT_DOMAIN` 是逐字原话）：`1 ≤ t ≤ 2000`、`2 ≤ n ≤ 50`、
n 为偶数、串里左右括号各 n/2。`valid()` 是同一条契约的反向校验。

`SHAPES` 摆的是这题真会挂人的几种形状：
  · `regular`  —— 已经是合法序列，答案 0；
  · `worst`    —— `")))((("` 这种，答案取到上界 n/2，
       把「答案是 removed + opened」这种把结果翻倍的写法钉死；
  · `one_swap` —— 只错一处，答案 1，区分「数失配右括号」与「数所有不匹配括号」；
  · `shortest` —— n = 2 的两种串（`"()"` 与 `")("`）；
  · `longest`  —— n = 50，题面长度上界；
  · `many_tests` —— **一组里放很多个测试用例**（含 t = 2000 的上界），
       整批 Codeforces 数据此前 t 恒为 1，多测试组这条路根本没被走过。
"""
from __future__ import annotations
import random

PROBLEM = "1374C"
INPUT_DOMAIN = "1 ≤ t ≤ 2000；2 ≤ n ≤ 50，n 为偶数；串由 n/2 个 '(' 与 n/2 个 ')' 组成"
LABEL = "first line t (1..2000), then per test a line n (even, 2..50) and a line s"
INVALID = "1\n3\n(()\n"                # n 是奇数，且左右括号不等
SAMPLE = "4\n2\n)(\n4\n()()\n8\n())()(()\n10\n)))((((())\n"   # 题面样例：1 0 1 3
SHAPES = ("worst", "one_swap", "regular", "shortest", "longest", "many_tests", "plain")


def _string(r, shape):
    if shape == "regular":
        pairs = r.randint(1, 25)
        text = ""
        for _ in range(pairs):
            text = "(" + text + ")" if r.randrange(2) and text else text + "()"
        return text[:50] if len(text) <= 50 else "()" * 25
    if shape == "worst":
        pairs = r.randint(1, 25)
        return ")" * pairs + "(" * pairs
    if shape == "one_swap":
        pairs = r.randint(2, 25)
        chars = list("()" * pairs)
        index = 2 * r.randrange(pairs)
        chars[index], chars[index + 1] = chars[index + 1], chars[index]
        return "".join(chars)
    if shape == "shortest":
        return r.choice(("()", ")("))
    if shape == "longest":
        chars = list("(" * 25 + ")" * 25)
        r.shuffle(chars)
        return "".join(chars)
    pairs = r.randint(1, 25)
    chars = list("(" * pairs + ")" * pairs)
    r.shuffle(chars)
    return "".join(chars)


def generate(problem, seed, attempt=0):
    """固定种子；`attempt` 只在两组撞车时递增，撞车不改形状、只换随机数。"""
    if problem != PROBLEM:
        raise KeyError(problem)
    r = random.Random(1374_0003 * 1_000_003 + seed * 9_176 + attempt)
    shape = SHAPES[(seed - 1) % len(SHAPES)]
    if shape == "many_tests":
        # seed 6 走 t 的上界 2000，其余几轮放中等规模的多测试组。
        count = 2000 if seed == 6 else r.randint(2, 200)
        blocks = [_string(r, r.choice(("plain", "worst", "regular", "one_swap"))) for _ in range(count)]
    elif shape == "shortest":
        # n = 2 只有 "()" 与 ")(" 两种串，单测试组撑不出 21 组互异的输入，
        # 所以这一档放一串长度 2 的用例 —— 边界还是 n = 2，组数随机。
        blocks = [r.choice(("()", ")(")) for _ in range(r.randint(3, 300))]
    else:
        blocks = [_string(r, shape)]
    body = "".join(f"{len(block)}\n{block}\n" for block in blocks)
    return f"{len(blocks)}\n{body}"


def valid(problem, text):
    if problem != PROBLEM:
        raise KeyError(problem)
    lines = text.rstrip("\n").split("\n")
    try:
        count = int(lines[0])
    except (ValueError, IndexError):
        return False
    if not 1 <= count <= 2000 or len(lines) != 1 + 2 * count:
        return False
    for index in range(count):
        try:
            length = int(lines[1 + 2 * index])
        except ValueError:
            return False
        block = lines[2 + 2 * index]
        if not 2 <= length <= 50 or length % 2 or len(block) != length:
            return False
        if set(block) - set("()") or block.count("(") != length // 2:
            return False
    return True


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

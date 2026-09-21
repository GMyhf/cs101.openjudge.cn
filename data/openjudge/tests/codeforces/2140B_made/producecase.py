#!/usr/bin/env python3
"""2140B: validate the t-case protocol as well as each concatenation witness."""
from __future__ import annotations

import random
import subprocess
import sys
from pathlib import Path

# 题面样例逐字。答案不唯一（走 `concat_divisible` 特判），所以只钉输入。
SAMPLE = '6\n8\n42\n1000\n66666\n106344\n9876543\n'
REFERENCE = Path(__file__).with_name("samplecode.py")


def generate(seed: int, attempt: int = 0) -> str:
    r = random.Random(2140_000_003 + seed * 9_176 + attempt)
    # 参考实现改成 y = 2x 的构造之后，x 不再需要收在 100 以内 ——
    # 现在按题面取到上界 10^8，小值、边界值和大值都覆盖。
    count = (1, 2, 3, 10, 20)[(seed - 1) % 5]
    pool = [1, 2, 9, 10, 99, 100, 10 ** 8, 10 ** 8 - 1]
    xs = [r.choice(pool) if r.random() < 0.3 else r.randint(1, 10 ** 8)
          for _ in range(count)]
    return f"{count}\n" + "\n".join(map(str, xs)) + "\n"


def valid(text: str) -> bool:
    tokens = text.split()
    try:
        count, xs = int(tokens[0]), list(map(int, tokens[1:]))
    except (ValueError, IndexError):
        return False
    # 题面：1 <= t <= 10^4，1 <= x <= 10^8。
    return 1 <= count <= 10_000 and len(xs) == count and all(1 <= x <= 10 ** 8 for x in xs)


def oracle(text: str, answer: str) -> bool:
    """答案不唯一，所以按题面**验证**而不是比对：y 在 [1,10^9] 内且 (x+y) | concat(x,y)。

    2026-09-20 之前这里自己在 y < 10^5 里线性扫一个见证再逐字比对 —— 既要求参考实现
    给出同一个 y（多解题不该这样判），又在 x 稍大时根本扫不出解。
    """
    xs = list(map(int, text.split()[1:]))
    ys = [int(token) for token in answer.split()]
    if len(ys) != len(xs):
        return False
    return all(1 <= y <= 10 ** 9 and int(str(x) + str(y)) % (x + y) == 0
               for x, y in zip(xs, ys))


def build():
    out = Path(__file__).with_name("data"); out.mkdir(exist_ok=True)
    cases = [SAMPLE]
    for seed in range(1, 40):
        attempt = 0; case = generate(seed)
        while case in cases:
            attempt += 1; case = generate(seed, attempt)
        cases.append(case)
    for index, case in enumerate(cases):
        if not valid(case):
            raise SystemExit(f"invalid case {index}")
        answer = subprocess.run([sys.executable, str(REFERENCE)], input=case, text=True,
                                capture_output=True, check=True, timeout=30).stdout
        if not oracle(case, answer):
            raise SystemExit(f"oracle rejected the reference answer at case {index}")
        (out / f"{index}.in").write_text(case, encoding="utf-8")
        (out / f"{index}.out").write_text(answer, encoding="utf-8")


if __name__ == "__main__":
    build()

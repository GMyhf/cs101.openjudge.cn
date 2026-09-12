#!/usr/bin/env python3
"""02679 整数的立方和 —— 生成器、输入契约与数据构建。

**这份文件 2026-09-12 重写过。** 旧版是那批中央生成器的副本，没有 `valid()`，
02679 那一段是

    if number == 2679:
        return f"{r.randint(1,10000)}\\n"

而题面（描述）明写 **`1 < k < 10`**。旧数据 21 组里 **20 组的 k 越界**（最大 9982），
实测后果：一份用 `int` 的 C++ 解 —— 在题面范围内完全正确，k≤9 时立方和最大 2025 ——
**Wrong Answer 挂第 2 组**（溢出）；一份把 k=2..9 全查表的解**Runtime Error**。
两份都是照题面写的正确程序。

**这题的合法输入域只有 8 个元素**（k = 2..9），所以「21 组互异数据」根本凑不出来 ——
凑出来的必然越界，这正是旧数据的来路。现在改成**穷举整个合法输入域**：8 组，
第 0 组是题面样例 k=5，其余七组是剩下的 2、3、4、6、7、8、9。穷举比 21 组随机更强：
判别力不是「够不够多」，而是「有没有漏」。
"""
from __future__ import annotations

NUMBER = 2679
INPUT_DOMAIN = "输入只有一行，该行包含一个正整数k；描述里给的范围是 1 < k < 10"
LABEL = "a single line holding one integer k with 1 < k < 10"
INVALID = "10\n"                     # k=10 越过题面的 1 < k < 10
SAMPLE = "5\n"
SAMPLE_OUT = "225\n"                 # 题面「样例输出」逐字

LEGAL = tuple(range(2, 10))          # 题面允许的全部 k
ORDER = (5,) + tuple(k for k in LEGAL if k != 5)     # 第 0 组必须是题面样例


def generate(number, seed):
    """seed 从 1 数到 len(ORDER)-1，各对应一个还没用过的合法 k。"""
    if number != NUMBER:
        raise KeyError(number)
    if not 1 <= seed < len(ORDER):
        raise KeyError(seed)
    return f"{ORDER[seed]}\n"


def valid(number, text):
    """输入契约：一行、一个整数、`1 < k < 10`。**旧生成器缺的就是这个函数。**"""
    if number != NUMBER:
        raise KeyError(number)
    if not text.endswith("\n"):
        return False
    lines = text.rstrip("\n").split("\n")
    if len(lines) != 1:
        return False
    token = lines[0].strip()
    if not token.isdigit():
        return False
    return 1 < int(token) < 10


import subprocess as _subprocess
from pathlib import Path as _Path
REFERENCE = _Path(__file__).with_name("samplecode.py")
LANGUAGE = "Python3"


def _build():
    out = _Path(__file__).with_name("data")
    out.mkdir(exist_ok=True)
    for stale in out.glob("*"):
        stale.unlink()
    cases = [SAMPLE] + [generate(NUMBER, seed) for seed in range(1, len(ORDER))]
    if len(set(cases)) != len(cases):
        raise SystemExit("两组输入撞了，数据必须互异")
    if {int(case) for case in cases} != set(LEGAL):
        raise SystemExit("没有穷举完整个合法输入域")
    for index, case in enumerate(cases):
        if not valid(NUMBER, case):
            raise SystemExit(f"case {index} violates the input contract: {case!r}")
        result = _subprocess.run(["python3", str(REFERENCE)], input=case, text=True,
                                 capture_output=True, timeout=60, check=True)
        if index == 0 and result.stdout != SAMPLE_OUT:
            raise SystemExit(f"第 0 组与题面样例输出不符：{result.stdout!r} != {SAMPLE_OUT!r}")
        (out / f"{index}.in").write_text(case, encoding="utf-8")
        (out / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    _build()

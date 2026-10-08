#!/usr/bin/env python3
"""31296 “淹园”救援 —— 生成器、输入契约与数据构建。

第 0、1 组是题面的两组样例。形状按错法排：

  · `exact`     —— 大量「两人体重之和恰好等于 C」的配对：把 `<= C` 写成 `< C` 的会多用船。
  · `adjacent`  —— 排序后「相邻两人能坐就一起坐」的贪心在这里错：轻的两两凑掉以后，
                   重的只能各坐一艘（正解是一轻一重配对）。
  · `full`      —— 所有人体重都等于 C：每人一艘。
  · `half`      —— C 为奇数、所有人体重都是 (C+1)/2：两两都超载，答案 n。
  · `unit`      —— C=1、所有人体重 1：同上，且是题面取值下界。
  · `odd`       —— n 为奇数、能两两配对：最后剩一人单走，双指针 `i < j` / `i <= j` 写错的漏这一人。
  · `random` / `big` —— 随机规模与题面上界 n=10^5、C=10^9。
"""
import random

NUMBER = 31296
INPUT_DOMAIN = "第一行包含两个整数 n, C（1 <= n <= 10^5，1 <= C <= 10^9）；第二行包含 n 个整数 w_1..w_n（1 <= w_i <= C）"
SAMPLES = [
    ("4 5\n3 2 2 1\n", "2\n"),
    ("5 3\n3 2 2 1 1\n", "3\n"),
]
MAX_N = 10 ** 5
MAX_C = 10 ** 9
SHAPES = ("exact", "adjacent", "random", "odd", "full", "half", "unit", "big", "exact", "adjacent", "random")


def render(cap, weights):
    return f"{len(weights)} {cap}\n" + " ".join(map(str, weights)) + "\n"


def generate(number, seed):
    rng = random.Random(number * 1000 + seed)
    shape = SHAPES[(seed - 1) % len(SHAPES)]
    if shape == "exact":
        cap = rng.randint(2, MAX_C)
        weights = []
        for _ in range(rng.randint(1, 20000)):
            a = rng.randint(1, cap - 1)
            weights += [a, cap - a]
        weights += [rng.randint(1, cap) for _ in range(rng.randint(0, 50))]
        rng.shuffle(weights)
        return render(cap, weights)
    if shape == "adjacent":
        # 轻的一半体重在 [1, C/4]，重的一半在 [3C/4 - 轻的, ...]：一轻一重恰好能配，
        # 两个重的不能配；先把轻的两两凑掉的写法会让重的人各坐一艘。
        cap = rng.randint(1000, MAX_C)
        half = rng.randint(1, 30000)
        light = [rng.randint(1, cap // 4) for _ in range(half)]
        heavy = [cap - x for x in light]
        weights = light + heavy
        rng.shuffle(weights)
        return render(cap, weights)
    if shape == "full":
        cap = rng.randint(1, MAX_C)
        return render(cap, [cap] * rng.randint(1, 5000))
    if shape == "half":
        cap = 2 * rng.randint(1, MAX_C // 2 - 1) + 1
        return render(cap, [(cap + 1) // 2] * rng.randint(2, 5000))
    if shape == "unit":
        return render(1, [1] * rng.randint(1, 1000))
    if shape == "odd":
        cap = rng.randint(10, 10 ** 6)
        weights = [rng.randint(1, cap // 2) for _ in range(2 * rng.randint(1, 5000) + 1)]
        return render(cap, weights)
    if shape == "big":
        cap = MAX_C - rng.randint(0, 1000)
        return render(cap, [rng.randint(1, cap) for _ in range(MAX_N - seed % 2)])
    cap = rng.randint(1, 10 ** rng.randint(1, 9))
    return render(cap, [rng.randint(1, cap) for _ in range(rng.randint(1, 30000))])


def valid(text):
    """照题面：第一行 n（1..10^5）与 C（1..10^9），第二行恰 n 个整数 w_i（1 <= w_i <= C）。"""
    lines = _lines(text)
    if lines is None or len(lines) != 2:
        return "应为 2 行且以换行结尾"
    head = _ints(lines[0])
    if not head or len(head) != 2:
        return "第一行应为 n C"
    n, cap = head
    if not 1 <= n <= MAX_N or not 1 <= cap <= MAX_C:
        return f"n={n} 或 C={cap} 越界"
    weights = _ints(lines[1])
    if weights is None or len(weights) != n:
        return "第二行个数与 n 不符"
    if not all(1 <= w <= cap for w in weights):
        return "w_i 越出 1..C（题面保证体重不超过载重上限）"
    return True


def _ints(line):
    parts = line.split(" ")
    for part in parts:
        body = part[1:] if part.startswith("-") else part
        if not body.isdigit() or (len(body) > 1 and body[0] == "0") or part == "-0":
            return None
    return [int(part) for part in parts]


def _lines(text):
    if not text.endswith("\n") or "\r" in text:
        return None
    return text[:-1].split("\n")


import subprocess as _subprocess
from pathlib import Path as _Path
REFERENCE = _Path(__file__).with_name("samplecode.py")
TOTAL = 40


def _build():
    out = _Path(__file__).with_name("data")
    out.mkdir(exist_ok=True)
    cases = [text for text, _answer in SAMPLES]
    cases += [generate(NUMBER, seed) for seed in range(1, TOTAL - len(SAMPLES) + 1)]
    if len(set(cases)) != len(cases):
        raise SystemExit("两组输入撞了，数据必须互异")
    for index, case in enumerate(cases):
        if valid(case) is not True:
            raise SystemExit(f"case {index} violates the input contract: {valid(case)}")
        result = _subprocess.run(["python3", str(REFERENCE)], input=case, text=True,
                                 capture_output=True, timeout=120, check=True)
        if index < len(SAMPLES) and result.stdout != SAMPLES[index][1]:
            raise SystemExit(f"第 {index} 组与题面样例输出不符：{result.stdout!r} != {SAMPLES[index][1]!r}")
        (out / f"{index}.in").write_text(case, encoding="utf-8")
        (out / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    _build()

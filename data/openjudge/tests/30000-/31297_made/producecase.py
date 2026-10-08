#!/usr/bin/env python3
"""31297 恒星共振裂变 —— 生成器、输入契约与数据构建。

第 0 组是题面样例。答案是最接近 N/2 的那组质数对，形状按错法排：

  · `max_n`      —— 大量 N 贴着上界 10^6：只筛到 N/2、或筛到 10^6 少一位的写法会把
                    p2 判成合数而越过正确答案。
  · `half_prime` —— N/2 本身是质数（答案 p p）：从 N/2 - 1 开始找的会错过。
  · `small`      —— N=4、6、8… 的小值：N=4 的答案是 2 2，把 2 当特例跳过或从 3 开始的会挂。
  · `gap`        —— N/2 附近质数间隔大的 N：检验确实是从中间往外找，而不是找到任意一组。
  · `full`       —— T 取到题面上界 10^4、N 在全范围随机：逐个 N 试除判质数的 O(T·N·√N) 写法超时。
  · `random`     —— 中等规模随机。
"""
import random

NUMBER = 31297
INPUT_DOMAIN = "第一行包含一个正整数 T（1 <= T <= 10^4）；接下来 T 行，每行包含一个偶数 N（4 <= N <= 10^6）"
SAMPLES = [
    ("3\n4\n10\n16\n", "2 2\n5 5\n5 11\n"),
]
MAX_T = 10 ** 4
MAX_N = 10 ** 6
SHAPES = ("max_n", "half_prime", "small", "gap", "full", "random")


def _primes(limit):
    sieve = bytearray([1]) * (limit + 1)
    sieve[0] = sieve[1] = 0
    for p in range(2, int(limit ** 0.5) + 1):
        if sieve[p]:
            sieve[p * p::p] = bytes(len(range(p * p, limit + 1, p)))
    return sieve


SIEVE = _primes(MAX_N)


def render(values):
    return f"{len(values)}\n" + "".join(f"{n}\n" for n in values)


def generate(number, seed):
    rng = random.Random(number * 1000 + seed)
    shape = SHAPES[(seed - 1) % len(SHAPES)]
    if shape == "max_n":
        values = [MAX_N - 2 * rng.randint(0, 500) for _ in range(rng.randint(100, MAX_T))]
    elif shape == "half_prime":
        values, target = [], rng.randint(50, 3000)
        while len(values) < target:
            p = rng.randint(2, MAX_N // 2)
            if SIEVE[p]:
                values.append(2 * p)
    elif shape == "small":
        values = list(range(4, 4 + 2 * rng.randint(20, 300), 2))
        rng.shuffle(values)
    elif shape == "gap":
        # N = p + q，p < q 是间隔 >= 50 的相邻质数：N/2 落在空档中间，答案恰是 p q
        values = []
        prev = None
        for p in range(MAX_N // 2, 2, -1):
            if SIEVE[p]:
                if prev is not None and prev - p >= 50:
                    values.append(p + prev)
                prev = p
        rng.shuffle(values)
        values = values[:rng.randint(100, len(values))]
    elif shape == "full":
        values = [2 * rng.randint(2, MAX_N // 2) for _ in range(MAX_T)]
    else:
        values = [2 * rng.randint(2, 10 ** rng.randint(1, 6) // 2) for _ in range(rng.randint(1, 3000))]
    return render(values)


def valid(text):
    """照题面：第一行 T（1..10^4），接下来恰 T 行，每行一个偶数 N（4..10^6）。"""
    lines = _lines(text)
    if lines is None:
        return "须以换行结尾"
    head = _ints(lines[0])
    if not head or len(head) != 1 or not 1 <= head[0] <= MAX_T:
        return f"T 越出 1..{MAX_T}"
    if len(lines) != head[0] + 1:
        return "行数与 T 不符"
    for line in lines[1:]:
        value = _ints(line)
        if not value or len(value) != 1 or value[0] % 2 or not 4 <= value[0] <= MAX_N:
            return f"N 不是 4..10^6 的偶数：{line!r}"
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

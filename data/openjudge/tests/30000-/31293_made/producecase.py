#!/usr/bin/env python3
"""31293 双十一凑单大作战 —— 生成器、输入契约与数据构建。

第 0、1 组是题面的两组样例（`_build()` 里逐字对样例输出）。其余 38 组按「这题会怎么错」
排形状，不是撒随机：

  · `tiny`        —— n=1、2、3 等极小规模：n<3 时一组也凑不成，写死「每 3 件免一件」
                     却不判边界的会越界或多免。
  · `ascending`   —— 输入本来就升序：不排序、按输入顺序三个一组的写法在这里免得最少。
  · `asc_trap`    —— 排序方向反了（从最便宜的开始三个一组，免掉 p[0], p[3], …）的写法
                     在价格差距大的数据上明显偏多；这里让价格跨好几个数量级。
  · `dup`         —— 大量相等价格：免单额并列，检验「最低的一件」取等的处理。
  · `mod`         —— n 分别取 3k、3k+1、3k+2，检验尾巴不足 3 件时不免单。
  · `big`         —— n 取到题面上界 10^5、价格取到 10^9，答案约 6.7×10^13，
                     超出 32 位整数（题面原话「答案可能超过 32 位有符号整数范围」）。
"""
import random

NUMBER = 31293
INPUT_DOMAIN = "第一行包含一个整数 n（1 <= n <= 10^5）；第二行包含 n 个整数 p_1..p_n（1 <= p_i <= 10^9）"
SAMPLES = [
    ("4\n3 2 1 10\n", "14\n"),
    ("7\n6 5 5 5 2 1 1\n", "19\n"),
]
MAX_N = 10 ** 5
MAX_P = 10 ** 9
SHAPES = ("tiny", "ascending", "asc_trap", "dup", "mod", "random", "big")


def render(prices):
    return f"{len(prices)}\n" + " ".join(map(str, prices)) + "\n"


def generate(number, seed):
    rng = random.Random(number * 1000 + seed)
    shape = SHAPES[(seed - 1) % len(SHAPES)]
    if shape == "tiny":
        n = (1, 2, 3, 5, 6, 4)[(seed - 1) // len(SHAPES) % 6]
        return render([rng.randint(1, 20) for _ in range(n)])
    if shape == "ascending":
        n = rng.randint(10, 3000)
        return render(sorted(rng.randint(1, 10 ** rng.randint(2, 9)) for _ in range(n)))
    if shape == "asc_trap":
        n = rng.randint(30, 5000)
        prices = [rng.randint(1, 10 ** rng.randint(0, 9)) for _ in range(n)]
        rng.shuffle(prices)
        return render(prices)
    if shape == "dup":
        n = rng.randint(50, 20000)
        pool = [rng.randint(1, MAX_P) for _ in range(rng.randint(1, 4))]
        return render([rng.choice(pool) for _ in range(n)])
    if shape == "mod":
        n = 3 * rng.randint(3, 2000) + (seed // len(SHAPES)) % 3
        return render([rng.randint(1, 1000) for _ in range(n)])
    if shape == "random":
        n = rng.randint(100, 50000)
        return render([rng.randint(1, MAX_P) for _ in range(n)])
    n = MAX_N - (seed // len(SHAPES)) % 3
    return render([rng.randint(MAX_P // 2, MAX_P) for _ in range(n)])


def valid(text):
    """照题面：第一行 n（1..10^5），第二行恰 n 个整数（1..10^9），单空格分隔。"""
    lines = _lines(text)
    if lines is None or len(lines) != 2:
        return "应为 2 行且以换行结尾"
    head = _ints(lines[0])
    if not head or len(head) != 1 or not 1 <= head[0] <= MAX_N:
        return f"n 越出 1..{MAX_N}"
    prices = _ints(lines[1])
    if prices is None or len(prices) != head[0]:
        return "第二行个数与 n 不符"
    if not all(1 <= p <= MAX_P for p in prices):
        return "p_i 越出 1..10^9"
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

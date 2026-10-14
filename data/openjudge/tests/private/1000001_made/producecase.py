#!/usr/bin/env python3
"""1000001 筛选法建最小堆的交换次数：确定性测试数据生成器。"""
import random
import subprocess
from pathlib import Path

NUMBER = 1000001
SAMPLES = [("10\n38 64 52 15 73 40 48 55 26 12\n", "6\n")]
TOTAL = 21


def render(values):
    return f"{len(values)}\n{' '.join(map(str, values))}\n"


def generate(number, seed):
    rng = random.Random(number * 1000 + seed)
    if seed == 1:
        values = list(range(1, 11))
        values.reverse()
    elif seed == 2:
        values = list(range(1, 16))
        rng.shuffle(values)
    elif seed == 3:
        values = [rng.randint(-10**9, 10**9) for _ in range(7)]
        while len(set(values)) != len(values):
            values = [rng.randint(-10**9, 10**9) for _ in range(7)]
    else:
        n = rng.randint(1, 100)
        values = rng.sample(range(-10000, 10001), n)
        if seed % 4 == 0:
            values.sort()
        elif seed % 4 == 1:
            values.sort(reverse=True)
    return render(values)


def valid(text):
    fields = text.split()
    if not fields:
        return "输入为空"
    n = int(fields[0])
    if not 1 <= n <= 100 or len(fields) != n + 1:
        return "n 或元素个数越界"
    values = list(map(int, fields[1:]))
    if len(set(values)) != n or any(abs(x) > 10**9 for x in values):
        return "元素不满足约束"
    return True


def _build():
    root = Path(__file__).parent
    data_dir = root / "data"
    data_dir.mkdir(exist_ok=True)
    cases = [text for text, _ in SAMPLES] + [generate(NUMBER, i) for i in range(1, TOTAL)]
    reference = root / "samplecode.py"
    for index, case in enumerate(cases):
        if valid(case) is not True:
            raise SystemExit(f"case {index}: {valid(case)}")
        result = subprocess.run(["python3", str(reference)], input=case, text=True,
                                capture_output=True, check=True).stdout
        if index < len(SAMPLES) and result != SAMPLES[index][1]:
            raise SystemExit(f"sample output mismatch: {result!r}")
        (data_dir / f"{index}.in").write_text(case, encoding="utf-8")
        (data_dir / f"{index}.out").write_text(result, encoding="utf-8")


if __name__ == "__main__":
    _build()

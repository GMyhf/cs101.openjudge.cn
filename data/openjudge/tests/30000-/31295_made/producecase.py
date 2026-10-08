#!/usr/bin/env python3
"""31295 宿舍的空调 —— 生成器、输入契约与数据构建。

第 0、1 组是题面的两组样例。答案是 max l（若 max l <= min r）否则 -1，形状按错法排：

  · `minus_one_ok` —— 交集非空且最低温度恰好是 -1：输出和「无解」长得一样，
                      用 -1 当哨兵、判「答案是不是 -1」再分支的写法会走错路。
  · `all_negative` —— 所有 l、r 都是负数：max l 初值写成 0 的写法会输出 0。
  · `touch`        —— max l == min r，交集只有一个点：比较写成严格小于的会判成无解。
  · `just_miss`    —— max l == min r + 1，差一度无解。
  · `extreme`      —— l、r 取到 ±10^9 的边界；初值用 ±10^9 以内哨兵的写法会错。
  · `single`       —— n=1。
  · `big_yes` / `big_no` —— n 取到题面上界 10^5。
"""
import random

NUMBER = 31295
INPUT_DOMAIN = "第一行包含一个整数 n（1 <= n <= 10^5）；接下来 n 行，每行两个整数 l_i, r_i（-10^9 <= l_i <= r_i <= 10^9）"
SAMPLES = [
    ("3\n18 25\n20 30\n16 22\n", "20\n"),
    ("2\n-5 0\n1 6\n", "-1\n"),
]
MAX_N = 10 ** 5
LIMIT = 10 ** 9
SHAPES = ("minus_one_ok", "all_negative", "touch", "just_miss", "extreme", "single",
          "random_yes", "random_no", "big_yes", "big_no")


def render(pairs):
    return f"{len(pairs)}\n" + "".join(f"{l} {r}\n" for l, r in pairs)


def around(rng, n, low, high, spread):
    """造 n 个都包含 [low, high] 的区间，并保证至少一个左端点恰是 low、一个右端点恰是 high。"""
    pairs = [[max(-LIMIT, low - rng.randint(0, spread)), min(LIMIT, high + rng.randint(0, spread))]
             for _ in range(n)]
    pairs[rng.randrange(n)][0] = low
    pairs[rng.randrange(n)][1] = high
    return [tuple(pair) for pair in pairs]


def generate(number, seed):
    rng = random.Random(number * 1000 + seed)
    shape = SHAPES[(seed - 1) % len(SHAPES)]
    if shape == "minus_one_ok":
        return render(around(rng, rng.randint(2, 2000), -1, rng.randint(-1, 50), 10 ** rng.randint(1, 9)))
    if shape == "all_negative":
        high = -rng.randint(1, 10 ** 6)
        low = high - rng.randint(0, 1000)
        pairs = around(rng, rng.randint(2, 3000), low, high, 10 ** 5)
        return render([(l, min(r, -1)) for l, r in pairs])
    if shape == "touch":
        x = rng.randint(-LIMIT, LIMIT)
        return render(around(rng, rng.randint(2, 5000), x, x, 10 ** rng.randint(1, 9)))
    if shape == "just_miss":
        x = rng.randint(-10 ** 6, 10 ** 6)
        pairs = around(rng, rng.randint(2, 5000), x, x + 1, 10 ** 4)
        pairs += [(x + 1, x + 1 + rng.randint(0, 9)), (x - rng.randint(0, 9), x)]
        rng.shuffle(pairs)
        return render(pairs)
    if shape == "extreme":
        if seed % 2:
            return render(around(rng, rng.randint(2, 100), -LIMIT, -LIMIT + rng.randint(0, 5), 0)
                          + [(-LIMIT, LIMIT)])
        return render(around(rng, rng.randint(2, 100), LIMIT - rng.randint(0, 5), LIMIT, 10))
    if shape == "single":
        l = rng.randint(-LIMIT, LIMIT)
        return render([(l, rng.randint(l, LIMIT))])
    if shape in ("random_yes", "big_yes"):
        n = MAX_N if shape == "big_yes" else rng.randint(10, 20000)
        low = rng.randint(-LIMIT // 2, LIMIT // 2)
        return render(around(rng, n, low, low + rng.randint(0, 10 ** 6), 10 ** 8))
    n = MAX_N if shape == "big_no" else rng.randint(10, 20000)
    low = rng.randint(-LIMIT // 2, LIMIT // 2)
    # 再加一个整段落在 max l 左边的区间，交集必空
    pairs = around(rng, n - 1, low, low + rng.randint(0, 10 ** 6), 10 ** 8)
    pairs.append((low - 10 ** 8 - 5, low - 1 - rng.randint(0, 3)))
    rng.shuffle(pairs)
    return render(pairs)


def valid(text):
    """照题面：第一行 n（1..10^5），接下来恰 n 行，每行两个整数 l, r，-10^9 <= l <= r <= 10^9。"""
    lines = _lines(text)
    if lines is None:
        return "须以换行结尾"
    head = _ints(lines[0])
    if not head or len(head) != 1 or not 1 <= head[0] <= MAX_N:
        return f"n 越出 1..{MAX_N}"
    if len(lines) != head[0] + 1:
        return "行数与 n 不符"
    for line in lines[1:]:
        pair = _ints(line)
        if pair is None or len(pair) != 2:
            return f"区间行格式不对：{line!r}"
        if not -LIMIT <= pair[0] <= pair[1] <= LIMIT:
            return f"区间越界或 l > r：{line!r}"
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

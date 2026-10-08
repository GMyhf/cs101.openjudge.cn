#!/usr/bin/env python3
"""31294 大肥鱼卖白饭 —— 生成器、输入契约与数据构建。

第 0、1 组是题面的两组样例。随机撒 5/10/20 几乎一开头就找不开，答案全是 NO，
判不出任何错法，所以这里先**按正确贪心模拟着造一条能找开的序列**，再按形状决定
要不要在某个位置故意放一张找不开的钞票：

  · `greedy_trap` —— 手里同时有 10 元和至少 3 张 5 元时来 20 元：先付 5+5+5 的写法
                     会把 5 元花光，后面的 10 元顾客就找不开（正确答案 YES、错法 NO）。
  · `fail_late`   —— 前面全能找开，到很靠后才第一次找不开：检验「出错就该停」以及
                     只看最后状态、计数被减成负数还继续跑的写法。
  · `fail_first`  —— 第一位就付 10 或 20 元（开张时没零钱）。
  · `all_five`    —— 全是 5 元，必然 YES。
  · `yes_long` / `no_long` —— n 取到题面上界 10^5 的长序列，分别以 YES、NO 收尾。
  · `tiny`        —— n=1..3 的极小规模。
"""
import random

NUMBER = 31294
INPUT_DOMAIN = "第一行包含一个整数 n（1 <= n <= 10^5）；第二行包含 n 个整数 a_1..a_n（a_i 属于 {5,10,20}）"
SAMPLES = [
    ("5\n5 5 10 5 20\n", "YES\n"),
    ("4\n5 10 20 5\n", "NO\n"),
]
MAX_N = 10 ** 5
SHAPES = ("greedy_trap", "fail_late", "yes_long", "tiny", "greedy_trap", "no_long",
          "fail_first", "all_five", "fail_late")


def render(bills):
    return f"{len(bills)}\n" + " ".join(map(str, bills)) + "\n"


def feasible_walk(rng, n, weights, trap_rate=0.0):
    """按正确贪心模拟，只挑当前能找开的钞票，造一条 YES 序列。"""
    five = ten = 0
    bills = []
    while len(bills) < n:
        if trap_rate and ten >= 1 and five >= 3 and rng.random() < trap_rate and len(bills) + five + 1 <= n:
            # 20 元：正解付 10+5，剩 five-1 张 5 元；接着来 five-1+... 个 10 元，
            # 每个都要一张 5 元。错法付 5+5+5 后只剩 five-3 张，必在这里断。
            bills.append(20)
            ten -= 1
            five -= 1
            for _ in range(five):
                bills.append(10)
                ten += 1
            five = 0
            continue
        options = [5]
        if five >= 1:
            options.append(10)
        if (ten >= 1 and five >= 1) or five >= 3:
            options.append(20)
        bill = rng.choices(options, [weights[{5: 0, 10: 1, 20: 2}[b]] for b in options])[0]
        bills.append(bill)
        if bill == 5:
            five += 1
        elif bill == 10:
            five -= 1
            ten += 1
        elif ten >= 1 and five >= 1:
            ten -= 1
            five -= 1
        else:
            five -= 3
    return bills[:n], (five, ten)


def break_at_end(bills, state):
    """在末尾补一张当前找不开的钞票（若来得及）。"""
    five, ten = state
    if five == 0:
        return bills + [10]
    if not (ten >= 1 and five >= 1) and five < 3:
        return bills + [20]
    return bills + [10] * five + [10]


def generate(number, seed):
    rng = random.Random(number * 1000 + seed)
    shape = SHAPES[(seed - 1) % len(SHAPES)]
    if shape == "tiny":
        n = rng.randint(1, 3)
        return render([rng.choice((5, 10, 20)) for _ in range(n)])
    if shape == "all_five":
        return render([5] * rng.randint(1, MAX_N))
    if shape == "fail_first":
        rest, _ = feasible_walk(rng, rng.randint(0, 2000), (5, 3, 2))
        return render([rng.choice((10, 20))] + rest)
    if shape == "greedy_trap":
        bills, _ = feasible_walk(rng, rng.randint(20, 20000), (5, 3, 2), trap_rate=0.3)
        return render(bills)
    if shape == "yes_long":
        bills, _ = feasible_walk(rng, MAX_N - seed, (4, 3, 2), trap_rate=0.05)
        return render(bills)
    if shape == "no_long":
        bills, state = feasible_walk(rng, MAX_N - 200 - seed, (4, 3, 2), trap_rate=0.05)
        bills = break_at_end(bills, state)
        bills += [rng.choice((5, 10, 20)) for _ in range(MAX_N - len(bills))]
        return render(bills)
    # fail_late：前面全能找开，靠后的位置第一次断，断点后再接一段随机钞票
    bills, state = feasible_walk(rng, rng.randint(50, 30000), (5, 3, 2), trap_rate=0.1)
    bills = break_at_end(bills, state)
    bills += [rng.choice((5, 5, 5, 10, 20)) for _ in range(rng.randint(0, 500))]
    return render(bills[:MAX_N])


def valid(text):
    """照题面：第一行 n（1..10^5），第二行恰 n 个取自 {5,10,20} 的整数。"""
    lines = _lines(text)
    if lines is None or len(lines) != 2:
        return "应为 2 行且以换行结尾"
    head = _ints(lines[0])
    if not head or len(head) != 1 or not 1 <= head[0] <= MAX_N:
        return f"n 越出 1..{MAX_N}"
    bills = _ints(lines[1])
    if bills is None or len(bills) != head[0]:
        return "第二行个数与 n 不符"
    if not set(bills) <= {5, 10, 20}:
        return "面额不在 {5,10,20} 内"
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

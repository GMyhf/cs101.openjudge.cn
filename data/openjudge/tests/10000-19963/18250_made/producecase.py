#!/usr/bin/env python3
"""18250 冰阔落 I —— 生成器、输入契约与数据构建。

2026-09-17 重写。旧生成器用无种子 `random`、只产 10 组、第 0 组不是题面样例，
重跑拿到的是另一批数据（见 collab/regression-sweep-2026-07-25-report.json）。

题面：多组数据、少于 5 组，读到 EOF；每组 `n m`（n, m<=50000），接着 m 行 `x y`
（1<=x, y<=n）。x、y 已同杯输出 Yes，否则把 y 所在杯倒进 x 所在杯、输出 No；
最后输出剩下有阔落的杯子数与编号（升序）。

`SHAPES` 按「这题会怎么错」排：
  · `direction_trap` —— 反复把小编号倒进大编号，合并方向写反（留 y 的根）的解法
        最后剩下的杯子编号全错。
  · `self_pour`      —— 大量 x==y 与同杯重复操作，必须输出 Yes 且不能改变任何东西。
  · `all_merge`      —— 全部倒进一杯，结果只剩 1 杯。
  · `untouched`      —— n 远大于 m 涉及的杯子，没被碰过的杯子都要列出来。
  · `tiny`           —— n=1。
  · `multi_eof`      —— 4 份数据，只读一份或不读到 EOF 的挂（其他形状也是 1..4 份）。
  · `upper_bound`    —— n=m=50000，压一下不做路径压缩的写法。
随机树的深度不刻意压到上万：平台原数据未知，递归 find 的正解在平台上能过就不在这里卡它。

答案由 `samplecode.py` 产出，构建时再用完全不同的朴素模拟（逐杯记录内容、真的把列表
倒过去）逐组复核。
"""
from __future__ import annotations
import random
import subprocess
from pathlib import Path

NUMBER = 18250
REFERENCE = Path(__file__).with_name("samplecode.py")
INPUT_DOMAIN = "有多组测试数据，少于 5 组。每组测试数据，第一行两个整数 n, m (n, m<=50000)。接下来 m 行，每行两个整数 x, y (1<=x, y<=n)。"
SAMPLE = "3 2\n1 2\n2 1\n4 2\n1 2\n4 3\n"
SAMPLE_OUT = "No\nYes\n2\n1 3 \nNo\nNo\n2\n1 4\n"      # 题面「样例输出」逐字（含原站行尾空格）
MAX_N = MAX_M = 50000
SHAPES = ("direction_trap", "self_pour", "all_merge", "untouched", "tiny",
          "multi_eof", "upper_bound")


def _group(r, shape):
    if shape == "tiny":
        n = 1; ops = [(1, 1)] * r.randint(1, 5)
    elif shape == "direction_trap":
        n = r.randint(20, 3000); ops = []
        for _ in range(r.randint(n // 2, n)):
            a, b = sorted(r.sample(range(1, n + 1), 2)); ops.append((b, a))
    elif shape == "self_pour":
        n = r.randint(5, 2000); ops = []
        for _ in range(r.randint(n, 2 * n)):
            x = r.randint(1, n); ops.append((x, x) if r.random() < 0.5 else (x, r.randint(1, min(n, x + 2))))
    elif shape == "all_merge":
        n = r.randint(2, 2000); order = list(range(1, n + 1)); r.shuffle(order)
        ops = [(order[r.randrange(i)], order[i]) for i in range(1, n)]
        ops += [(r.randint(1, n), r.randint(1, n)) for _ in range(r.randint(1, 50))]
        r.shuffle(ops)
    elif shape == "untouched":
        n = r.randint(1000, 5000); pool = r.sample(range(1, n + 1), 30)
        ops = [(r.choice(pool), r.choice(pool)) for _ in range(r.randint(10, 60))]
    else:  # upper_bound
        n = MAX_N; ops = [(r.randint(1, n), r.randint(1, n)) for _ in range(MAX_M)]
    return f"{n} {len(ops)}\n" + "".join(f"{x} {y}\n" for x, y in ops)


def generate(number, seed):
    assert number == NUMBER
    r = random.Random(number * 1_000_003 + seed)
    # seed 1..20：前 14 组轮流用前五种形状（各组 1..4 份），multi_eof 与 upper_bound 各 3 组
    if seed <= 14:
        shape = SHAPES[(seed - 1) % 5]
        return "".join(_group(r, shape) for _ in range(r.randint(1, 4)))
    if seed <= 17:  # multi_eof：4 份，形状混排
        return "".join(_group(r, SHAPES[r.randrange(5)]) for _ in range(4))
    count = 1 if seed == 18 else 2 if seed == 19 else 4
    return "".join(_group(r, "upper_bound") for _ in range(count))


def valid(number, text):
    tokens = text.split()
    if not text.endswith("\n") or not tokens:
        return False
    p = groups = 0
    while p < len(tokens):
        n, m = int(tokens[p]), int(tokens[p + 1]); p += 2
        if not (1 <= n <= MAX_N and 1 <= m <= MAX_M) or p + 2 * m > len(tokens):
            return False
        if not all(1 <= int(v) <= n for v in tokens[p:p + 2 * m]):
            return False
        p += 2 * m; groups += 1
    lines = text.split("\n")[:-1]
    return 1 <= groups < 5 and all(len(line.split()) == 2 for line in lines)


def _oracle(text):
    """朴素模拟：members[b] 是容器 b 里的原始编号，box[i] 是 i 所在容器，cup[b] 是容器的杯号。

    不用并查集：倒的时候真把编号搬过去（少的那边搬进多的那边），杯号取 x 所在的杯。
    """
    tokens, p, out = list(map(int, text.split())), 0, []
    while p < len(tokens):
        n, m = tokens[p], tokens[p + 1]; p += 2
        members = {i: [i] for i in range(1, n + 1)}; box = list(range(n + 1))
        cup = {i: i for i in range(1, n + 1)}
        for _ in range(m):
            x, y = tokens[p], tokens[p + 1]; p += 2
            if box[x] == box[y]:
                out.append("Yes"); continue
            out.append("No")
            into, poured = box[x], box[y]
            label = cup[into]
            if len(members[into]) < len(members[poured]):
                into, poured = poured, into
            for i in members[poured]: box[i] = into
            members[into] += members.pop(poured); del cup[poured]
            cup[into] = label
        out += [str(len(cup)), " ".join(map(str, sorted(cup.values())))]
    return out


def _build():
    out = Path(__file__).with_name("data")
    out.mkdir(exist_ok=True)
    for path in out.glob("*"):
        path.unlink()
    cases = [SAMPLE] + [generate(NUMBER, seed) for seed in range(1, 21)]
    if len(set(cases)) != len(cases):
        raise SystemExit("两组输入撞了，数据必须互异")
    for index, case in enumerate(cases):
        if not valid(NUMBER, case):
            raise SystemExit(f"case {index} violates the input contract")
        result = subprocess.run(["python3", str(REFERENCE)], input=case, text=True,
                                capture_output=True, timeout=120, check=True)
        if index == 0 and result.stdout.split() != SAMPLE_OUT.split():
            raise SystemExit(f"第 0 组与题面样例输出不符：{result.stdout!r}")
        if _oracle(case) != [line.strip() for line in result.stdout.splitlines()]:
            raise SystemExit(f"case {index}: samplecode 与朴素模拟不一致")
        (out / f"{index}.in").write_text(case, encoding="utf-8")
        (out / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    _build()

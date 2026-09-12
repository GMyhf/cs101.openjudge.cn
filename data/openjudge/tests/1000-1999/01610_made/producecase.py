#!/usr/bin/env python3
"""01610 四分树 —— 生成器、输入契约与数据构建。

**这份文件 2026-09-12 重写过。** 旧版是那批中央生成器的副本（一个 `generate()` 里
塞着七十多道题的形状，没有 `valid()`），其中 01610 那一段把矩阵写成了无分隔的
`10010111`：

    chunks.append(str(n) + "\\n" + "\\n".join(
        "".join(r.choice("01") for _ in range(n)) for _ in range(n)))

题面明写「每两个 0 和 1 之间**至少有一个空格**」。参考实现按 `input().split()` 读，
于是把一整行读成单个整数 `10010111`，21 组 `.out` 全是乱码
（`1.out` 是 `64924924924020408102040810000000000000000`）。数据自洽 —— 重跑生成器
逐字节不变、参考解 21/21 Accepted —— 所以所有闸门都是绿的，而**任何按题面写的正解
在这题上都会挂**。根因是缺 `valid()`：输入契约要是写下来了，生成的第一组就被挡住了。

题面的硬约束：`1 <= k <= 100`；`N <= 512` 且 `N = 2^i`（i 为正整数，所以 N ≥ 2）；
矩阵元素只有 0/1，两两之间至少一个空格。`valid()` 是这条契约的反向校验。

`SHAPES` 按「这题会怎么错」排：
  · `uniform_zero` —— 整幅全 0，编码是单个叶子 `00`，答案是 **`0`**（不是 `00`）。
        手工按 4 位一组转十六进制、忘了去前导零的写法在这里挂。
  · `uniform_one`  —— 整幅全 1，叶子 `01`，答案 `1`。
  · `quadrant_blocks` —— 四个象限各自全同且**右上 ≠ 左下**，四个孩子的入队顺序
        （左上→右上→左下→右下）一旦搞反，答案立刻变。
  · `one_cell` —— 只有一个格子是 1，沿一条路径递归到底，考的是「深」。
  · `checkerboard` —— 棋盘格，每一层都得继续划分，编码最长，考的是「宽」。
  · `min_size` / `upper_bound` —— N 取到题面两端 2 和 **512**。
  · `many_pictures` —— k 取到题面上界 **100**，只处理第一幅图的写法在这里挂。
  · `random_dense` / `structured` —— 随机稠密与随机分层。
答案由 `samplecode.py` 产出，再由另写的 oracle（不建树、按子矩阵 BFS + 前缀和判块，
手工 4 位一组转十六进制）逐组复核。
"""
from __future__ import annotations
import random

NUMBER = 1610
INPUT_DOMAIN = "1 <= k <= 100；N <= 512 且 N = 2^i（i为正整数）；每两个0和1之间至少有一个空格"
LABEL = "k pictures; each is N then an N×N matrix of space-separated 0/1"
INVALID = "1\n3\n0 0 0\n0 0 0\n0 0 0\n"        # N=3 不是 2 的幂
SAMPLE = """3
2
0 0
0 0
4
0 0 1 1
0 0 1 1
1 1 0 0
1 1 0 0
8
0 0 0 0 0 0 1 1
0 0 0 0 0 0 1 1
0 0 0 0 0 1 0 0
0 0 0 0 0 1 0 0
1 1 1 1 0 0 0 0
1 1 1 1 0 0 0 0
1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1
"""
SAMPLE_OUT = "0\n114\n258C0511\n"              # 题面「样例输出」逐字，第 0 组必须与它相同

MAX_N = 512
MAX_K = 100
SIZES = (2, 4, 8, 16, 32)
SHAPES = ("uniform_zero", "uniform_one", "quadrant_blocks", "one_cell", "checkerboard",
          "min_size", "upper_bound", "many_pictures", "random_dense", "structured")
# 显式排班而不是 `SHAPES[(seed-1) % len(SHAPES)]`：两条上界形状（N=512 的 `upper_bound`、
# k=100 的 `many_pictures`）各只该出现一次 —— 前者一组输入就 512 KiB，后者本身已经把
# 一个文件占满，取模排班会让它们各来两遍，白占一倍体积。
SCHEDULE = ("uniform_zero", "uniform_one", "min_size", "quadrant_blocks", "one_cell",
            "checkerboard", "upper_bound", "many_pictures", "random_dense", "structured",
            "uniform_zero", "quadrant_blocks", "one_cell", "checkerboard", "min_size",
            "random_dense", "structured", "quadrant_blocks", "one_cell", "checkerboard")
assert len(SCHEDULE) == 20 and set(SCHEDULE) == set(SHAPES)
BOUNDARY = ("upper_bound", "many_pictures")


def _uniform(n, value):
    return [[value] * n for _ in range(n)]


def _structured(r, n, floor):
    """随机分层：块边长降到 `floor` 就必须全同，保证 N=512 也不会炸成 26 万个叶子。"""
    if n <= floor or r.random() < 0.35:
        return _uniform(n, r.randrange(2))
    half = n // 2
    parts = [_structured(r, half, floor) for _ in range(4)]
    grid = [parts[0][i] + parts[1][i] for i in range(half)]
    grid += [parts[2][i] + parts[3][i] for i in range(half)]
    return grid


def _picture(r, shape):
    if shape == "uniform_zero":
        return _uniform(r.choice(SIZES), 0)
    if shape == "uniform_one":
        return _uniform(r.choice(SIZES), 1)
    if shape == "min_size":
        return [[r.randrange(2) for _ in range(2)] for _ in range(2)]
    if shape == "quadrant_blocks":
        n = r.choice((2, 4, 8, 16))
        half = n // 2
        while True:                      # 右上 ≠ 左下，否则换孩子顺序也看不出来
            values = [r.randrange(2) for _ in range(4)]
            if values[1] != values[2]:
                break
        grid = [[values[0]] * half + [values[1]] * half for _ in range(half)]
        grid += [[values[2]] * half + [values[3]] * half for _ in range(half)]
        return grid
    if shape == "one_cell":
        n = r.choice((4, 8, 16, 32))
        grid = _uniform(n, 0)
        grid[r.randrange(n)][r.randrange(n)] = 1
        return grid
    if shape == "checkerboard":
        n = r.choice((2, 4, 8, 16))
        flip = r.randrange(2)
        return [[(row + col + flip) % 2 for col in range(n)] for row in range(n)]
    if shape == "upper_bound":
        return _structured(r, MAX_N, floor=MAX_N // 8)
    if shape == "random_dense":
        n = r.choice(SIZES)
        return [[r.randrange(2) for _ in range(n)] for _ in range(n)]
    if shape == "structured":
        n = r.choice((8, 16, 32, 64))
        return _structured(r, n, floor=2)
    raise KeyError(shape)


def _render(pictures):
    chunks = [str(len(pictures))]
    for grid in pictures:
        chunks.append(str(len(grid)))
        chunks += [" ".join(map(str, row)) for row in grid]
    return "\n".join(chunks) + "\n"


def generate(number, seed):
    if number != NUMBER:
        raise KeyError(number)
    r = random.Random(number * 1_000_003 + seed)
    shape = SCHEDULE[seed - 1]
    if shape == "many_pictures":
        return _render([_picture(r, "min_size") for _ in range(MAX_K)])   # k 取到题面上界
    if shape in BOUNDARY:
        return _render([_picture(r, shape)])
    extra = [r.choice(SHAPES) for _ in range(r.randint(0, 2))]
    shapes = [shape] + [name for name in extra if name not in BOUNDARY]
    r.shuffle(shapes)
    return _render([_picture(r, name) for name in shapes])


def valid(number, text):
    """输入契约：题面那三条硬约束的反向校验。**旧生成器缺的就是这个函数。**"""
    if number != NUMBER:
        raise KeyError(number)
    if not text.endswith("\n"):
        return False
    lines = text.rstrip("\n").split("\n")
    if not lines or not lines[0].strip().isdigit():
        return False
    count = int(lines[0].strip())
    if not 1 <= count <= MAX_K:
        return False
    position = 1
    for _ in range(count):
        if position >= len(lines) or not lines[position].strip().isdigit():
            return False
        size = int(lines[position].strip()); position += 1
        if not 2 <= size <= MAX_N or size & (size - 1):
            return False                          # N 必须是 2 的幂且 ≥ 2
        for _row in range(size):
            if position >= len(lines):
                return False
            cells = lines[position].split(" ")     # 题面：每两个 0/1 之间至少一个空格
            position += 1
            if len(cells) != size or any(cell not in ("0", "1") for cell in cells):
                return False
    return position == len(lines)


import subprocess as _subprocess
from pathlib import Path as _Path
REFERENCE = _Path(__file__).with_name("samplecode.py")
LANGUAGE = "Python3"


def _build():
    out = _Path(__file__).with_name("data")
    out.mkdir(exist_ok=True)
    cases = [SAMPLE] + [generate(NUMBER, seed) for seed in range(1, 21)]
    if len(set(cases)) != len(cases):
        raise SystemExit("两组输入撞了，数据必须互异")
    for index, case in enumerate(cases):
        if not valid(NUMBER, case):
            raise SystemExit(f"case {index} violates the input contract")
        result = _subprocess.run(["python3", str(REFERENCE)], input=case, text=True,
                                 capture_output=True, timeout=300, check=True)
        if index == 0 and result.stdout != SAMPLE_OUT:
            raise SystemExit(f"第 0 组与题面样例输出不符：{result.stdout!r} != {SAMPLE_OUT!r}")
        (out / f"{index}.in").write_text(case, encoding="utf-8")
        (out / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    _build()

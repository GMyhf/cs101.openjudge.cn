#!/usr/bin/env python3
"""01830 开关问题 —— 生成器、输入契约与数据构建。

题面的硬约束只有 `0 < N < 29`（镜像页里这半句被原站的裸 `<` 吃掉了，见 `INPUT_DOMAIN`）
和「状态是 0/1」「每组以 `0 0` 结束」；K 没给上界。`valid()` 是同一条契约的反向校验。

`SHAPES` 按「这题会怎么错」排，不是撒随机 —— 2026-09-11 第一版数据就是撒随机撒出来
的，参考实现漏了对角线，21 组答案全错而生成器自洽，谁也没发现（第 0 组本该跟题面
样例逐字对一遍，那一步漏了）。现在每种形状各钉一类错法：

  · `isolated` / `tiny` / `chain` —— 无边、N=1、单向链，矩阵满秩，答案恒为 1。
        漏对角线的写法在这里最狠：矩阵整个塌成 0，起止态不同直接报无解。
  · `cycle`           —— 环状关联，秩恰好 n-1，答案恒为 2。把 `2^(n-rank)` 写成 1 的挂在这。
  · `complete_multi`  —— 完全关联图，矩阵全 1、秩 1，答案 2^(n-1)（最大 2^6=64）。
  · `complete_impossible` —— 同一个矩阵换个非常量右端项，唯一答案是 impossible。
  · `sparse_solvable` / `sparse_impossible` —— 稀疏有向关联，后者先逼出 rank<n
        再用左零向量把右端项顶出列空间，保证真无解（不是碰运气）。
  · `transpose_trap`  —— 专抓「行列搞反」：矩阵不对称且 rank<n，右端项在 col(A) 里
        但**不在** col(Aᵀ) 里，所以按 `A[i][j]` 建方程的写法会报无解。
  · `upper_bound`     —— N 取到题面上界 28，顺带压一下消元的规模。

答案由 `samplecode.py` 产出，再由 `tools/` 外的第三方 oracle（枚举 2^n 个操作子集
暴力模拟）对 N≤18 的组逐组复核，见 CHANGELOG 里记的不一致数。
"""
from __future__ import annotations
import random

NUMBER = 1830
INPUT_DOMAIN = "第一行 一个数N（0 < N < 29)；第二行 N个0或者1的数；第三行 N个0或者1的数；每组数据以 0 0 结束"
LABEL = "k groups; each group is N (1..28), the start row, the target row, then `I J` relation lines ended by `0 0`"
INVALID = "1\n29\n" + "0 " * 29 + "\n" + "1 " * 29 + "\n0 0\n"      # N=29 越过题面的 28
SAMPLE = """2
3
0 0 0
1 1 1
1 2
1 3
2 1
2 3
3 1
3 2
0 0
3
0 0 0
1 0 1
1 2
2 1
0 0
"""
SAMPLE_OUT = "4\nOh,it's impossible~!!\n"       # 题面「样例输出」逐字，第 0 组必须与它相同

MAX_N = 28
SHAPES = ("isolated", "tiny", "cycle", "complete_multi", "complete_impossible",
          "sparse_solvable", "sparse_impossible", "transpose_trap", "chain", "upper_bound")


def _rows(n, edges):
    """A 的各行：A[j] 的第 i 位为 1 ⟺ i==j（开关翻转自己）或存在关联 (i, j)。"""
    out = [1 << j for j in range(n)]
    for i, j in edges:
        out[j] |= 1 << i
    return out


def _eliminate(rows, n, width):
    """对 [A | 附加位] 做 GF(2) 消元，返回 (rank, 消元后的行)。附加位只跟着走。"""
    rows = list(rows)
    rank = 0
    for col in range(n):
        pivot = next((r for r in range(rank, len(rows)) if (rows[r] >> col) & 1), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for r in range(len(rows)):
            if r != rank and ((rows[r] >> col) & 1):
                rows[r] ^= rows[rank]
        rank += 1
    return rank, rows


def _rank_and_nulls(rows, n):
    """秩，以及左零空间的一组向量（哪些行加起来是 0 —— 用来把右端项顶出列空间）。"""
    tagged = [row | (1 << (n + index)) for index, row in enumerate(rows)]
    rank, reduced = _eliminate(tagged, n, 2 * n)
    nulls = [(row >> n) for row in reduced if (row & ((1 << n) - 1)) == 0 and (row >> n)]
    return rank, nulls


def _consistent(rows, b, n):
    tagged = [row | (((b >> index) & 1) << n) for index, row in enumerate(rows)]
    _rank, reduced = _eliminate(tagged, n, n + 1)
    return not any((row & ((1 << n) - 1)) == 0 and ((row >> n) & 1) for row in reduced)


def _apply(rows, x, n):
    """b = A·x，保证方程组有解。"""
    return sum((bin(rows[j] & x).count("1") & 1) << j for j in range(n))


def _random_edges(r, n, density):
    return [(i, j) for i in range(n) for j in range(n) if i != j and r.random() < density]


def _group(r, shape):
    """返回 (n, start, target, edges)；start/target 用 0/1 列表表示。"""
    if shape == "tiny":
        n, edges = 1, []
    elif shape == "isolated":
        n, edges = r.randint(2, 8), []
    elif shape == "chain":
        n = r.randint(3, 9)
        edges = [(i, i + 1) for i in range(n - 1)]
    elif shape == "cycle":
        n = r.randint(3, 9)
        edges = [(i, (i + 1) % n) for i in range(n)]
    elif shape in ("complete_multi", "complete_impossible"):
        n = r.randint(2, 7)
        edges = [(i, j) for i in range(n) for j in range(n) if i != j]
    elif shape == "upper_bound":
        n = MAX_N
        edges = _random_edges(r, n, 0.12)
    elif shape == "sparse_solvable":
        n = r.randint(4, 10)
        edges = _random_edges(r, n, r.choice((0.18, 0.25, 0.35)))
    elif shape == "sparse_impossible":
        while True:                                  # 先逼出 rank < n，否则无从构造无解
            n = r.randint(4, 10)
            edges = _random_edges(r, n, r.choice((0.25, 0.35, 0.45)))
            rows = _rows(n, edges)
            rank, nulls = _rank_and_nulls(rows, n)
            if rank < n and nulls:
                break
    elif shape == "transpose_trap":
        while True:                                  # A 不对称、rank<n，且 b ∈ col(A) \ col(Aᵀ)
            n = r.randint(3, 7)
            edges = _random_edges(r, n, r.choice((0.3, 0.4, 0.5)))
            rows = _rows(n, edges)
            rank, _nulls = _rank_and_nulls(rows, n)
            if rank == n:
                continue
            x = r.randrange(1 << n)
            b = _apply(rows, x, n)
            if not _consistent(_rows(n, [(j, i) for i, j in edges]), b, n):
                break
    else:
        raise KeyError(shape)

    rows = _rows(n, edges)
    if shape == "complete_impossible":
        b = r.randrange(1, (1 << n) - 1) if n > 1 else 1        # 非常量右端项 ⇒ 必然无解
        while b in (0, (1 << n) - 1):
            b = r.randrange(1 << n)
    elif shape == "sparse_impossible":
        _rank, nulls = _rank_and_nulls(rows, n)
        b = _apply(rows, r.randrange(1 << n), n)
        b ^= 1 << (nulls[0].bit_length() - 1)                   # 顶出列空间
    elif shape == "transpose_trap":
        pass                                                    # b 在上面的循环里定好了
    elif shape in ("isolated", "tiny", "chain"):
        b = r.randrange(1 << n)                                 # 满秩，任何 b 都有唯一解
    elif shape == "complete_multi":
        b = 0                                                   # 全 1 矩阵，常量右端项才有解
    else:
        b = _apply(rows, r.randrange(1 << n), n)

    start = [r.randrange(2) for _ in range(n)]
    target = [start[j] ^ ((b >> j) & 1) for j in range(n)]
    return n, start, target, edges


def _render(groups):
    chunks = [str(len(groups))]
    for n, start, target, edges in groups:
        chunks.append(str(n))
        chunks.append(" ".join(map(str, start)))
        chunks.append(" ".join(map(str, target)))
        chunks += [f"{i + 1} {j + 1}" for i, j in edges]
        chunks.append("0 0")
    return "\n".join(chunks) + "\n"


def generate(number, seed):
    if number != NUMBER:
        raise KeyError(number)
    r = random.Random(number * 1_000_003 + seed)
    shapes = [SHAPES[(seed - 1) % len(SHAPES)]]
    shapes += [r.choice(SHAPES) for _ in range(r.randint(0, 2))]
    r.shuffle(shapes)
    return _render([_group(r, shape) for shape in shapes])


def valid(number, text):
    if number != NUMBER:
        raise KeyError(number)
    tokens = text.split()
    if not text.endswith("\n") or not tokens:
        return False
    position = 0

    def take():
        nonlocal position
        if position >= len(tokens):
            raise ValueError("truncated")
        token = tokens[position]; position += 1
        if not token.lstrip("-").isdigit():
            raise ValueError("not an integer")
        return int(token)

    try:
        k = take()
        if k < 1:
            return False
        for _ in range(k):
            n = take()
            if not 1 <= n <= MAX_N:
                return False
            for _ in range(2 * n):
                if take() not in (0, 1):
                    return False
            while True:
                i, j = take(), take()
                if i == 0 and j == 0:
                    break
                if not (1 <= i <= n and 1 <= j <= n):
                    return False
    except ValueError:
        return False
    return position == len(tokens)


import subprocess as _subprocess
from pathlib import Path as _Path
REFERENCE = _Path(__file__).with_name("samplecode.py")
LANGUAGE = "Python"


def _build():
    out = _Path(__file__).with_name("data")
    out.mkdir(exist_ok=True)
    cases = [SAMPLE] + [generate(NUMBER, seed) for seed in range(1, 21)]
    if len(set(cases)) != len(cases):
        raise SystemExit("两组输入撞了，数据必须互异")
    for index, case in enumerate(cases):
        if not valid(NUMBER, case):
            raise SystemExit(f"case {index} violates the input contract: {case!r}")
        result = _subprocess.run(["python3", str(REFERENCE)], input=case, text=True,
                                 capture_output=True, timeout=120, check=True)
        if index == 0 and result.stdout != SAMPLE_OUT:
            raise SystemExit(f"第 0 组与题面样例输出不符：{result.stdout!r} != {SAMPLE_OUT!r}")
        (out / f"{index}.in").write_text(case, encoding="utf-8")
        (out / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    _build()

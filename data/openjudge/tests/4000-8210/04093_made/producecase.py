#!/usr/bin/env python3
"""04093 倒排索引查询 —— 生成器、输入契约与数据构建。

**这份文件 2026-09-12 重写过。** 旧版出自批次 001a 的生成器，没有 `valid()`，
两处越过题面：

    docs = sorted(r.sample(range(1, 10), r.randint(0, 5)))          # c_i 可以是 0
    lines.append(" ".join(str(r.choice([-1, 0, 1])) for _ in range(n)))  # 可能一个 1 都没有

题面写得很明确：`1 <= c_i <= 1000`，以及**「数据保证每行至少出现一个 1」**
（这两处的裸 `<` 被原站当标签吃掉了，要看镜像页的 HTML 源码才看得见）。旧数据里
有 13 处 `c_i = 0`、**22 条查询行一个 1 都没有**。后者不是纸面问题：题面既然保证
这种查询不存在，实现怎么处理它都不影响正确性 —— 参考实现按 NOT FOUND 处理，而
「全集减去排除项」同样说得通，实测后者在旧数据上 **Wrong Answer 挂第 2 组**。
**旧数据会判错一份正确程序。**

旧版另外三处不足：只有 20 组（流水线要 21）、文档编号恒取 1..9（题面说的是 32 位
整数）、每个词的文档列表永远是**有序**的（题面明写「编号不一定有序」，于是「假设
输入有序」的写法在旧数据上照样满分）。

`SHAPES` 按「这题会怎么错」排：
  · `zeros_ignored`  —— 查询里带 0，题面说 0 是「无所谓」。把 0 当成 -1 的写法挂在这。
  · `excludes`       —— 1 与 -1 混用，排除项真的会削掉结果。
  · `all_ones`       —— 整行全 1，纯交集；同时造出「交集非空」和「交集为空」两种。
  · `not_found`      —— 结果必为空，考 `NOT FOUND` 这条分支。
  · `unordered_docs` —— 文档编号**故意打乱**（题面：编号不一定有序），
        「假设输入已排序、直接按读入顺序输出」的写法挂在这。
  · `single_word`    —— N=1。
  · `upper_n`        —— N 与 M 都取到题面上界 100。
  · `upper_ci`       —— 某个词的 c_i 取到题面上界 1000。
  · `big_ids`        —— 文档编号贴近 32 位上界 2^31-1。
文档编号的取值域刻意保持在几千以内（`big_ids` 除外），这样第三方 oracle 的
「逐文档扫一遍」才跑得动 —— 它是以文档为中心的另一套算法，不能退化成和参考实现
同一个写法。
"""
from __future__ import annotations
import random

NUMBER = 4093
INPUT_DOMAIN = ("1 <= N <= 100；1 <= c_i <= 1000，文档编号为32位整数；1 <= M <= 100；"
                "查询每个数取 1/-1/0，数据保证每行至少出现一个1")
LABEL = "N inverted lists (c_i then c_i doc ids), then M query rows of N values in {1,-1,0}"
INVALID = "1\n1 7\n1\n0\n"                 # 查询行一个 1 都没有，越过题面的保证
SAMPLE = "3\n3 1 2 3\n1 2\n1 3\n3\n1 1 1\n1 -1 0\n1 -1 -1\n"
SAMPLE_OUT = "NOT FOUND\n1 3\n1\n"         # 题面「样例输出」逐字

MAX_N = 100
MAX_M = 100
MAX_CI = 1000
INT32 = 2 ** 31 - 1
SHAPES = ("zeros_ignored", "excludes", "all_ones", "not_found", "unordered_docs",
          "single_word", "upper_n", "upper_ci", "big_ids")
SCHEDULE = ("zeros_ignored", "excludes", "all_ones", "not_found", "unordered_docs",
            "single_word", "upper_n", "upper_ci", "big_ids", "zeros_ignored",
            "excludes", "all_ones", "not_found", "unordered_docs", "excludes",
            "zeros_ignored", "all_ones", "not_found", "unordered_docs", "excludes")
assert len(SCHEDULE) == 20 and set(SCHEDULE) == set(SHAPES)


def _words(r, count, universe, low=1, high=6):
    """每个词一个非空文档集合（`c_i >= 1` 是题面的硬约束）。"""
    return [r.sample(universe, min(len(universe), max(1, r.randint(low, high))))
            for _ in range(count)]


def _query_from_doc(r, words, doc, zeros=True, excludes=True):
    """照某一篇文档的实际归属造一条查询 —— 保证它至少命中这一篇，结果非空。"""
    row = []
    for docs in words:
        if doc in docs:
            row.append(1)
        elif excludes and r.random() < 0.35:
            row.append(-1)
        elif zeros and r.random() < 0.5:
            row.append(0)
        else:
            row.append(0)
    if 1 not in row:                      # 题面保证每行至少一个 1
        row[r.randrange(len(row))] = 1
    return row


def _random_query(r, n, zeros=True, excludes=True):
    choices = [1, 1]
    if excludes:
        choices.append(-1)
    if zeros:
        choices.append(0)
    row = [r.choice(choices) for _ in range(n)]
    if 1 not in row:
        row[r.randrange(n)] = 1
    return row


def _group(r, shape):
    if shape == "single_word":
        universe = list(range(1, 12))
        words = _words(r, 1, universe)
        queries = [[1] for _ in range(r.randint(2, 5))]
    elif shape == "upper_n":
        universe = list(range(1, 60))
        words = _words(r, MAX_N, universe, 1, 8)
        docs = sorted({doc for group in words for doc in group})
        # 100 个词求交，纯随机查询几乎必然 NOT FOUND —— 那样最大的一组只测到
        # NOT FOUND 这一条分支。所以一半查询照某篇文档的实际归属造，保证命中。
        queries = [_query_from_doc(r, words, r.choice(docs)) for _ in range(MAX_M // 2)]
        queries += [_random_query(r, MAX_N) for _ in range(MAX_M - MAX_M // 2)]
        r.shuffle(queries)
    elif shape == "upper_ci":
        universe = list(range(1, 1600))
        words = _words(r, r.randint(3, 6), universe, 400, 900)
        words[r.randrange(len(words))] = r.sample(universe, MAX_CI)   # c_i 取到上界
        queries = [_random_query(r, len(words)) for _ in range(r.randint(4, 10))]
    elif shape == "big_ids":
        universe = r.sample(range(INT32 - 5000, INT32 + 1), 40)
        words = _words(r, r.randint(2, 5), universe, 2, 10)
        docs = sorted({doc for group in words for doc in group})
        queries = [_query_from_doc(r, words, r.choice(docs)) for _ in range(3)]
        queries += [_random_query(r, len(words)) for _ in range(r.randint(1, 4))]
    elif shape == "not_found":
        universe = list(range(1, 30))
        count = r.randint(2, 5)
        words = _words(r, count, universe, 1, 4)
        # 两两不相交 ⇒ 整行全 1 必然交集为空
        pool = r.sample(universe, sum(len(group) for group in words))
        position = 0
        for index, group in enumerate(words):
            words[index] = pool[position:position + len(group)]
            position += len(group)
        queries = [[1] * count for _ in range(r.randint(2, 4))]
        queries += [_random_query(r, count) for _ in range(r.randint(1, 3))]
    elif shape == "unordered_docs":
        universe = list(range(1, 40))
        words = _words(r, r.randint(2, 6), universe, 3, 9)
        for group in words:
            r.shuffle(group)              # 题面：编号不一定有序
        docs = sorted({doc for group in words for doc in group})
        queries = [_query_from_doc(r, words, r.choice(docs)) for _ in range(r.randint(2, 5))]
    elif shape == "all_ones":
        universe = list(range(1, 20))
        count = r.randint(2, 5)
        shared = r.sample(universe, r.randint(1, 3))
        words = [sorted(set(shared) | set(r.sample(universe, r.randint(1, 5))))
                 for _ in range(count)]
        queries = [[1] * count]           # 交集非空（`shared` 在里面）
        queries += [_random_query(r, count) for _ in range(r.randint(2, 5))]
    elif shape == "excludes":
        universe = list(range(1, 25))
        words = _words(r, r.randint(2, 6), universe, 2, 8)
        docs = sorted({doc for group in words for doc in group})
        queries = [_query_from_doc(r, words, r.choice(docs), zeros=False)
                   for _ in range(r.randint(2, 4))]
        queries += [_random_query(r, len(words), zeros=False) for _ in range(r.randint(1, 3))]
    elif shape == "zeros_ignored":
        universe = list(range(1, 25))
        words = _words(r, r.randint(2, 6), universe, 2, 8)
        docs = sorted({doc for group in words for doc in group})
        # 0 必须被当成「无所谓」：这些查询只有一个 1，其余全 0 ——
        # 把 0 当成 -1 的写法会把结果削成空。
        queries = []
        for _ in range(r.randint(2, 5)):
            row = [0] * len(words)
            row[r.randrange(len(words))] = 1
            queries.append(row)
        queries += [_query_from_doc(r, words, r.choice(docs)) for _ in range(r.randint(1, 3))]
    else:
        raise KeyError(shape)
    return words, queries


def _render(words, queries):
    lines = [str(len(words))]
    lines += [" ".join(map(str, [len(group)] + list(group))) for group in words]
    lines.append(str(len(queries)))
    lines += [" ".join(map(str, row)) for row in queries]
    return "\n".join(lines) + "\n"


def generate(number, seed):
    if number != NUMBER:
        raise KeyError(number)
    r = random.Random(number * 1_000_003 + seed)
    return _render(*_group(r, SCHEDULE[seed - 1]))


def valid(number, text):
    """输入契约：题面那几条硬约束的反向校验。**旧生成器缺的就是这个函数。**"""
    if number != NUMBER:
        raise KeyError(number)
    if not text.endswith("\n"):
        return False
    lines = text.rstrip("\n").split("\n")
    try:
        count = int(lines[0])
    except (ValueError, IndexError):
        return False
    if not 1 <= count <= MAX_N:
        return False
    position = 1
    for _ in range(count):
        if position >= len(lines):
            return False
        parts = lines[position].split(" ")
        position += 1
        try:
            size = int(parts[0]); docs = [int(value) for value in parts[1:]]
        except ValueError:
            return False
        if not 1 <= size <= MAX_CI or len(docs) != size:
            return False                            # 1 <= c_i <= 1000
        if any(not 0 <= doc <= INT32 for doc in docs):
            return False                            # 文档编号为 32 位整数
    if position >= len(lines):
        return False
    try:
        queries = int(lines[position])
    except ValueError:
        return False
    position += 1
    if not 1 <= queries <= MAX_M:
        return False
    for _ in range(queries):
        if position >= len(lines):
            return False
        parts = lines[position].split(" ")
        position += 1
        if len(parts) != count or any(value not in ("1", "-1", "0") for value in parts):
            return False
        if "1" not in parts:
            return False                            # 数据保证每行至少出现一个1
    return position == len(lines)


import subprocess as _subprocess
from pathlib import Path as _Path
REFERENCE = _Path(__file__).with_name("samplecode.py")
LANGUAGE = "Python3"


def _build():
    out = _Path(__file__).with_name("data")
    out.mkdir(exist_ok=True)
    for stale in out.glob("*"):
        stale.unlink()
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

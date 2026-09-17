#!/usr/bin/env python3
"""02793 孙子问题 —— 生成器、输入契约、special judge 自检与数据构建。

题面：多组数据（不多于 30 组），每组一行：n（1 <= n <= 10），然后 n 个不大于 50 的正整数
a_1..a_n；n = 0 结束。每组输出任意一组满足题意的正整数 b（每个不超过 50 位），不存在
输出 NO。答案不唯一，判题走同目录 `checker.py`（判据推导见其文件头）。

解总是存在（构造见 `samplecode.py`），所以 NO 永远是错的 —— 旧离线目录里的 `e1.py`
按「模数不两两互素就 NO」写，正是本题最典型的错法。`checker.py` 接受旧离线目录
`2793/1.out`（原站 28 组答案，与本仓库参考解的数值大多不同）。

`SHAPES` 按「这题会怎么错」排：
  · `primes`        —— 两两互素，教科书 CRT 就能过；用来确认基本路径。
  · `nested_powers` —— 2 4 8 16 32 / 3 9 27 / 5 25 / 7 49 打乱次序：把素数 q 分给「第一个
        被 q 整除」而不是「q 的最高次幂所在」的下标，就错。
  · `ones`          —— a_i = 1 混在里面（N mod 1 恒为 0，对应 b 随便取）、全 1（L=1）。
  · `duplicates`    —— 同一个数重复多次，只有 b 的和有约束。
  · `single`        —— n = 1，答案是 ≡1 (mod a) 的任意正整数。
  · `max_lcm`       —— n=10、lcm 尽量大（10^15 以上），64 位整数里 L·inverse 会溢出。
  · `shared_factors` —— 6 10 15、2 6 4 这类两两不互素但整体有解的组，e1.py 式 NO 挂在这。
  · `random`        —— 原站生成器的样子：n=10，a 在 1..50 里随机。
  · `boundary`      —— 48、49、50 等上界附近。
每个文件 1..30 组，大多数取满 30 组。

构建时每组都要：参考解输出被 checker 接受、并与朴素判据（对 N = 0..L-1 逐个验证，
仅 L <= 20000 的组）一致；题面样例输出被接受；`ALTERNATIVES` 里的正确解全部被接受
且与 `.out` 不同；`WRONG` 里每个错解至少被拒一组。
"""
from __future__ import annotations
import importlib.util
import random
import subprocess
import sys
import tempfile
from math import lcm
from pathlib import Path

NUMBER = 2793
HERE = Path(__file__).resolve().parent
REFERENCE = HERE / "samplecode.py"
CHECKER = HERE / "checker.py"
INPUT_DOMAIN = "输入包括多组测试数据(不多于30组)，每组数据包括一行。在每组数据中，首先给出ai的个数n (1 <= n <= 10)，然后给出n个不大于50的正整数a1, a2, ... an。最后一组测试数据中n = 0，表示输入的结束，这组数据不用处理。"
SAMPLE = "3 3 5 7\n0\n"
SAMPLE_OUT = "70 21 15\n"                 # 题面「样例输出」逐字
MAX_GROUPS, MAX_N, MAX_A, MAX_DIGITS = 30, 10, 50, 50
PRIMES = [p for p in range(2, MAX_A + 1) if all(p % q for q in range(2, p))]


def _group(r, shape):
    if shape == "primes":
        a = r.sample(PRIMES, r.randint(1, MAX_N))
    elif shape == "nested_powers":
        chains = [[2, 4, 8, 16, 32], [3, 9, 27], [5, 25], [7, 49]]
        a = [x for chain in r.sample(chains, r.randint(1, 4)) for x in r.sample(chain, r.randint(1, len(chain)))]
        a = a[:MAX_N]; r.shuffle(a)
    elif shape == "ones":
        n = r.randint(1, MAX_N)
        a = [1] * n if r.random() < 0.3 else [1 if r.random() < 0.5 else r.randint(2, MAX_A) for _ in range(n)]
    elif shape == "duplicates":
        pool = r.sample(range(2, MAX_A + 1), r.randint(1, 3))
        a = [r.choice(pool) for _ in range(r.randint(2, MAX_N))]
    elif shape == "single":
        a = [r.randint(1, MAX_A)]
    elif shape == "max_lcm":
        a = r.sample([32, 27, 25, 49, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47], MAX_N)
    elif shape == "shared_factors":
        base = r.choice([[6, 10, 15], [2, 6, 4], [12, 18, 8], [14, 21, 6], [20, 30, 45], [35, 10, 14]])
        a = base + [r.choice([2, 3, 5, 6, 10, 12, 15, 30]) for _ in range(r.randint(0, MAX_N - 3))]
        r.shuffle(a)
    elif shape == "boundary":
        a = [r.choice([50, 49, 48, 47, 46, 45]) for _ in range(r.randint(1, MAX_N))]
    else:  # random
        a = [r.randint(1, MAX_A) for _ in range(MAX_N)]
    return a


SHAPES = ("primes", "nested_powers", "ones", "duplicates", "single", "max_lcm",
          "shared_factors", "boundary", "random")


def _render(groups):
    return "".join(f"{len(a)} " + " ".join(map(str, a)) + "\n" for a in groups) + "0\n"


def generate(number, seed):
    assert number == NUMBER
    r = random.Random(number * 1_000_003 + seed)
    if seed <= 9:                          # 每种形状一个满 30 组的文件
        groups = [_group(r, SHAPES[seed - 1]) for _ in range(MAX_GROUPS)]
    elif seed <= 13:                       # 原站样子：n=10 随机，组数不一
        groups = [_group(r, "random") for _ in range(r.choice([1, 7, 20, 30]))]
    elif seed == 14:
        groups = [_group(r, "max_lcm")]
    elif seed == 15:
        groups = [[1]]
    elif seed == 16:                       # 同一多重集的不同排列：分配跟着下标走
        base = [16, 8, 27, 9, 6, 10, 25, 50, 49, 7]
        groups = [r.sample(base, MAX_N) for _ in range(MAX_GROUPS)]
    else:                                  # 形状混排
        groups = [_group(r, r.choice(SHAPES)) for _ in range(r.randint(10, MAX_GROUPS))]
    return _render(groups)


def valid(number, text):
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if lines[-1] != "0" or not 2 <= len(lines) <= MAX_GROUPS + 1:
        return False
    for line in lines[:-1]:
        parts = line.split(" ")
        if not all(p.isascii() and p.isdigit() and str(int(p)) == p for p in parts):
            return False
        n, a = int(parts[0]), [int(p) for p in parts[1:]]
        if not (1 <= n <= MAX_N and len(a) == n and all(1 <= x <= MAX_A for x in a)):
            return False
    return True


# ---- 另几种正确解与典型错解 ----

def _groups(text):
    tokens, p, out = text.split(), 0, []
    while True:
        n = int(tokens[p]); p += 1
        if n == 0:
            return out
        out.append([int(x) for x in tokens[p:p + n]]); p += n


def _prime_powers(L):
    return [(p, p ** next(e for e in range(7, 0, -1) if L % p ** e == 0)) for p in PRIMES if L % p == 0]


def _idempotents(a, pick, modulus_of=lambda p, q: q):
    """pick(候选下标列表) 选一个下标接管素数幂；modulus_of 决定按 q^e 还是 p 找候选。"""
    L = lcm(*a)
    share = [1] * len(a)
    for p, q in _prime_powers(L):
        share[pick([i for i, x in enumerate(a) if x % modulus_of(p, q) == 0])] *= q
    out = []
    for P in share:
        rest = L // P
        try:
            value = rest * pow(rest, -1, P) % L if P > 1 else 0
        except ValueError:                  # 错解里 P 与 rest 可能不互素
            value = rest
        out.append(value)
    return out


def _fmt(b):
    return " ".join(map(str, b))


def _shift(a):
    L = lcm(*a)
    r = random.Random(sum(a) * 131 + len(a))
    return _fmt((x or L) + L * r.randint(0, 10 ** 20) for x in _idempotents(a, min))


ALTERNATIVES = {
    "last_index_owns_prime_power": lambda a: _fmt(x or lcm(*a) for x in _idempotents(a, max)),
    "plus_random_multiples_of_L": _shift,
}


def _pairwise_coprime(a):
    return all(lcm(x, y) == x * y for i, x in enumerate(a) for y in a[i + 1:])


WRONG = {
    "NO_unless_pairwise_coprime": lambda a: _fmt(x or lcm(*a) for x in _idempotents(a, min)) if _pairwise_coprime(a) else "NO",
    "prime_goes_to_first_multiple_of_p": lambda a: _fmt(x or lcm(*a) for x in _idempotents(a, min, lambda p, q: p)),
    "prints_0_instead_of_L": lambda a: _fmt(_idempotents(a, min)),
    "over_50_digits_when_L_big": lambda a: _fmt((x or lcm(*a)) + (lcm(*a) * 10 ** 50 if lcm(*a) > 10 ** 6 else 0) for x in _idempotents(a, min)),
}


def _oracle_ok(a, b):
    L = lcm(*a)
    return all(sum(bi * (N % ai) for ai, bi in zip(a, b)) % L == N % L for N in range(L))


def check(case, output, answer):
    with tempfile.TemporaryDirectory() as temp:
        paths = []
        for name, data in (("in", case), ("out", output), ("ans", answer)):
            path = Path(temp) / name
            path.write_text(data, encoding="utf-8")
            paths.append(str(path))
        result = subprocess.run([sys.executable, "-I", str(CHECKER), *paths],
                                capture_output=True, timeout=30)
    if result.returncode not in (0, 42):
        raise SystemExit(f"checker 出错：{result.returncode} {result.stdout!r} {result.stderr[-500:]!r}")
    return result.returncode == 0


def _build():
    out = HERE / "data"
    out.mkdir(exist_ok=True)
    for path in out.glob("*"):
        path.unlink()
    cases = [SAMPLE] + [generate(NUMBER, seed) for seed in range(1, 21)]
    if len(set(cases)) != len(cases):
        raise SystemExit("两组输入撞了，数据必须互异")
    differs = dict.fromkeys(ALTERNATIVES, False)
    rejected = dict.fromkeys(WRONG, 0)
    for index, case in enumerate(cases):
        if not valid(NUMBER, case):
            raise SystemExit(f"case {index} violates the input contract")
        answer = subprocess.run([sys.executable, str(REFERENCE)], input=case, text=True,
                                capture_output=True, timeout=120, check=True).stdout
        groups = _groups(case)
        rows = [list(map(int, line.split())) for line in answer.splitlines()]
        if len(rows) != len(groups):
            raise SystemExit(f"case {index}: 参考解行数不对")
        for a, b in zip(groups, rows):
            if lcm(*a) <= 20000 and not _oracle_ok(a, b):
                raise SystemExit(f"case {index}: 参考解在 {a} 上不满足朴素判据")
        if not check(case, answer, answer):
            raise SystemExit(f"case {index}: 参考解输出被 checker 拒绝")
        if index == 0 and not check(case, SAMPLE_OUT, answer):
            raise SystemExit("题面样例输出被 checker 拒绝")
        for name, fn in ALTERNATIVES.items():
            output = "".join(fn(a) + "\n" for a in groups)
            if not check(case, output, answer):
                raise SystemExit(f"case {index}: 正确解 {name} 被 checker 拒绝")
            differs[name] |= output != answer
        for name, fn in WRONG.items():
            rejected[name] += not check(case, "".join(fn(a) + "\n" for a in groups), answer)
        (out / f"{index}.in").write_text(case, encoding="utf-8")
        (out / f"{index}.out").write_text(answer, encoding="utf-8")
    if not all(differs.values()):
        raise SystemExit(f"有正确解与 .out 完全相同：{differs}")
    if not all(rejected.values()):
        raise SystemExit(f"有错解一组都没被拒：{rejected}")
    print("wrong solutions rejected on:", rejected)


if __name__ == "__main__":
    _build()

#!/usr/bin/env python3
"""03151 Pots —— 生成器、输入契约、special judge 自检与数据构建。

题面：一行 A B C，都是 1..100 的整数且 C <= max(A, B)。输出最短操作序列（长度 K 加 K 行
操作），到不了输出 impossible。最短序列不唯一，判题走同目录 `checker.py`。

旧离线目录 `3151/` 的 7 组里，`5.out`（100 47 25，K=72）照题面语义模拟到最后是 (6, 47)，
根本不是合法答案 —— 同目录 `validate_new.cpp` 注释说原站 SPJ 读错了文件，所以这份坏答案
一直没被发现。它的 K=72 与本仓库 BFS 一致；其余 6 组的旧答案都被本 checker 接受。

每个文件只有一组，所以 20 组都是挑出来的「会怎么错」：
  · `max_k`          —— 100 99 50 / 99 100 50，K=196，全题最长；回溯写成递归或路径存不下的挂。
  · `impossible_gcd` —— gcd(A,B) ∤ C。
  · `impossible_equal` —— A == B 且 C < A：只能是 0 或 A。
  · `fill_one`       —— C == A < B / C == B < A / A == B == C：K=1，且要分清是哪只壶。
  · `only_larger_pot` —— C > min(A,B)，只能出现在大壶里；按「C <= min 才有解」判的挂。
  · `pot1_goal_trap` / `pot2_goal_trap` —— 只在某一只壶里找 C 的 BFS 会得到更长或无解。
  · `unit_pot`       —— A 或 B 为 1。
  · `sample_mirror`  —— 5 3 4，题面样例把两壶对调。
  · `random_long` / `random` —— 随机，前者限定 K >= 100。
  · `two_shortest`   —— 最短序列恰有两条的输入（绝大多数输入最短序列唯一，全题只有 1756 个
        输入有两条）。只有在这类输入和 A == B 上，另一份正确解才可能与 `.out` 逐字不同。

构建时每组都要：参考解输出被 checker 接受、K 与朴素 BFS（只算距离）及双向灌倒循环模拟一致；
题面样例输出（第 0 组）被接受；`ALTERNATIVES` 里另三种最短序列全部被接受，其中至少两种有组与
`.out` 不同；`WRONG` 里每个错解至少被拒一组。
"""
from __future__ import annotations
import random
import subprocess
import sys
import tempfile
from collections import deque
from functools import lru_cache
from math import gcd
from pathlib import Path

NUMBER = 3151
HERE = Path(__file__).resolve().parent
REFERENCE = HERE / "samplecode.py"
CHECKER = HERE / "checker.py"
INPUT_DOMAIN = "On the first and only line are the numbers A, B, and C. These are all integers in the range from 1 to 100 and C≤max(A,B)."
SAMPLE = "3 5 4\n"
SAMPLE_OUT = "6\nFILL(2)\nPOUR(2,1)\nDROP(1)\nPOUR(2,1)\nFILL(2)\nPOUR(2,1)\n"   # 题面「样例输出」逐字
MAX = 100
OPS = ("FILL(1)", "FILL(2)", "DROP(1)", "DROP(2)", "POUR(1,2)", "POUR(2,1)")


def _apply(A, B, state, op):
    x, y = state
    if op == "FILL(1)": return A, y
    if op == "FILL(2)": return x, B
    if op == "DROP(1)": return 0, y
    if op == "DROP(2)": return x, 0
    if op == "POUR(1,2)":
        t = min(x, B - y); return x - t, y + t
    t = min(y, A - x); return x + t, y - t


@lru_cache(maxsize=None)
def _dist(A, B, order=OPS):
    d, parent, q = {(0, 0): 0}, {(0, 0): None}, deque([(0, 0)])
    while q:
        s = q.popleft()
        for op in order:
            t = _apply(A, B, s, op)
            if t not in d:
                d[t] = d[s] + 1; parent[t] = (s, op); q.append(t)
    return d, parent


@lru_cache(maxsize=None)
def _path_counts(A, B):
    """每个状态的最短路条数（BFS 分层累加）。"""
    d, cnt, q = {(0, 0): 0}, {(0, 0): 1}, deque([(0, 0)])
    while q:
        s = q.popleft()
        for op in OPS:
            t = _apply(A, B, s, op)
            if t not in d:
                d[t] = d[s] + 1; cnt[t] = cnt[s]; q.append(t)
            elif d[t] == d[s] + 1:
                cnt[t] += cnt[s]
    return d, cnt


def _shortest_count(A, B, C):
    d, cnt = _path_counts(A, B)
    k = _k(A, B, C)
    return 0 if k is None else sum(cnt[s] for s, v in d.items() if v == k and C in s)


def _k(A, B, C, goal=lambda s, C: C in s):
    d, _ = _dist(A, B)
    hits = [v for s, v in d.items() if goal(s, C)]
    return min(hits) if hits else None


def generate(number, seed):
    assert number == NUMBER
    r = random.Random(number * 1_000_003 + seed)
    triples = [(A, B, C) for A in range(1, MAX + 1) for B in range(1, MAX + 1) for C in range(1, max(A, B) + 1)]
    def pick(pred):
        return r.choice([t for t in triples if pred(*t)])
    if seed == 1:
        t = (100, 99, 50)
    elif seed == 2:
        t = (99, 100, 50)
    elif seed == 3:
        t = pick(lambda A, B, C: gcd(A, B) >= 3 and C % gcd(A, B) and A >= 50 and B >= 50)
    elif seed == 4:
        t = pick(lambda A, B, C: A == B and C < A and A >= 60)
    elif seed == 5:
        t = pick(lambda A, B, C: C == A < B)
    elif seed == 6:
        t = pick(lambda A, B, C: C == B < A)
    elif seed == 7:
        t = (100, 100, 100)
    elif seed == 8:
        t = pick(lambda A, B, C: B < C < A and gcd(A, B) == 1 and B >= 20)
    elif seed == 9:
        t = pick(lambda A, B, C: A < C < B and gcd(A, B) == 1 and A >= 20)
    elif seed == 10:          # 只看 1 号壶会更长
        t = pick(lambda A, B, C: A >= 60 and B >= 60 and C <= min(A, B) and gcd(A, B) == 1
                 and C % 7 == 3 and _k(A, B, C, lambda s, C: s[0] == C) != _k(A, B, C))
    elif seed == 11:          # 只看 2 号壶会更长
        t = pick(lambda A, B, C: A >= 60 and B >= 60 and C <= min(A, B) and gcd(A, B) == 1
                 and C % 7 == 5 and _k(A, B, C, lambda s, C: s[1] == C) != _k(A, B, C))
    elif seed == 12:
        t = (1, 1, 1)
    elif seed == 13:
        t = pick(lambda A, B, C: A == 1 and B >= 80 and 1 < C < B)
    elif seed == 14:
        t = (5, 3, 4)
    elif seed == 15:
        t = pick(lambda A, B, C: gcd(A, B) == 2 and C % 2 == 1 and C > min(A, B))
    elif seed <= 17:
        t = pick(lambda A, B, C: A >= 90 and B >= 90 and gcd(A, B) == 1 and C % 11 == seed % 11
                 and _k(A, B, C) >= 100)
    elif seed == 18:          # 最短序列恰有两条（全题只有 1756 个这样的输入，最多也就两条）
        t = pick(lambda A, B, C: A >= 40 and B >= 90 and C % 2 == 0 and _k(A, B, C) is not None
                 and _k(A, B, C) >= 100 and _shortest_count(A, B, C) >= 2)
    elif seed == 19:
        t = pick(lambda A, B, C: 20 <= A <= 60 and 20 <= B <= 60 and C % 3 == 1
                 and _shortest_count(A, B, C) >= 2)
    else:
        t = pick(lambda A, B, C: C % 13 == 7 and A < B and gcd(A, B) == 1)
    return "%d %d %d\n" % t


def valid(number, text):
    if not text.endswith("\n") or text.count("\n") != 1:
        return False
    parts = text[:-1].split(" ")
    if len(parts) != 3 or not all(p.isascii() and p.isdigit() and str(int(p)) == p for p in parts):
        return False
    A, B, C = map(int, parts)
    return 1 <= A <= MAX and 1 <= B <= MAX and 1 <= C <= MAX and C <= max(A, B)


# ---- 另几种正确解与典型错解 ----

def _render(ops):
    return "impossible\n" if ops is None else f"{len(ops)}\n" + "".join(op + "\n" for op in ops)


def _bfs_path(A, B, C, order=OPS, goal=lambda s, C: C in s):
    d, parent = _dist(A, B, order)
    hits = sorted((v, i, s) for i, (s, v) in enumerate(d.items()) if goal(s, C))
    if not hits:
        return None
    s, ops = hits[0][2], []
    while parent[s] is not None:
        s, op = parent[s]; ops.append(op)
    return ops[::-1]


def _random_shortest(A, B, C):
    """在所有最短序列里随机挑一条：随机选终点，再逐步随机选满足 d[p] = d[s]-1 的前驱。"""
    d, _ = _dist(A, B)
    hits = [s for s, v in d.items() if C in s]
    if not hits:
        return None
    k = min(d[s] for s in hits)
    r = random.Random(A * 10007 + B * 101 + C)
    s, ops = r.choice(sorted(s for s in hits if d[s] == k)), []
    while s != (0, 0):
        choices = sorted((p, op) for p, v in d.items() if v == d[s] - 1 for op in OPS if _apply(A, B, p, op) == s)
        s, op = r.choice(choices); ops.append(op)
    return ops[::-1]


def _cycle(A, B, C, first):
    """「灌满 first → 倒进另一只 → 另一只满了就倒掉」的朴素模拟。

    单一方向未必最短；两个方向取短的那条，在全部 671650 个合法输入上都等于 BFS 的 K
    （2026-09-17 穷举核过），所以它既是另一种正确解，也是与 BFS 无关的 K 旁证。
    """
    other = 3 - first
    cap = {1: A, 2: B}
    state, ops, seen = (0, 0), [], set()
    while C not in state:
        if state in seen:
            return None
        seen.add(state)
        if state[first - 1] == 0: op = f"FILL({first})"
        elif state[other - 1] == cap[other]: op = f"DROP({other})"
        else: op = f"POUR({first},{other})"
        state = _apply(A, B, state, op); ops.append(op)
    return ops


def _shorter_cycle(A, B, C):
    got = [c for c in (_cycle(A, B, C, 1), _cycle(A, B, C, 2)) if c is not None]
    return min(got, key=len) if got else None


ALTERNATIVES = {
    "bfs_reversed_op_order": lambda A, B, C: _render(_bfs_path(A, B, C, OPS[::-1])),
    "random_shortest_path": lambda A, B, C: _render(_random_shortest(A, B, C)),
    "shorter_of_two_fill_pour_cycles": lambda A, B, C: _render(_shorter_cycle(A, B, C)),
}
WRONG = {
    "goal_only_in_pot_1": lambda A, B, C: _render(_bfs_path(A, B, C, goal=lambda s, C: s[0] == C)),
    "cycle_always_starting_from_pot_1": lambda A, B, C: _render(_cycle(A, B, C, 1)),
    "impossible_if_C_gt_min": lambda A, B, C: "impossible\n" if C > min(A, B) else _render(_bfs_path(A, B, C)),
    "space_after_comma": lambda A, B, C: _render(_bfs_path(A, B, C)).replace(",", ", "),
    "K_plus_one": lambda A, B, C: (lambda ops: _render(ops) if ops is None else f"{len(ops) + 1}\n" + "".join(o + "\n" for o in ops))(_bfs_path(A, B, C)),
    "capital_Impossible": lambda A, B, C: _render(_bfs_path(A, B, C)).replace("impossible", "Impossible"),
}


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
    cases = [SAMPLE] + [generate(NUMBER, seed) for seed in range(1, 40)]
    if len(set(cases)) != len(cases):
        raise SystemExit(f"两组输入撞了，数据必须互异：{cases}")
    differs = dict.fromkeys(ALTERNATIVES, False)
    rejected = dict.fromkeys(WRONG, 0)
    for index, case in enumerate(cases):
        if not valid(NUMBER, case):
            raise SystemExit(f"case {index} violates the input contract")
        A, B, C = map(int, case.split())
        answer = subprocess.run([sys.executable, str(REFERENCE)], input=case, text=True,
                                capture_output=True, timeout=120, check=True).stdout
        k, cyc = _k(A, B, C), _shorter_cycle(A, B, C)
        if answer.split("\n", 1)[0] != ("impossible" if k is None else str(k)) \
                or (cyc is None) != (k is None) or (cyc is not None and len(cyc) != k):
            raise SystemExit(f"case {index}: 参考解的 K 与朴素 BFS / 双向循环模拟不一致")
        if not check(case, answer, answer):
            raise SystemExit(f"case {index}: 参考解输出被 checker 拒绝")
        if index == 0 and not check(case, SAMPLE_OUT, answer):
            raise SystemExit("题面样例输出被 checker 拒绝")
        for name, fn in ALTERNATIVES.items():
            output = fn(A, B, C)
            if not check(case, output, answer):
                raise SystemExit(f"case {index}: 正确解 {name} 被 checker 拒绝")
            differs[name] |= output != answer
        for name, fn in WRONG.items():
            rejected[name] += not check(case, fn(A, B, C), answer)
        (out / f"{index}.in").write_text(case, encoding="utf-8")
        (out / f"{index}.out").write_text(answer, encoding="utf-8")
    if sum(differs.values()) < 2:          # 双向循环模拟恰好与参考解的扩展顺序同路，不要求它不同
        raise SystemExit(f"与 .out 不同的正确解不到两份，checker 没被真正考到：{differs}")
    if not all(rejected.values()):
        raise SystemExit(f"有错解一组都没被拒：{rejected}")
    print("wrong solutions rejected on:", rejected)


if __name__ == "__main__":
    _build()

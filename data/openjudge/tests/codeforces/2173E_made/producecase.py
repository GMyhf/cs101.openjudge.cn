#!/usr/bin/env python3
"""2173E Shiro's Mirror Duel：交互题隐藏数据（排列 + 硬币种子），参考解逐组经 judge.run_interactive 验证。

隐藏数据格式见 interactor.py 文档串。.out 只是占位（每组一行 n 与操作上限），交互器不读。
第 0 组 = 题面样例（剧本硬币 0 1 逐字复现 Note 的回应）。
"""
from __future__ import annotations

import itertools
import random
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(ROOT))
import judge  # noqa: E402

INTERACTOR = "tests/codeforces/2173E_made/interactor.py"
REFERENCE = HERE / "samplecode.py"
MAX_T, MAX_N, MAX_SUM = 100, 4000, 20000
SAMPLE_TESTS = [[5, 1, 3, 4, 2], [1, 2]]
SAMPLE_COINS = (7, [0, 1])


def render(tests, seed, coins=()):
    lines = [str(len(tests))]
    for p in tests:
        lines += [str(len(p)), " ".join(map(str, p))]
    lines.append(" ".join(map(str, [seed, len(coins), *coins])))
    return "\n".join(lines) + "\n"


def valid(text):
    try:
        v = list(map(int, text.split()))
        t, at, total = v[0], 1, 0
        if not 1 <= t <= MAX_T:
            return False
        for _ in range(t):
            n = v[at]
            p = v[at + 1:at + 1 + n]
            if not 1 <= n <= MAX_N or len(p) != n or sorted(p) != list(range(1, n + 1)):
                return False
            total += n
            at += 1 + n
        seed, k = v[at], v[at + 1]
        coins = v[at + 2:]
        return (total <= MAX_SUM and seed >= 0 and k == len(coins)
                and all(c in (0, 1) for c in coins) and text == render_back(text))
    except (IndexError, ValueError):
        return False


def render_back(text):
    v = list(map(int, text.split()))
    t, at, tests = v[0], 1, []
    for _ in range(t):
        n = v[at]
        tests.append(v[at + 1:at + 1 + n])
        at += 1 + n
    return render(tests, v[at], v[at + 2:])


# ---- 排列形状 ---------------------------------------------------------------

def rand_perm(r, n):
    p = list(range(1, n + 1))
    r.shuffle(p)
    return p


def orbit_shuffle(r, n, single_cycle=False, flip=0.5, all_asym=False):
    """p 由「镜像对」整体搬动而来：每对 {i, n+1-i} 的值落在另一对位置上。

    single_cycle：对的置换是一个长环（第二阶段最费操作）；all_asym：再把每对拆开，
    让第一阶段每个值对都要修（操作数期望最大）。"""
    m = n // 2
    order = list(range(1, m + 1))
    if single_cycle and m > 1:
        r.shuffle(order)
        target = {order[k]: order[(k + 1) % m] for k in range(m)}
    else:
        shuffled = order[:]
        r.shuffle(shuffled)
        target = dict(zip(order, shuffled))
    p = [0] * (n + 1)
    if n % 2:
        p[m + 1] = m + 1
    for i in range(1, m + 1):
        j = target[i]
        a, b = i, n + 1 - i
        if r.random() < flip:
            a, b = b, a
        p[j], p[n + 1 - j] = a, b
    p = p[1:]
    if all_asym and m >= 2:
        # 把每个镜像对的「右半边」整体循环移一格：任何一对都不再对称
        rights = [n - 1 - j for j in range(m)]
        vals = [p[k] for k in rights]
        vals = vals[1:] + vals[:1]
        for k, val in zip(rights, vals):
            p[k] = val
    return p


def reversed_perm(n):
    return list(range(n, 0, -1))


def centre_displaced(r, n):
    p = list(range(1, n + 1))
    c = (n + 1) // 2 - 1
    k = r.randrange(n)
    if k == c:
        k = 0
    p[c], p[k] = p[k], p[c]
    return p


def split_sum(r, total, lo, hi, count_max):
    sizes = []
    while total > 0 and len(sizes) < count_max:
        s = min(total, r.randint(lo, hi))
        sizes.append(s)
        total -= s
    return sizes


def generate(seed):
    r = random.Random(2173_0500 + seed * 7919)
    if seed == 1:      # n = 1..3 的全部排列 + 若干 n=4,5
        tests = [list(q) for n in (1, 2, 3) for q in itertools.permutations(range(1, n + 1))]
        while len(tests) < MAX_T:
            tests.append(rand_perm(r, r.choice((4, 5))))
    elif seed == 2:    # n = 4 全部排列 + n = 5 随机
        tests = [list(q) for q in itertools.permutations(range(1, 5))]
        tests += [rand_perm(r, 5) for _ in range(MAX_T - len(tests))]
    elif seed == 3:    # 最大 n，纯随机
        tests = [rand_perm(r, MAX_N) for _ in range(5)]
    elif seed == 4:    # 已排好序 / 完全逆序 / n=1 / n=2 逆序
        tests = [list(range(1, MAX_N + 1)), reversed_perm(MAX_N), reversed_perm(3999),
                 list(range(1, 3999 + 1)), [1], [2, 1], [1, 2], reversed_perm(3),
                 reversed_perm(4000 - 3 - 3)]
        tests = tests[:8] + [reversed_perm(20000 - sum(map(len, tests[:8])))]
    elif seed == 5:    # 奇数 n，中心被挪走
        tests = [rand_perm(r, 3999) if k % 2 else centre_displaced(r, 3999) for k in range(5)]
    elif seed == 6:    # t = 100，每组 n = 200 随机（每组固定开销 800 占比最小）
        tests = [rand_perm(r, 200) for _ in range(MAX_T)]
    elif seed == 7:    # 对整体搬动、单个长环（第二阶段操作最多）
        tests = [orbit_shuffle(r, MAX_N, single_cycle=True) for _ in range(5)]
    elif seed == 8:    # 每对都不对称 + 长环（两阶段都拉满）
        tests = [orbit_shuffle(r, MAX_N, single_cycle=True, all_asym=True) for _ in range(5)]
    elif seed == 9:    # 奇数 n 的镜像结构，中心不动；方向全反
        tests = [orbit_shuffle(r, 3999, flip=1.0) for _ in range(4)] + [orbit_shuffle(r, 4000, flip=0.0)]
    elif seed == 10:   # 随机 n、总和拉满
        sizes = split_sum(r, MAX_SUM, 1, MAX_N, MAX_T)
        tests = [rand_perm(r, s) for s in sizes]
    elif seed == 11:   # t = 100 个 n = 1（只需立刻 `!`）
        tests = [[1] for _ in range(MAX_T)]
    elif seed == 12:   # 小 n 各种镜像结构，n = 2..9
        tests = []
        for k in range(MAX_T):
            n = 2 + k % 8
            kind = k % 4
            if kind == 0:
                tests.append(orbit_shuffle(r, n, single_cycle=True))
            elif kind == 1:
                tests.append(orbit_shuffle(r, n, single_cycle=True, all_asym=True))
            elif kind == 2:
                tests.append(centre_displaced(r, n) if n % 2 else reversed_perm(n))
            else:
                tests.append(rand_perm(r, n))
    elif seed == 13:   # 只差一个对换 / 循环移一位
        n = MAX_N
        a = list(range(1, n + 1)); a[0], a[-1] = a[-1], a[0]
        b = list(range(2, n + 1)) + [1]
        c = list(range(1, n + 1)); c[1999], c[2000] = c[2000], c[1999]
        d = [n] + list(range(1, n))
        e = list(range(1, n + 1)); e[0], e[1] = e[1], e[0]
        tests = [a, b, c, d, e]
    elif seed == 14:   # 一组 n = 4000 与很多中等 n 混合
        tests = [orbit_shuffle(r, MAX_N, single_cycle=True, all_asym=True)]
        tests += [rand_perm(r, 160) for _ in range(99)]
    elif seed == 15:   # 左右半边整体互换（每个值都在镜像对的「另一侧」外）
        tests = []
        for n in (4000, 3999, 4000, 3999, 4000):
            h = n // 2
            if n % 2:
                tests.append(list(range(h + 2, n + 1)) + [h + 1] + list(range(1, h + 1)))
            else:
                tests.append(list(range(h + 1, n + 1)) + list(range(1, h + 1)))
    elif seed == 16:   # 块逆序：每 k 个一段反转
        tests = []
        for k, n in zip((2, 3, 7, 50, 1000), (4000, 4000, 3999, 4000, 3999)):
            p = []
            for s in range(0, n, k):
                p += list(range(min(n, s + k), s, -1))
            tests.append(p)
    elif seed == 17:   # 奇数 n 随机、镜像结构混合，n 取 3999 与 3997
        tests = [orbit_shuffle(r, 3999, single_cycle=True, all_asym=True),
                 centre_displaced(r, 3999), rand_perm(r, 3997),
                 orbit_shuffle(r, 3997, single_cycle=True), rand_perm(r, 4000)]
    elif seed == 18:   # 对的置换是许多 2-环（每步都能一次到位或恰好换回）
        tests = []
        for n in (4000,) * 5:
            m = n // 2
            p = [0] * (n + 1)
            for i in range(1, m + 1, 2):
                j = i + 1 if i + 1 <= m else i
                for src, dst in ((i, j), (j, i)):
                    a, b = src, n + 1 - src
                    if r.random() < 0.5:
                        a, b = b, a
                    p[dst], p[n + 1 - dst] = a, b
            tests.append(p[1:])
    elif seed == 19:   # 很多小随机 + 若干 n = 1、2
        sizes = [r.choice((1, 2, 3, r.randint(4, 400))) for _ in range(MAX_T)]
        tests = [rand_perm(r, s) for s in sizes]
    else:              # 最大 n 的镜像结构多组（多环），方向随机
        tests = [orbit_shuffle(r, MAX_N, all_asym=bool(k % 2)) for k in range(5)]
    return render(tests, r.randrange(10**9))


def run_reference(case):
    source = REFERENCE.read_text()
    with tempfile.TemporaryDirectory(prefix="cf2173e-") as tmp:
        cmd, fail = judge.prepare_program(Path(tmp), "python3", source)
        if fail:
            raise SystemExit(f"reference failed to prepare: {fail}")
        return judge.run_interactive(cmd, INTERACTOR, case.encode(), b"", Path(tmp),
                                     cpu_seconds=4, address_space_bytes=768 * 1024 * 1024,
                                     file_size_bytes=2 * 1024 * 1024)


def build():
    out = HERE / "data"
    out.mkdir(exist_ok=True)
    cases = [render(SAMPLE_TESTS, *SAMPLE_COINS)] + [generate(seed) for seed in range(1, 21)]
    if len(set(cases)) != len(cases):
        raise SystemExit("duplicate cases")
    for index, case in enumerate(cases):
        if not valid(case) or len(case) > 1_000_000:
            raise SystemExit(f"invalid case {index}")
        v = case.split()
        t, at, answer = int(v[0]), 1, []
        for _ in range(t):
            n = int(v[at]); at += 1 + n
            answer.append(f"{n} {(5 * n + 1600) // 2}")
        result = run_reference(case)
        if result["outcome"] != "accepted":
            raise SystemExit(f"reference not accepted on case {index}: {result['outcome']} {result['message']}")
        print(f"case {index}: {result['time_ms']} ms, {result['message']}", file=sys.stderr)
        (out / f"{index}.in").write_text(case, encoding="utf-8")
        (out / f"{index}.out").write_text("\n".join(answer) + "\n", encoding="utf-8")


if __name__ == "__main__":
    build()

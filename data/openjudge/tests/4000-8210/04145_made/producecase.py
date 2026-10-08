"""4145 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 30 组数据。

2026-10-07 审计加强：原 19 组每块 n 只有 2..20、每个文件 1..3 块，离 n<=1000 很远。
第 1..19 组保持原样，追加第 20..29 组：n=1000 多块满规模、k=1 与 k=n-1、
答案为 0（a 远小于 b）与 100、按 a/b 贪心丢最差几场会错的组、几百个小块的多组输入。
每组都用整数 Dinkelbach 求出精确最优比值，拒收 100·比值 小数部分离 .5 太近的块
（四舍五入规则在题面上没细说，也免得浮点二分的误差翻转结果），并核对参考解输出。

出处：build_001b
生成器与循环取自 scripts/build_001b.py（批次 001b），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 4145
SAMPLE_IN = '3 1\n5 0 2\n5 1 6\n4 2\n1 2 7 9\n5 6 7 9\n0 0\n'
SAMPLE_OUT = '83\n100\n'
REFERENCE_SOURCE = "# 蒋子轩23工学院\ndef can_achieve(target,a,b,k):\n    diffs=[a[i]-target*b[i] for i in range(len(a))]\n    diffs.sort()\n    #放弃k场考试后可以达到target\n    return sum(diffs[k:])>=0\ndef max_avg_score(k,a,b):\n    l,r=0,100\n    while r-l>1e-5:\n    \t#非整数二分\n        m=(l+r)/2\n        if can_achieve(m,a,b,k):\n            l=m\n        else:\n            r=m\n    return m*100\nwhile True:\n    n,k=map(int,input().split())\n    if n==0 and k==0:\n        break\n    a = list(map(int, input().split()))\n    b = list(map(int, input().split()))\n    print(f'{max_avg_score(k,a,b):.0f}')\n"

def g4145(r):
    parts = []
    for _ in range(r.randint(1, 3)):
        n = r.randint(2, 20); k = r.randint(1, n - 1)
        a = [r.randint(1, 1_000_000_000) for _ in range(n)]
        b = [x + r.randint(0, 1_000_000_000 - x) for x in a]
        parts.append(f"{n} {k}\n" + " ".join(map(str, a)) + "\n" + " ".join(map(str, b)))
    return "\n".join(parts) + "\n0 0\n"

def valid(text):
    """题面：多组数据，每组三行：「n k」、n 个 ai、n 个 bi；(1<=k<n<=1000)，
    (1<=ai<=bi<=10^9)；最后一行 0 0。整数间单个空格。

    题面写 1<=ai，但样例第一块 `5 0 2` 自己就有 ai=0（POJ 2976 原题是 0<=ai），
    所以 ai 放宽到 >=0，bi 仍要求 >=1。
    """
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if len(lines) < 4 or lines[-1] != "0 0" or (len(lines) - 1) % 3:
        return False

    def num(t, lo, hi):
        if not t.isdigit() or (t != "0" and t[0] == "0"):
            return None
        v = int(t)
        return v if lo <= v <= hi else None

    for i in range(0, len(lines) - 1, 3):
        head = lines[i].split(" ")
        if len(head) != 2:
            return False
        n, k = num(head[0], 2, 1000), num(head[1], 1, 999)
        if n is None or k is None or k >= n:
            return False
        a, b = lines[i + 1].split(" "), lines[i + 2].split(" ")
        if len(a) != n or len(b) != n:
            return False
        a = [num(t, 0, 10 ** 9) for t in a]
        b = [num(t, 1, 10 ** 9) for t in b]
        if None in a or None in b or any(x > y for x, y in zip(a, b)):
            return False
    return True


def exact_best(n, k, a, b):
    """整数 Dinkelbach：返回最优比值 (p, q)，即 Σa/Σb 的最大值（放弃恰好 k 场）。"""
    p, q = sum(a), sum(b)
    while True:
        keep = sorted(range(n), key=lambda i: a[i] * q - p * b[i], reverse=True)[:n - k]
        p2, q2 = sum(a[i] for i in keep), sum(b[i] for i in keep)
        if p2 * q <= p * q2:
            return p, q
        p, q = p2, q2


def safe_block(n, k, a, b):
    """100·p/q 的小数部分离 .5 至少 1e-4，四舍五入不会有争议。"""
    p, q = exact_best(n, k, a, b)
    frac = (100 * p) % q / q
    return abs(frac - 0.5) > 1e-4


def block(n, k, a, b):
    return f"{n} {k}\n" + " ".join(map(str, a)) + "\n" + " ".join(map(str, b))


def rand_block(r, n, k=None, amax=10 ** 9, bmax=10 ** 9):
    while True:
        kk = r.randint(1, n - 1) if k is None else k
        b = [r.randint(1, bmax) for _ in range(n)]
        a = [r.randint(1, min(x, amax)) for x in b]
        if safe_block(n, kk, a, b):
            return block(n, kk, a, b)


def greedy_trap_block(r):
    """按 a/b 从小到大丢 k 场的贪心会错的小块（n<=8，枚举核对）。"""
    from itertools import combinations
    while True:
        n = r.randint(3, 8); k = r.randint(1, n - 2)
        b = [r.randint(1, 50) for _ in range(n)]
        a = [r.randint(1, x) for x in b]
        best = max((sum(a[i] for i in c) * 10 ** 6 // sum(b[i] for i in c), c)
                   for c in combinations(range(n), n - k))[1]
        order = sorted(range(n), key=lambda i: a[i] / b[i])[k:]
        ga, gb = sum(a[i] for i in order), sum(b[i] for i in order)
        ba, bb = sum(a[i] for i in best), sum(b[i] for i in best)
        if ga * bb < ba * gb and round(100 * ga / gb) != round(100 * ba / bb) and safe_block(n, k, a, b):
            return block(n, k, a, b)


def join(blocks):
    return "\n".join(blocks) + "\n0 0\n"


def build_cases():
    cases = [SAMPLE_IN] + [g4145(random.Random(NUMBER + i)) for i in range(1, 20)]
    R = random.Random
    cases.append(join([rand_block(R(4145020 + j), 1000) for j in range(10)]))         # 20：10 块满规模
    cases.append(join([rand_block(R(4145021 + j), 1000, 999) for j in range(5)]))     # 21：k=n-1，只留一场
    cases.append(join([rand_block(R(4145022 + j), 1000, 1) for j in range(5)]))       # 22：k=1
    cases.append(join([block(1000, 500, [1] * 1000, [10 ** 9] * 1000),                # 23：答案 0
                       block(2, 1, [1, 1], [10 ** 9, 10 ** 9 - 1])]))
    cases.append(join([block(1000, 3, [10 ** 9] * 1000, [10 ** 9] * 1000),            # 24：答案 100
                       block(3, 2, [1, 999999999, 7], [2, 10 ** 9, 7])]))
    cases.append(join([greedy_trap_block(R(4145025 + j)) for j in range(30)]))        # 25：贪心陷阱
    cases.append(join([rand_block(R(4145026 + j), 2, 1, 100, 100) for j in range(50)]))  # 26：n=2,k=1
    cases.append(join([rand_block(R(4145027 + j), R(j).randint(2, 12)) for j in range(300)]))  # 27：多块
    cases.append(join([rand_block(R(4145028 + j), 1000, None, 10 ** 6, 10 ** 6) for j in range(10)]))  # 28
    cases.append(join([rand_block(R(4145029 + j), R(j).randint(900, 1000)) for j in range(10)]))  # 29
    return cases

def exact_answers(content):
    """逐块用精确比值四舍五入（半数向上），只用于核对参考解。"""
    t = content.split(); i = 0; out = []
    while True:
        n, k = int(t[i]), int(t[i + 1]); i += 2
        if n == 0 and k == 0:
            return out
        a = list(map(int, t[i:i + n])); b = list(map(int, t[i + n:i + 2 * n])); i += 2 * n
        p, q = exact_best(n, k, a, b)
        out.append(str((200 * p + q) // (2 * q)))


def solve_reference(content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE)
        handle.flush()
        result = subprocess.run(["python3", handle.name], input=content, text=True,
                                capture_output=True, timeout=120, check=True)
    return result.stdout


def main():
    cases = build_cases()
    assert cases[0] == SAMPLE_IN, "第 0 组必须是题面样例"
    assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split(), "参考解法跑不出样例输出"
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    assert len(set(cases)) == len(cases), "组间不得重复"
    for index, content in enumerate(cases):
        assert valid(content), f"第 {index} 组越出题面约束"
        out = solve_reference(content)
        assert out.split() == exact_answers(content), f"第 {index} 组参考解与精确解不符"
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(out, encoding="utf-8")


if __name__ == "__main__":
    main()

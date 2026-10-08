"""5467 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 40 组数据。

出处：build_001b
生成器与循环取自 scripts/build_001b.py（批次 001b），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 5467
SAMPLE_IN = '2\n-1 17 2 20 5 9 -7 7 10 4 22 2 -15 0 16 5 0 -1\n2 19 7 7 3 17 4 4 15 10 -10 5 13 2 -7 0 8 -8\n-1 17 2 23 22 2 6 8 -4 7 -18 0 1 5 21 4 0 -1\n12 7 -7 5 3 17 23 4 15 10 -10 5 13 5 2 19 9 -7\n'
SAMPLE_OUT = '[ 2 20 ] [ 2 19 ] [ 2 17 ] [ 15 10 ] [ 5 9 ] [ 6 5 ] [ 14 4 ] [ 35 2 ] [ -22 0 ]\n[ 2 23 ] [ 2 19 ] [ 2 17 ] [ 15 10 ] [ 6 8 ] [ 8 7 ] [ -3 5 ] [ 44 4 ] [ 22 2 ] [ -18 0 ]\n'
REFERENCE_SOURCE = "#23n2300011072(X)\nfrom collections import defaultdict\ndef add(a):\n    i=0\n    while 1:\n        m,n=a[i],a[i+1]\n        if n<0:\n            break\n        res[n]+=m\n        i+=2\nfor _ in range(int(input())):\n    res=defaultdict(int)\n    add(list(map(int,input().split())))\n    add(list(map(int,input().split())))\n    for i in sorted(res,reverse=True):\n        if res[i]!=0:\n            print(f'[ {res[i]} {i} ] ',end='')\n    print()\n"

def g5467(r):
    groups = r.randint(2, 5)
    lines = [str(groups)]
    for _ in range(groups * 2):
        exponents = r.sample(range(0, 50), r.randint(2, 10))
        pairs = []
        for exponent in exponents:
            pairs.append((str(r.randint(-30, 30) or 1), str(exponent)))
        r.shuffle(pairs)
        pairs.append((str(r.randint(1, 30)), str(-r.randint(1, 9))))
        lines.append(" ".join(value for pair in pairs for value in pair))
    return "\n".join(lines) + "\n"

# 题面：第一行 n（1 < n < 100），其后 2n 行，每行若干「系数 幂数」整数对，
# 以第一个幂数为负的整数对结束（该对不参与计算），每行长度小于 300。
def valid(text):
    if not text.endswith("\n") or "\r" in text:
        return False
    lines = text[:-1].split("\n")
    def is_int(t):
        u = t[1:] if t[:1] == "-" else t
        return u.isdigit()
    if not is_int(lines[0]) or lines[0] != lines[0].strip():
        return False
    n = int(lines[0])
    if not (1 < n < 100) or len(lines) != 2 * n + 1:
        return False
    for ln in lines[1:]:
        if len(ln) >= 300:
            return False
        toks = ln.split(" ")
        if not toks or any(not is_int(t) for t in toks) or len(toks) % 2:
            return False
        exps = [int(t) for t in toks[1::2]]
        if exps[-1] >= 0 or any(e < 0 for e in exps[:-1]):
            return False
    return True


def poly_line(r, exps, coef_hi, zero_coef=False):
    """按给定幂数序列造一行，长度控制在 300 以内。"""
    pairs = []
    for e in exps:
        c = r.randint(-coef_hi, coef_hi)
        if c == 0 and not zero_coef:
            c = 1
        pairs.append((c, e))
    while True:
        term = (r.randint(-coef_hi, coef_hi), -r.randint(1, 1000))
        ln = " ".join(f"{c} {e}" for c, e in pairs + [term])
        if len(ln) < 300:
            return ln, pairs
        pairs.pop()


def g5467_hard(r, kind):
    n = {"max": 99, "min": 2}.get(kind, r.randint(2, 99))
    lines = [str(n)]
    for _ in range(n):
        mode = kind if kind in ("cancel", "dup", "big") else r.choice(["long", "cancel", "dup", "zero", "big", "same"])
        if mode == "big":
            exps = r.sample(range(0, 10**6), r.randint(1, 15))
            a, pa = poly_line(r, exps, 10**6)
            b, _ = poly_line(r, r.sample(range(0, 10**6), r.randint(1, 15)) + [e for _, e in pa[:3]], 10**6)
        elif mode == "cancel":
            # 第二行把第一行的项全部或大部分抵消，可能整行输出为空
            exps = r.sample(range(0, 100), r.randint(1, 20))
            a, pa = poly_line(r, exps, 50)
            keep = [] if r.random() < 0.5 else r.sample(range(0, 100), r.randint(1, 3))
            neg = [(-c, e) for c, e in pa]
            r.shuffle(neg)
            b = " ".join(f"{c} {e}" for c, e in neg + [(r.randint(1, 9), e) for e in keep] + [(r.randint(-9, 9), -1)])
        elif mode == "dup":
            # 同一行里幂数重复出现，需要先合并
            exps = [r.randint(0, 8) for _ in range(r.randint(5, 40))]
            a, _ = poly_line(r, exps, 20, zero_coef=True)
            b, _ = poly_line(r, [r.randint(0, 8) for _ in range(r.randint(1, 40))], 20, zero_coef=True)
        elif mode == "zero":
            # 含系数为 0 的项，以及常数项（幂 0）
            a, _ = poly_line(r, r.sample(range(0, 30), r.randint(1, 15)) + [0], 3, zero_coef=True)
            b, _ = poly_line(r, r.sample(range(0, 30), r.randint(1, 15)), 3, zero_coef=True)
        elif mode == "same":
            # 只有一项
            e = r.randint(0, 1000)
            a, _ = poly_line(r, [e], 100)
            b, _ = poly_line(r, [r.choice([e, r.randint(0, 1000)])], 100)
        else:
            a, _ = poly_line(r, r.sample(range(0, 1000), 60), 99)
            b, _ = poly_line(r, r.sample(range(0, 1000), 60), 99)
        if r.random() < 0.5:
            a, b = b, a
        assert len(a) < 300 and len(b) < 300
        lines += [a, b]
    return "\n".join(lines) + "\n"


def build_cases():
    base = [SAMPLE_IN] + [g5467(random.Random(NUMBER + i)) for i in range(1, 20)]
    kinds = ["min", "max", "max", "cancel", "dup", "big"] + ["mix"] * 14
    extra = [g5467_hard(random.Random(NUMBER * 100 + i), k) for i, k in enumerate(kinds)]
    return base + extra

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
    for index, content in enumerate(cases):
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")


if __name__ == "__main__":
    main()

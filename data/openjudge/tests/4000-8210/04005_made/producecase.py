"""4005 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001a
生成器与循环取自 scripts/build_001a.py（批次 001a），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 4005
SAMPLE_IN = '3\n92 83 71\n95 87 74\n2\n20 20\n20 20\n2\n20 19\n22 18\n0\n'
SAMPLE_OUT = '9 5\n4 4\n4 4\n'
REFERENCE_SOURCE = 'def get_max_profit(a1, a2):\n    la1 = 0\n    ra1 = len(a1) - 1\n    la2 = 0\n    ra2 = len(a2) - 1\n    ans_max = 0\n    ans_min = 0\n\n    while la2 <= ra2:\n        if a2[la2] > a1[la1]:\n            ans_max += 3\n            ans_min += 1\n            la1 += 1\n            la2 += 1\n        elif a2[ra2] > a1[ra1]:\n            ans_max += 3\n            ans_min += 1\n            ra1 -= 1\n            ra2 -= 1\n        else:\n            if a2[la2] < a1[ra1]:\n                ans_max += 1\n                ans_min += 3\n            elif a2[la2] == a1[ra1]:\n                ans_max += 2\n                ans_min += 2\n\n            la2 += 1\n            ra1 -= 1\n\n    return ans_max, ans_min\n\n\nwhile True:\n    n = int(input())\n    if n == 0:\n        break\n\n    *C, = map(int, input().split())\n    *S, = map(int, input().split())\n    C.sort()\n    S.sort()\n\n    ans_max, _ = get_max_profit(C, S)\n    _, ans_min = get_max_profit(S, C)\n\n    print(ans_max, ans_min)\n'

def g4005(r):
    lines = []
    for _ in range(r.randint(2, 5)):
        n = r.randint(1, 12)
        lines += [str(n), " ".join(str(r.randint(1, 100)) for _ in range(n)), " ".join(str(r.randint(1, 100)) for _ in range(n))]
    return "\n".join(lines + ["0"]) + "\n"

def valid(text):
    """题面契约：多组（< 50 组），每组 n(1<=n<=1000) 一行、C 的 n 个整数一行、S 的 n 个整数一行，最后一行 0。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")

    def is_int(tok):
        return tok.lstrip("-").isdigit() and tok not in ("-",) and (tok.lstrip("-") == "0" or not tok.lstrip("-").startswith("0")) and tok != "-0"

    p = groups = 0
    while True:
        if p >= len(lines):
            return False
        head = lines[p]
        if not head.isdigit() or (head != "0" and head.startswith("0")):
            return False
        n = int(head)
        p += 1
        if n == 0:
            break
        if not 1 <= n <= 1000 or p + 2 > len(lines):
            return False
        for row in lines[p:p + 2]:
            toks = row.split(" ")
            if len(toks) != n or not all(is_int(t) for t in toks):
                return False
        p += 2
        groups += 1
    return p == len(lines) and 1 <= groups < 50


def fmt(groups):
    lines = []
    for c, s in groups:
        assert len(c) == len(s)
        lines += [str(len(c)), " ".join(map(str, c)), " ".join(map(str, s))]
    return "\n".join(lines + ["0"]) + "\n"


def extra_cases():
    """补强：n=1000 满规模、49 组上限、大量相等点数、n=1 三种胜负、一方全胜、负数与 0。"""
    r = random.Random(40050)
    R = lambda lo, hi, n: [r.randint(lo, hi) for _ in range(n)]
    out = []
    out.append(fmt([(R(1, 10 ** 6, 1000), R(1, 10 ** 6, 1000))]))
    out.append(fmt([(R(1, 50, 1000), R(1, 50, 1000)) for _ in range(49)]))
    out.append(fmt([([5], [5]), ([5], [6]), ([6], [5]), ([7] * 1000, [7] * 1000),
                    (list(range(1, 1001)), list(range(2, 1002))),
                    (list(range(2, 1002)), list(range(1, 1001)))]))
    out.append(fmt([(R(1, 5, k), R(1, 5, k)) for k in [r.randint(1, 12) for _ in range(49)]]))
    out.append(fmt([(R(-1000, 1000, 1000), R(-1000, 1000, 1000)) for _ in range(5)] +
                   [(R(-3, 3, 12), R(-3, 3, 12)) for _ in range(10)]))
    a = sorted(R(1, 200, 1000)); b = sorted(R(1, 200, 1000), reverse=True)
    out.append(fmt([(a, b), (b, a), (a, list(a))]))
    # 田忌赛马型：S 的最小牌只略小，于是「拿最小去换对方最大」和「平局」要分清
    tj = []
    for _ in range(40):
        k = r.randint(2, 12)
        base = R(1, 8, k)
        tj.append((base, [x + r.choice([-1, 0, 0, 1]) for x in base]))
    out.append(fmt(tj))
    out.append(fmt([(R(1, 10 ** 9, 1000), R(1, 10 ** 9, 1000)) for _ in range(20)]))
    return out


def build_cases():
    return [SAMPLE_IN] + [g4005(random.Random(NUMBER + i)) for i in range(1, 20)] + extra_cases()

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
    assert len(set(cases)) == len(cases)
    for index, content in enumerate(cases):
        assert valid(content), index
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")


if __name__ == "__main__":
    main()

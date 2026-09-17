"""Codeforces 2146D1 checker (answers are not unique).

Written for this repository as a hand-off artifact; no external license.
python3 -I checker.py <input> <contestant_output> <reference_answer>; exit 0 = AC, 42 = WA.

For l = 0 the optimum is always r(r+1) (a|b <= a+b, equality iff a&b = 0, and a
permutation with a_i & i = 0 always exists), so the checker recomputes it from r and
never trusts the reference file.  Per test it requires: the printed value equals
r(r+1); exactly r+1 following integers forming a permutation of 0..r; and the real
sum of a_i | (i) equals the printed value.  No tokens may follow the last test.
"""
import sys


def wa(msg):
    print(msg)
    sys.exit(42)


def to_int(tok):
    # strict decimal integer, bounded length so garbage never costs time
    if not 0 < len(tok) <= 12:
        return None
    s = tok[1:] if tok[:1] == b"-" else tok
    if not s or not s.isdigit():
        return None
    return int(tok)


def main():
    inp = open(sys.argv[1], "rb").read().split()
    with open(sys.argv[2], "rb") as f:
        out = f.read().split()
    t = int(inp[0])
    p = 0
    total = len(out)
    for case in range(1, t + 1):
        r = int(inp[2 * case])
        n = r + 1
        if p >= total:
            wa(f"第 {case} 组测试：输出不完整")
        v = to_int(out[p]); p += 1
        if v is None:
            wa(f"第 {case} 组测试：最大值不是整数")
        best = r * (r + 1)
        if v != best:
            wa(f"第 {case} 组测试：给出的最大值不对")
        if p + n > total:
            wa(f"第 {case} 组测试：重排后的数组不足 n 个数")
        seen = bytearray(n)
        s = 0
        for i in range(n):
            x = to_int(out[p + i])
            if x is None or not 0 <= x <= r:
                wa(f"第 {case} 组测试：数组里有不在 [l, r] 范围内的数")
            if seen[x]:
                wa(f"第 {case} 组测试：数组不是 l..r 的重排（有重复）")
            seen[x] = 1
            s += x | i
        p += n
        if s != v:
            wa(f"第 {case} 组测试：按给出的数组算出的值与给出的最大值不符")
    if p != total:
        wa("输出里有多余的内容")
    sys.exit(0)


main()

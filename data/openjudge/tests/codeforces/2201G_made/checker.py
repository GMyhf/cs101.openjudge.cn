"""Special judge for Codeforces 2201G Codeforces Heuristic Contest 1001.

Written for this repository as a hand-off artifact; no external license.

Usage: python3 -I checker.py <input> <contestant_output> <reference_answer>
Exit 0 = accepted, 42 = wrong answer; first stdout line is shown to the student.

The contestant prints n strings of length n over {0,1}.  Let S be the set of 1s in
the Zebra Graph ((r1-r2)^2 + (c1-c2)^2 = 13, i.e. moves (+-2,+-3) and (+-3,+-2)).
Accepted iff the graph induced by S is a single cycle with |S| >= floor(n^2/e):
  * every vertex of S has exactly two neighbours in S (row bitsets, adder trick);
  * walking from one vertex along its neighbours returns after exactly |S| steps
    (so S is connected; a simple 2-regular connected graph is a cycle, |S| >= 3).
The reference answer is not used: any valid cycle is accepted.
"""
import sys
from decimal import Decimal, getcontext

WA = 42


def wrong(msg):
    print(msg)
    sys.exit(WA)


def threshold(n):
    getcontext().prec = 60
    e = Decimal("2.71828182845904523536028747135266249775724709369995957496696763")
    return int(Decimal(n * n) / e)          # int() truncates toward zero == floor here


def main():
    n = int(open(sys.argv[1], "rb").read().split()[0])
    try:
        toks = open(sys.argv[2], "rb").read().split()
    except OSError:
        toks = []
    if len(toks) != n:
        wrong(f"应输出 n 行 01 串，实际读到 {len(toks)} 个串")
    for tok in toks:
        if len(tok) != n or tok.strip(b"01"):
            wrong("每行必须是长度为 n、只含 0 和 1 的串")
    need = threshold(n)
    total = sum(tok.count(b"1") for tok in toks)
    if total < need:
        wrong(f"集合 S 只有 {total} 个点，少于要求的 floor(n^2/e) = {need}")

    full = (1 << n) - 1
    rows = [int(tok[::-1], 2) for tok in toks] + [0, 0, 0]      # rows[-1..-3] == 0
    for r in range(n):
        row = rows[r]
        if not row:
            continue
        ones = twos = three = 0
        for m in ((rows[r + 2] << 3), (rows[r + 2] >> 3), (rows[r - 2] << 3) if r >= 2 else 0,
                  (rows[r - 2] >> 3) if r >= 2 else 0, (rows[r + 3] << 2), (rows[r + 3] >> 2),
                  (rows[r - 3] << 2) if r >= 3 else 0, (rows[r - 3] >> 2) if r >= 3 else 0):
            m &= full
            three |= twos & m
            twos |= ones & m
            ones |= m
        if row & ~(twos & ~three):
            wrong("S 的导出子图不是环：有点在 S 中的邻居数不等于 2")

    # connectivity: walk the cycle on a padded grid
    w = n + 6
    grid = bytearray(w * w)
    start = -1
    for r, tok in enumerate(toks):
        base = (r + 3) * w + 3
        grid[base:base + n] = tok.replace(b"1", b"\x01").replace(b"0", b"\x00")
        if start < 0:
            c = tok.find(b"1")
            if c >= 0:
                start = base + c
    offs = (2 * w + 3, 3 * w + 2, -2 * w + 3, -3 * w + 2, 2 * w - 3, 3 * w - 2, -2 * w - 3, -3 * w - 2)
    prev, cur, steps = -1, start, 0
    while True:
        for o in offs:
            j = cur + o
            if grid[j] and j != prev:
                break
        prev, cur = cur, j
        steps += 1
        if cur == start or steps > total:
            break
    if steps != total:
        wrong("S 的导出子图由多个互不相连的环组成，不是一个环")
    print("答案正确")
    sys.exit(0)


main()

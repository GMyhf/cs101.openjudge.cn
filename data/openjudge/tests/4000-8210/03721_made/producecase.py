"""3721 和数 测试数据生成器：固定种子，重跑可逐字节复现 data/。

题面约束：两行，第一行 n（1 <= n <= 100），第二行 n 个不大于 10000 的正整数，
相邻两个整数之间用单个空格隔开。

2026-10 审计修正：原数据 n 只在 3~30、数值在 1~10000 里均匀随机，39 组里 35 组答案是 0，
「只输出 0」能过绝大多数组；n=1、n=100 都没出现。现在：
  - 边界 n=1、n=2、n=100、数值 10000；
  - 1..100（答案 98）、偶数列、小值域稠密列等答案很大的组；
  - 「x 恰好是某个数的两倍、但那个数只出现一次」的陷阱（把同一个数用两次的写法会多算），
    「一个数有多种拆法」（不 break、按对数计数的写法会多算）。
生成的数列内数值互不相同：题面没说重复值怎么计数，避开歧义（题面并未保证互异，valid 不查）。
"""
import random
import re
import subprocess
import tempfile
from pathlib import Path

REFERENCE_SOURCE = 'import sys\na=list(map(int,sys.stdin.read().split())); n=a[0]; v=a[1:1+n]; ans=0\nfor i,x in enumerate(v):\n    seen=set()\n    for j,y in enumerate(v):\n        if j!=i and x-y in seen: ans+=1; break\n        if j!=i: seen.add(y)\nprint(ans)'
SAMPLE_IN = '4\n1 2 3 4\n'
SAMPLE_OUT = '2\n'


def valid(text):
    if not re.fullmatch(r"[1-9]\d*\n[1-9]\d*( [1-9]\d*)*\n", text):
        return False
    first, second = text.split("\n")[:2]
    n = int(first)
    v = list(map(int, second.split(" ")))
    return 1 <= n <= 100 and len(v) == n and all(1 <= x <= 10000 for x in v)


def make(v):
    return f"{len(v)}\n" + " ".join(map(str, v)) + "\n"


def build_cases():
    cases = [SAMPLE_IN]
    fixed = [
        [5], [10000], [1, 2], [2, 4], [1, 2, 3], [2, 4, 6], [3, 1, 2], [5000, 10000],
        [1, 9999, 10000, 5000], list(range(1, 101)), list(range(2, 201, 2)),
        list(range(9901, 10001)), [1 << k for k in range(14)],
        list(range(100, 0, -1)),
    ]
    for v in fixed:
        c = make(v)
        if c not in cases:
            cases.append(c)
    # 斐波那契式：每个数都是前两个之和
    fib = [1, 2]
    while fib[-1] + fib[-2] <= 10000:
        fib.append(fib[-1] + fib[-2])
    cases.append(make(fib[::-1]))
    k = 0
    while len(cases) < 40:
        k += 1
        r = random.Random(3721 * 1000 + k)
        t = k % 4
        if t == 0:      # 满规模、全值域随机
            v = r.sample(range(1, 10001), 100)
        elif t == 1:    # 小值域稠密，答案大、一数多拆
            n = r.randint(5, 100)
            v = r.sample(range(1, r.randint(n, 2 * n + 10) + 1), n)
        elif t == 2:    # 构造：先取基数，再加入若干两两之和
            base = r.sample(range(1, 5001), r.randint(2, 40))
            sums = {a + b for a in base for b in base if a != b} - set(base)
            extra = r.sample(sorted(sums), min(len(sums), r.randint(1, 100 - len(base))))
            # 加入「两倍陷阱」：2x 但 x 只出现一次
            traps = [2 * x for x in base if 2 * x not in base and 2 * x not in extra][:3]
            v = base + extra + traps
            v = v[:100]
            r.shuffle(v)
        else:           # 中等规模随机
            n = r.randint(3, 100)
            v = r.sample(range(1, r.choice([100, 1000, 10000]) + 1), n)
        c = make(v)
        if c not in cases:
            cases.append(c)
    return cases


def main():
    cases = build_cases()
    assert cases[0] == SAMPLE_IN
    assert all(valid(c) for c in cases) and len(set(cases)) == len(cases)
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE)
        handle.flush()
        for index, content in enumerate(cases):
            result = subprocess.run(["python3", handle.name], input=content, text=True,
                                    capture_output=True, timeout=10, check=True)
            if index == 0:
                assert result.stdout.split() == SAMPLE_OUT.split()
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()

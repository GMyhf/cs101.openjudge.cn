import random
REFERENCE="# External reference: /practice/30085/statistics/\n# Accepted submission: 52831605\n# Source: http://cs101.openjudge.cn/practice/solution/52831605/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\n\ndef main():\n    # 读取所有输入数据\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n    \n    w = int(input_data[0])\n    n = int(input_data[1])\n    prices = [int(x) for x in input_data[2:2+n]]\n    \n    # 升序排序\n    prices.sort()\n    \n    left = 0\n    right = n - 1\n    group_count = 0\n    \n    # 双指针扫描\n    while left <= right:\n        if left == right:\n            # 只剩下一个纪念品，单独一组\n            group_count += 1\n            break\n        \n        if prices[left] + prices[right] <= w:\n            # 两个可以分在同一组\n            left += 1\n            right -= 1\n        else:\n            # 最贵的纪念品只能单独一组\n            right -= 1\n        \n        group_count += 1\n        \n    print(group_count)\n\nif __name__ == '__main__':\n    main()"
SAMPLE='100 \n9 \n90 \n20 \n20 \n30 \n50 \n60 \n70 \n80 \n90\n'
GENERATOR_NAME='g30085'
import re as _re

def valid(text):
    """题面：共 n+2 行；第一行 w（80 ≤ w ≤ 200）；第二行 n（1 ≤ n ≤ 3×10^4）；
    其后 n 行每行一个正整数 Pi（5 ≤ Pi ≤ w）。题面样例行末带空格，故允许行末空格。"""
    if not text.endswith('\n'):
        return False
    lines = [l.rstrip(' ') for l in text[:-1].split('\n')]
    if len(lines) < 2 or not all(_re.fullmatch(r'[1-9]\d*', l) for l in lines):
        return False
    w, n = int(lines[0]), int(lines[1])
    if not (80 <= w <= 200 and 1 <= n <= 30000) or len(lines) != n + 2:
        return False
    return all(5 <= int(p) <= w for p in lines[2:])

def _fmt(w, prices):
    return f"{w}\n{len(prices)}\n" + "\n".join(map(str, prices)) + "\n"

def g30085(r):
    # 旧版生成器：n ≤ 200；新数据见 build_cases()
    n = r.randint(1, 200); w = r.randint(80, 200); prices = [r.randint(5, w) for _ in range(n)]
    return f"{w}\n{n}\n" + "\n".join(map(str, prices)) + "\n"

def build_cases():
    r = random.Random(30085)
    N = 30000
    cases = [SAMPLE]
    cases += [_fmt(80, [5]), _fmt(200, [200]), _fmt(80, [80, 5]), _fmt(100, [50, 50]), _fmt(100, [50, 51]),
              _fmt(100, [60, 60, 40, 40]), _fmt(100, [10, 20, 30, 90, 80, 70])]
    cases.append(_fmt(80, [5] * N))                                       # 全最小 → N/2
    cases.append(_fmt(200, [200] * N))                                    # 全等于 w → N
    cases.append(_fmt(200, [r.randint(101, 200) for _ in range(N)]))      # 都超过 w/2 → N
    cases.append(_fmt(200, [100] * (N - 1)))                              # 恰好两两相加 = w，奇数个
    cases.append(_fmt(199, [r.randint(5, 99) for _ in range(N)]))         # 任意两件可配
    cases.append(_fmt(80, [r.randint(5, 80) for _ in range(N)]))
    cases.append(_fmt(200, [r.randint(5, 200) for _ in range(N)]))
    # 贪心易错：大的要和最小的配，相邻配对会错
    half = N // 2
    cases.append(_fmt(100, [r.randint(5, 30) for _ in range(half)] + [r.randint(70, 95) for _ in range(half)]))
    cases.append(_fmt(150, [r.choice([5, 145, 75, 76]) for _ in range(N)]))
    # 小规模随机（可暴力核对）
    for t in range(10):
        w = r.randint(80, 200)
        cases.append(_fmt(w, [r.randint(5, w) for _ in range(r.randint(1, 12))]))
    # 中等与大规模随机
    for t in range(13):
        w = r.choice([80, 200, r.randint(80, 200)])
        n = r.choice([r.randint(100, 3000), r.randint(10000, N), N])
        lo, hi = r.choice([(5, w), (w // 3, w), (5, w // 2), (w // 2 - 5, w // 2 + 5)])
        cases.append(_fmt(w, [r.randint(lo, hi) for _ in range(n)]))
    assert len(cases) == 40, len(cases)   # catalog.json 登记了 0..39 共 40 组
    return cases

from pathlib import Path
import random, subprocess, sys, tempfile
REFERENCE = REFERENCE
def solve(text):
    with tempfile.TemporaryDirectory(prefix='producecase-run-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        result=subprocess.run([sys.executable, str(p)], input=text, text=True, capture_output=True, timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=build_cases()
    assert all(valid(c) for c in cases)
    for i, case in enumerate(cases):
        (data/f'{i}.in').write_text(case); (data/f'{i}.out').write_text(solve(case))
if __name__=='__main__': main()

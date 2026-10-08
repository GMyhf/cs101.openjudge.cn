import random
REFERENCE="# External reference: /practice/29750/statistics/\n# Accepted submission: 52710073\n# Source: http://cs101.openjudge.cn/practice/solution/52710073/\n# License: not declared on the submission page; no license is inferred.\n\nn = int(input())\na = [*map(int, input().split())]\na = [0] + a\nnum = ['', 'A', 'B', 'C']\ndef f(n, l, m, r): # n代表当前移动的是第n个圆盘\n    if n == 0:\n        return\n    if (l, r) in [(1, 2), (2, 1), (2, 3), (3, 2)] or a[n] == 0:\n        f(n-1, l, r, m)\n        print(f'moving disk {n} from {num[l]} to {num[r]}')\n        f(n-1, m, l, r)\n    else:\n        f(n-1, l, m, r)\n        print(f'moving disk {n} from {num[l]} to {num[m]}')\n        f(n-1, r, m, l)\n        print(f'moving disk {n} from {num[m]} to {num[r]}')\n        f(n-1, l, m, r)\nf(n, 1, 2, 3)"
SAMPLE='2\n0 1\n'
GENERATOR_NAME='g29750'
def g29750(r):
    n = r.randint(1, 11); return f"{n}\n" + " ".join(str(r.randint(0, 1)) for _ in range(n)) + "\n"


def valid(text):
    """题面契约：第一行正整数 n；第二行恰 n 个 0/1，单空格分隔。题面未给 n 的上限，只核格式。"""
    import re
    m = re.fullmatch(r'([1-9][0-9]*)\n([01]( [01])*)\n', text)
    return bool(m) and len(m.group(2).split(' ')) == int(m.group(1))

# 原随机组中第 14/32/39 组与前面重复，换成构造组（输出均 <= 2MB）
EXTRA = {
    14: "10\n" + " ".join(["1"] * 10) + "\n",          # 全黄金：3^10-1 步
    32: "15\n" + " ".join(["0"] * 15) + "\n",          # 全普通：2^15-1 步
    39: "12\n" + "1 0 1 0 0 0 0 0 0 0 0 1" + "\n",
}
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
    cases=[SAMPLE]+[EXTRA.get(seed) or globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1, 40)]
    assert len(set(cases)) == len(cases)
    for i, case in enumerate(cases):
        assert valid(case), i
    for i, case in enumerate(cases):
        (data/f'{i}.in').write_text(case); (data/f'{i}.out').write_text(solve(case))
if __name__=='__main__': main()

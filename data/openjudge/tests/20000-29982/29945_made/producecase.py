import random
REFERENCE='# External reference: /practice/29945/statistics/\n# Accepted submission: 52733426\n# Source: http://cs101.openjudge.cn/practice/solution/52733426/\n# License: not declared on the submission page; no license is inferred.\n\nn = int(input())\nwhile n != 1:\n    if n % 2 == 1:\n        nxt = n * 3 + 1\n        print(f"{n}*3+1={nxt}")\n    else:\n        nxt = n // 2\n        print(f"{n}/2={nxt}")\n    n = nxt\nprint("End")'
SAMPLE='5\n'
GENERATOR_NAME='g29945'
def g29945(r): return f"{r.randint(1, 100000)}\n"

from pathlib import Path
import random, subprocess, sys, tempfile


def valid(text):
    """题面契约：一行一个正整数 n，n <= 2,000,000。"""
    if not text.endswith("\n") or text.count("\n") != 1:
        return False
    s = text[:-1]
    return s.isdigit() and s == str(int(s)) and 1 <= int(s) <= 2000000


# 追加：原 40 组 n 全在 1e5 以内，也没有 n=1（直接 End 的分支）。
# 1723519 是 2e6 内步数最多的（556 步）；1988859 的轨迹峰值 156914378224 超过 2^32，
# 卡 32 位整型；704511 峰值 56991483520；2^20 一路折半；2000000 是上界。
EXTRA = [f"{v}\n" for v in (1, 2, 3, 27, 1048576, 2000000, 1999999,
                             1723519, 1988859, 704511, 837799, 1564063)]
REFERENCE = REFERENCE
def solve(text):
    with tempfile.TemporaryDirectory(prefix='producecase-run-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        result=subprocess.run([sys.executable, str(p)], input=text, text=True, capture_output=True, timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1, 40)]
    cases+=EXTRA
    assert all(valid(c) for c in cases) and len(set(cases)) == len(cases)
    for i, case in enumerate(cases):
        (data/f'{i}.in').write_text(case); (data/f'{i}.out').write_text(solve(case))
if __name__=='__main__': main()

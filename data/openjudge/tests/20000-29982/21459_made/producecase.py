import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/21459/\n# Accepted submission: 52832820\n# Source: http://cs101.openjudge.cn/practice/solution/52832820/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\n\ndef solve():\n    # 读取输入的正整数\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n    x = int(input_data[0])\n    \n    # 当 x 大于 1 时，持续进行变换\n    while x > 1:\n        if x % 2 == 1:\n            next_x = x * 3 + 1\n            print(f"{x}*3+1={next_x}")\n        else:\n            next_x = x // 2\n            print(f"{x}/2={next_x}")\n        # 更新 x 的值\n        x = next_x\n\nif __name__ == \'__main__\':\n    solve()'
SAMPLE='3\n'
GENERATOR_NAME='g21459'


def valid(text):
    """题面：一个正整数 x (x>1)。题面没给上界，只核单个整数且 >1。"""
    t = text.split()
    if len(t) != 1 or len(text.strip().split('\n')) != 1:
        return False
    try:
        return int(t[0]) > 1
    except ValueError:
        return False


# 边界组：最小 x=2、2 的幂、27（111 步）、1e5 内最长链 77031 与最高峰 77671（峰值 1570824736 < 2^31）
SPECIALS = ['2\n', '4\n', '27\n', '1023\n', '65536\n', '77031\n', '77671\n', '99999\n']


def seeded_cases():
    out = []
    for s in range(1, 40):
        c = g21459(random.Random(s))
        k = 1
        while c in out or c == SAMPLE:   # 原先第 35 组与第 29 组重复，重抽
            c = g21459(random.Random(s + 1000 * k)); k += 1
        out.append(c)
    return out
def g21459(r):
    return f"{r.randint(2, 1000)}\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+seeded_cases()+SPECIALS
    assert all(valid(c) for c in cases) and len(set(cases)) == len(cases)
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()

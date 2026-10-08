import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='import sys\n\n\ndef count_ways(m, n):\n    # 边界条件\n    if m == 0 or n == 1:\n        return 1\n\n    # 苹果数少于盘子数\n    if m < n:\n        return count_ways(m, m)\n\n    # 苹果数大于等于盘子数：有空盘子 + 没有空盘子\n    return count_ways(m, n - 1) + count_ways(m - n, n)\n\n\ndef main():\n    # 读取所有输入\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n\n    m = int(input_data[0])\n    n = int(input_data[1])\n\n    # 计算并输出结果\n    print(count_ways(m, n))\n\n\nif __name__ == "__main__":\n    main()\n'
SAMPLE='7 3\n'
GENERATOR_NAME='g21006'


def valid(text):
    """题面：输入苹果个数 M 和盘子个数 N，0<=M，1<=N<=10（M 无上界，只核非负整数）。"""
    t = text.split()
    if len(t) != 2:
        return False
    try:
        m, n = int(t[0]), int(t[1])
    except ValueError:
        return False
    return m >= 0 and 1 <= n <= 10


# 边界组：M=0、N=1、M<N、M=N、最大规模 100 10
SPECIALS = ['0 1\n', '0 10\n', '1 1\n', '1 10\n', '10 1\n', '9 10\n', '100 10\n', '99 9\n']
def g21006(r):
    n = r.randint(1, 10)
    return f"{r.randint(0, 100)} {n}\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+[g21006(random.Random(s)) for s in range(1, 40)]+SPECIALS
    assert all(valid(c) for c in cases) and len(set(cases)) == len(cases)
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()

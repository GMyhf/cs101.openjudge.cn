import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='import sys\n\n\ndef count_ways(m, n):\n    # 边界条件\n    if m == 0 or n == 1:\n        return 1\n\n    # 苹果数少于盘子数\n    if m < n:\n        return count_ways(m, m)\n\n    # 苹果数大于等于盘子数：有空盘子 + 没有空盘子\n    return count_ways(m, n - 1) + count_ways(m - n, n)\n\n\ndef main():\n    # 读取所有输入\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n\n    m = int(input_data[0])\n    n = int(input_data[1])\n\n    # 计算并输出结果\n    print(count_ways(m, n))\n\n\nif __name__ == "__main__":\n    main()\n'
SAMPLE='7 3\n'
GENERATOR_NAME='g21006'
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
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()

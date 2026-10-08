import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE="# External reference: statistics page /practice/23556/\n# Accepted submission: 52832495\n# Source: http://cs101.openjudge.cn/practice/solution/52832495/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\n\ndef solve():\n    # 从标准输入读取荷叶数量 n\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n    n = int(input_data[0])\n    \n    # 边界情况处理\n    if n == 1:\n        print(1)\n        return\n    if n == 2:\n        print(2)\n        return\n    \n    # 使用滚动变量优化空间复杂度到 O(1)\n    a, b = 1, 2\n    for _ in range(3, n + 1):\n        a, b = b, a + b\n        \n    print(b)\n\nif __name__ == '__main__':\n    solve()"
SAMPLE='3\n'
GENERATOR_NAME='g23556'
def valid(text):
    """题面契约：只有一行，一个整数 n，1 <= n <= 1000。"""
    if not text.endswith("\n") or text.count("\n") != 1:
        return False
    t = text[:-1]
    return t.isdigit() and t == str(int(t)) and 1 <= int(t) <= 1000
def g23556(r): return f"{r.randint(1,1000)}\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    # 2026-10 补强：原 39 组纯随机，没有 n=1、n=2 两个边界，也没有上限 n=1000，且 562 重复了一次。
    # 现在固定放入 1、2、4（题面样例 2）、999、1000，其余随机且两两不同，总组数仍为 40。
    cases=[SAMPLE]+['1\n','2\n','4\n','999\n','1000\n']
    s=1
    while len(cases)<40:
        c=globals()[GENERATOR_NAME](random.Random(s)); s+=1
        if c not in cases: cases.append(c)
    assert all(valid(c) for c in cases)
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()

import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/23654/\n# Accepted submission: 52485897\n# Source: http://cs101.openjudge.cn/practice/solution/52485897/\n# License: not declared on the submission page; no license is inferred.\n\nx=int(input())\nlis=[]\nwhile True:\n    x+=1\n    lis=list(str(x))\n    zan=0\n    for i in range(4):\n        zan+=int(lis[i])\n    if zan==20:\n        print(x)\n        break'
SAMPLE='1892\n'
GENERATOR_NAME='g23654'
def valid(text):
    """题面契约：一行，一个整数 y，1000 <= y <= 9000。"""
    if not text.endswith("\n") or text.count("\n") != 1:
        return False
    t = text[:-1]
    return t.isdigit() and t == str(int(t)) and 1000 <= int(t) <= 9000
def g23654(r): return f"{r.randint(1000,9000)}\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    # 2026-10 补强：原 39 组纯随机，缺两端 1000、9000，缺「答案超过 9000」（题面提示特殊年号可能大于 9000），
    # 缺「y 本身就是特殊年号」（要严格大于），也缺题面样例 2。末 6 组换成固定值。
    fixed=['1000\n','9000\n','8930\n','2021\n','2099\n','1991\n']
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1, 40-len(fixed))]+fixed
    assert len(cases)==40 and len(set(cases))==40 and all(valid(c) for c in cases)
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()

import random, re, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/23741/\n# Accepted submission: 52296431\n# Source: http://cs101.openjudge.cn/practice/solution/52296431/\n# License: not declared on the submission page; no license is inferred.\n\nka=[0]*25\nka[1]=1\nfor i in range(2,25):\n    ka[i]=ka[i-1]*(4*i-2)//(i+1)\nn=int(input())\nprint(ka[n])'
SAMPLE='4\n'
GENERATOR_NAME='g23741'

def valid(text):
    """题面：一行一个正整数 n，0 < n < 25。"""
    lines=text.split('\n')
    if lines and lines[-1]=='': lines.pop()
    if len(lines)!=1: return False
    t=lines[0].split()
    if len(t)!=1 or not re.fullmatch(r'[0-9]+',t[0]): return False
    return 0<int(t[0])<25

def build_cases():
    # 值域只有 1..24：第 1..24 组逐个覆盖全部 n（含 n=1 与 n=24，C_20 起超出 32 位整型），
    # 其余组重点重复易错的大 n 与最小 n
    extra=[24,23,22,21,20,19,1,2,24,20,13,16,18,12,24]
    return [SAMPLE]+[f"{n}\n" for n in range(1,25)]+[f"{n}\n" for n in extra]
def g23741(r): return f"{r.randint(1,24)}\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=build_cases()
    assert len(cases)==40 and all(valid(c) for c in cases)
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()

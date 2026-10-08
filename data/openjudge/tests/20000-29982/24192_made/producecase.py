import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/24192/\n# Accepted submission: 52740123\n# Source: http://cs101.openjudge.cn/practice/solution/52740123/\n# License: not declared on the submission page; no license is inferred.\n\nn, m = map(int, input().split())\ntotal = n * m\nans = (total + 1) // 2\nprint(ans)'
SAMPLE='5 7\n'
GENERATOR_NAME='g24192'
def g24192(r): return f"{r.randint(1,1000000)} {r.randint(1,1000000)}\n"
def valid(text):
    # 题面：一行两个整数 n m，一个空格分隔；1<=n,m<=1000000
    if not text.endswith('\n') or text.count('\n')!=1: return False
    parts=text[:-1].split(' ')
    if len(parts)!=2 or not all(p.isdigit() and p==str(int(p)) for p in parts): return False
    return all(1<=int(p)<=1000000 for p in parts)
# 边界：最小规模、单行/单列、满规模、奇×奇（答案要向上取整）、50% 子任务规模
EDGE=['1 1\n','1 2\n','2 1\n','1 1000000\n','1000000 1\n','1000000 1000000\n','999999 999999\n','999999 1000000\n','3 3\n','10000 9999\n','9999 9999\n']

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+(['8\n','9\n'] if GENERATOR_NAME == 'g22007' else [])+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1, 40)]+EDGE
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()

import random, re, subprocess, sys, tempfile
from pathlib import Path
REFERENCE="# External reference: statistics page /practice/26144/\n# Accepted submission: 51527404\n# Source: http://cs101.openjudge.cn/practice/solution/51527404/\n# License: not declared on the submission page; no license is inferred.\n\nn = int(input())\ntemp = []\nfor i in range(1, n+1):\n    for j in range(1, i+1):\n        temp.append(f'{j}x{i}={i*j}')\n    print(*temp)\n    temp = []"
SAMPLE='6\n'
EXTRA_CASE='7\n'
GENERATOR_NAME='g26144'
def g26144(r): return f"{r.randint(1, 9)}\n"

def valid(text):
    """题面：一个整数 n，1<=n<=9。"""
    return re.fullmatch(r'[1-9]\n', text) is not None

def build_cases():
    # 合法输入只有 n=1..9 共 9 种：第 0 组样例 6，其余每个 n 各一组，不重复
    return [SAMPLE]+[f"{n}\n" for n in (9, 1, 2, 3, 4, 5, 7, 8)]

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=60)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def scale_case():
    if EXTRA_CASE is not None: return EXTRA_CASE
    if GENERATOR_NAME == 'g26267': return 'A'*1000000+'\n'+'A'*1000+'\n'
    if GENERATOR_NAME == 'g26273': return ('abcdefghij'*10000)+'\n'
    if GENERATOR_NAME == 'g26835':
        e=[(i-1,i,float(i)) for i in range(1,99)]
        for i in range(99):
            for j in range(i+2,min(99,i+12)): e.append((i,j,float(10000+i*99+j)))
        return '99 %d\n'%len(e)+'\n'.join(f'{a} {b} {w:.3f}' for a,b,w in e)+'\n'
    if GENERATOR_NAME == 'g27311': return '100000\n'+' '.join(str(i%10001) for i in range(100000))+'\n'+' '.join(str((i*7)%10001) for i in range(100000))+'\n'
    return None
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=build_cases()
    assert all(valid(c) for c in cases) and len(set(cases))==len(cases)
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()

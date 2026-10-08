import random,subprocess,sys,tempfile
from pathlib import Path
import re

# ---- 输入契约（照题面）：每行 "target 字母串"，target 是小于 1200 万的正整数，
# 一个空格，然后 5~12 个互不相同的大写字母；最后一行 "0 END" 结束。
_INT=re.compile(r'(0|[1-9][0-9]*)$')
def valid(text):
    try:
        if not text.endswith('\n'): return False
        lines=text[:-1].split('\n')
        if len(lines)<2 or lines[-1]!='0 END': return False
        for ln in lines[:-1]:
            t=ln.split(' ')
            if len(t)!=2 or not _INT.match(t[0]): return False
            if not 0<int(t[0])<12_000_000: return False
            if not re.fullmatch(r'[A-Z]{5,12}',t[1]) or len(set(t[1]))!=len(t[1]): return False
        return True
    except Exception:
        return False

AL="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
def _f(w):
    v,x,y,z,u=(ord(c)-64 for c in w)
    return v-x**2+y**3-z**4+u**5

def _planted(r,letters):
    for _ in range(500):
        t=_f(r.sample(letters,5))
        if 0<t<12_000_000: return t
    return None

def _line(r,kind):
    n=r.choice([5,6,8,10,12,12,12])
    if kind=='hi': letters=r.sample(AL[14:],min(n,12))     # 偏大的字母，target 接近上限
    elif kind=='lo': letters=r.sample(AL[:12],n)
    else: letters=r.sample(AL,n)
    if kind=='nosol':
        t=r.randint(1,11_999_999)
    else:
        t=_planted(r,letters)
        if t is None: t=r.randint(1,11_999_999)
    return f"{t} {''.join(letters)}"

def generate(seed):
    r=random.Random(1248*1_000_003+seed)
    rows=[]
    if seed==1:   # 恰 5 个字母，且有解/无解各一
        rows=["1 EDCBA","2 ABCDE","11881376 ZABCD","11999999 ZYXWV"]
    elif seed==2: # 全 12 个字母都无解，最坏枚举量
        rows=[f"{r.randint(1,11_999_999)} {''.join(r.sample(AL,12))}" for _ in range(25)]
    elif seed==3: # 多解：同一组字母上多个 target，取字典序最大
        letters="ABCDEFGHIJKL";rows=[f"{t} {letters}" for t in (1,2,3,5,8,13,100,1000)]
        letters="".join(r.sample(AL,12));rows+=[f"{_planted(r,letters)} {letters}" for _ in range(8)]
    elif seed==4: # target 接近上限
        rows=[_line(r,'hi') for _ in range(20)]
    else:
        for _ in range(r.randint(1,30)):
            rows.append(_line(r,r.choice(['any','any','hi','lo','nosol'])))
    return "\n".join(rows)+"\n0 END\n"

REFERENCE='# External reference: http://cs101.openjudge.cn/practice/01248/statistics/\n# Accepted submission: 52718716\n# Source: http://cs101.openjudge.cn/practice/solution/52718716/\n# License: not declared on the submission page; no license is inferred.\n\nlt = {}\nfor i in range(1, 27):\n    lt[i] = chr(64 + i)\n\nch = []\na = 0\n\ndef find(visited, f):\n    if len(visited) == 5:\n        if a == f[0] - f[1]**2 + f[2]**3 - f[3]**4 + f[4]**5:\n            print(\'\'.join(map(lambda x: lt[x], f)))\n            return True\n        else:\n            return False\n    for i in ch:\n        if i not in visited and find(visited | {i}, f + [i]):\n            return True\n    return False\n\nwhile True:\n    sa, l = input().split()\n    a = int(sa)\n    if a == 0:\n        break\n    ch = sorted(map(lambda x: ord(x) - 64, l), reverse = True)\n    if not find(set(), []):\n        print("no solution")\n'
NUMBER=1248
SAMPLE='1 ABCDEFGHIJKL\n11700519 ZAYEXIWOVU\n3072997 SOUGHT\n1234567 THEQUICKFROG\n0 END\n'
CASES=40
def run(x):
 with tempfile.TemporaryDirectory() as t:
  p=Path(t)/'s.py';p.write_text(REFERENCE);q=subprocess.run([sys.executable,'-I',str(p)],input=x,text=True,capture_output=True,timeout=120)
  if q.returncode:raise SystemExit(q.stderr)
  return '\n'.join(line.rstrip() for line in q.stdout.rstrip().splitlines())+'\n'
def main():
 d=Path('data');d.mkdir(exist_ok=True)
 for p in d.glob('*'):p.unlink()
 for i,x in enumerate([SAMPLE]+[generate(s) for s in range(1, CASES)]):
  assert valid(x),i
  (d/f'{i}.in').write_text(x);(d/f'{i}.out').write_text(run(x))
if __name__=='__main__':main()

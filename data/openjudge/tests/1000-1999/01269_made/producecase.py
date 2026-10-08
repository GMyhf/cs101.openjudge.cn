import random,subprocess,sys,tempfile
from pathlib import Path
import re
from fractions import Fraction

# ---- 输入契约（照题面）：第一行 N（1..10），其后恰 N 行，每行 8 个整数 x1 y1 x2 y2 x3 y3 x4 y4，
# 取值在 -1000..1000；(x1,y1)≠(x2,y2)，(x3,y3)≠(x4,y4)；相交于一点时交点坐标也在 -1000..1000 内。
_INT=re.compile(r'-?(0|[1-9][0-9]*)$')
def valid(text):
    try:
        if not text.endswith('\n'): return False
        lines=text[:-1].split('\n')
        if not _INT.match(lines[0]): return False
        n=int(lines[0])
        if not 1<=n<=10 or len(lines)!=n+1: return False
        for ln in lines[1:]:
            t=ln.split(' ')
            if len(t)!=8 or any(not _INT.match(x) for x in t): return False
            t=list(map(int,t))
            if any(not -1000<=v<=1000 for v in t): return False
            if (t[0],t[1])==(t[2],t[3]) or (t[4],t[5])==(t[6],t[7]): return False
            p=_inter(t)   # 题面 All numbers required by this problem ... between -1000 and 1000：交点坐标也限制在此范围
            if p is not None and (abs(p[0])>1000 or abs(p[1])>1000): return False
        return True
    except Exception:
        return False

def _inter(t):
    x1,y1,x2,y2,x3,y3,x4,y4=t
    d=(x2-x1)*(y4-y3)-(y2-y1)*(x4-x3)
    if d==0: return None
    s=Fraction((x3-x1)*(y4-y3)-(y3-y1)*(x4-x3),d)
    return x1+s*(x2-x1),y1+s*(y2-y1)

def _safe(v):
    # 避开保留两位小数时的歧义：|v|<0.005（可能印出 -0.00）以及恰好/几乎落在 .xx5 上
    if abs(v)<Fraction(1,200): return False
    f=(abs(v)*100)%1
    return abs(f-Fraction(1,2))>Fraction(1,10**6)

def _ok(t):
    return all(-1000<=v<=1000 for v in t) and (t[0],t[1])!=(t[2],t[3]) and (t[4],t[5])!=(t[6],t[7])

def _pt(r,R): return [r.randint(-R,R),r.randint(-R,R)]

def _row(r,kind,R=1000):
    for _ in range(10000):
        if kind=='point':
            t=_pt(r,R)+_pt(r,R)+_pt(r,R)+_pt(r,R)
        elif kind in ('none','line'):
            g=r.randint(1,30);dx,dy=r.choice([(r.randint(-30,30),r.randint(-30,30)),(0,1),(1,0),(r.randint(1,9),r.randint(1,9))])
            if (dx,dy)==(0,0): continue
            a=_pt(r,R);k1,k2=r.sample(range(-40,41),2)
            if kind=='line': q=r.randint(-40,40);b=[a[0]+q*dx,a[1]+q*dy]   # 同一直线上的另一基点
            else: b=_pt(r,R)
            k3,k4=r.sample(range(-40,41),2)
            t=[a[0]+k1*dx,a[1]+k1*dy,a[0]+k2*dx,a[1]+k2*dy,b[0]+k3*dx,b[1]+k3*dy,b[0]+k4*dx,b[1]+k4*dy]
            if r.random()<.5: t=t[4:]+t[:4]
            if r.random()<.5: t=t[2:4]+t[0:2]+t[4:]
        elif kind=='axis':   # 竖直/水平线
            a=_pt(r,R);b=_pt(r,R)
            t=r.choice([[a[0],a[1],a[0],r.randint(-R,R)]+_pt(r,R)+_pt(r,R),
                        _pt(r,R)+_pt(r,R)+[b[0],b[1],b[0],r.randint(-R,R)],
                        [a[0],a[1],a[0],r.randint(-R,R),b[0],b[1],r.randint(-R,R),b[1]],
                        [a[0],a[1],r.randint(-R,R),a[1]]+_pt(r,R)+_pt(r,R)])
        if not _ok(t): continue
        p=_inter(t)
        if kind in ('none','line'):
            if p is not None: continue
            x1,y1,x2,y2,x3,y3,_,_=t
            col=(x2-x1)*(y3-y1)-(y2-y1)*(x3-x1)==0
            if col!=(kind=='line'): continue
        elif p is None or not (_safe(p[0]) and _safe(p[1])) or abs(p[0])>1000 or abs(p[1])>1000: continue
        return " ".join(map(str,t))
    raise RuntimeError(kind)

def generate(seed):
    r=random.Random(1269*1_000_003+seed)
    if seed==1: rows=[_row(r,'point',5)]
    elif seed==2: rows=[_row(r,'line') for _ in range(5)]+[_row(r,'none') for _ in range(5)]
    elif seed==3: rows=["0 0 1 1 1000 1000 -1000 -1000","-1000 -1000 1000 1000 -999 1000 1000 -1000",
                        "1000 -1000 -1000 1000 999 -999 -999 1000","0 0 0 1 1 0 1 1","0 0 1 0 0 1 1 1",
                        "3 0 3 7 3 -5 3 9","-1000 1000 1000 -999 -1000 -1000 1000 -999"]
    elif seed==4: rows=[_row(r,'axis') for _ in range(10)]
    else:
        n=r.choice([10,10,r.randint(1,10)])
        rows=[_row(r,r.choice(['point','point','point','none','line','axis']),r.choice([1000,1000,100,10])) for _ in range(n)]
    return f"{len(rows)}\n"+"\n".join(rows)+"\n"

REFERENCE="# External reference: http://cs101.openjudge.cn/practice/01269/statistics/\n# Accepted submission: 51703457\n# Source: http://cs101.openjudge.cn/practice/solution/51703457/\n# License: not declared on the submission page; no license is inferred.\n\nN = int(input())\nprint('INTERSECTING LINES OUTPUT')\nfor _ in range(N):\n    x1, y1, x2, y2, x3, y3, x4, y4 = map(int, input().split())\n    INF = float('inf')\n    k1, k2 = INF, INF\n    if x1 != x2:\n        k1 = (y1-y2)/(x1-x2)\n    if x3 != x4:\n        k2 = (y3-y4)/(x3-x4)\n    if k1 == k2:\n        if k1 == INF:\n            if x1 == x3:\n                print('LINE')\n            else:\n                print('NONE')\n        else:\n            b1 = (x2*y1-x1*y2)/(x2-x1)\n            b2 = (x4*y3-x3*y4)/(x4-x3)\n            if b1 == b2:\n                print('LINE')\n            else:\n                print('NONE')\n    else:\n        if k1 == INF:\n            b2 = (x4*y3-x3*y4)/(x4-x3)\n            y = k2*x1+b2\n            print(f'POINT {x1:.2f} {y:.2f}')\n        elif k2 == INF:\n            b1 = (x2*y1-x1*y2)/(x2-x1)\n            y = k1*x3+b1\n            print(f'POINT {x3:.2f} {y:.2f}')\n        else:\n            b1 = (x2*y1-x1*y2)/(x2-x1)\n            b2 = (x4*y3-x3*y4)/(x4-x3)\n            x = (b2-b1)/(k1-k2)\n            y = k1*x+b1\n            print(f'POINT {x:.2f} {y:.2f}')\nprint('END OF OUTPUT')\n"
NUMBER=1269
SAMPLE='5\n0 0 4 4 0 4 4 0\n5 0 7 6 1 0 2 3\n5 0 7 6 3 -6 4 -3\n2 0 2 27 1 5 18 5\n0 3 4 0 1 2 2 5\n'
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

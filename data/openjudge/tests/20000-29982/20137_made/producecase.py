import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/20137 statistics, Accepted solution 32302039.\n# Source: http://cs101.openjudge.cn/practice/solution/32302039/\n# Statistics: http://cs101.openjudge.cn/practice/20137/statistics/\n# License: not declared on submission page; no license inferred\nr,c=map(int,input().split())\na,b=map(int,input().split())\nd1,d2=map(int,input().split())\nflag=[[-1]*(c+3),*[[-1]+[0]*(c+1)+[-1] for _ in range(r+1)],[-1]*(c+3)]\na+=1;b+=1\nflag[a][b]=1\ncnt=1\nwhile(True):\n    a+=d1;b+=d2\n    if(flag[a][b]==1 or (flag[a-d1][b]==1 and flag[a][b-d2]==1)):\n        break\n    if(flag[a][b]==-1):\n        if(flag[a-d1][b]==-1 and flag[a][b-d2]==-1):\n            break\n        elif(a==0 or a==r+2):\n            a-=d1\n            if(flag[a][b]==1):\n                break\n            flag[a][b]=1;cnt+=1\n            if(flag[a+d1][b]==-1 and flag[a][b+d2]==-1):\n                break\n            d1=-d1\n        else:\n            b -= d2\n            if (flag[a][b] == 1):\n                break\n            cnt += 1\n            flag[a][b] = 1\n            if (flag[a + d1][b] == -1 and flag[a][b + d2] == -1):\n                break\n            d2=-d2\n    else: flag[a][b]=1;cnt+=1\nprint(cnt)\n\n'
SAMPLE='5 7\n0 1\n1 1\n'
GENERATOR_NAME='g20137'
SAMPLE2='6 4\n0 1\n1 1\n'


def valid(text):
    """题面：三行；r c（1<=r,c<=50）；起点 m n 在地图边界上（m=r 或 0，或 n=c 或 0）且不是顶点；
    方向 d1 d2 = ±1，且是「进入」地图的方向（上边界 d1=1、下边界 d1=-1、左边界 d2=1、右边界 d2=-1）。"""
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    if len(lines) != 3:
        return False
    try:
        v = [list(map(int, l.split())) for l in lines]
    except ValueError:
        return False
    if any(len(x) != 2 for x in v):
        return False
    (r, c), (m, n), (d1, d2) = v
    if not (1 <= r <= 50 and 1 <= c <= 50 and 0 <= m <= r and 0 <= n <= c):
        return False
    if d1 not in (1, -1) or d2 not in (1, -1):
        return False
    on_row, on_col = m in (0, r), n in (0, c)
    if on_row == on_col:                 # 不在边界上，或者是顶点
        return False
    if on_row:
        return d1 == (1 if m == 0 else -1)
    return d2 == (1 if n == 0 else -1)


def starts(rows, cols):
    out = []
    for y in range(1, cols):
        out += [(0, y, 1, 1), (0, y, 1, -1), (rows, y, -1, 1), (rows, y, -1, -1)]
    for x in range(1, rows):
        out += [(x, 0, 1, 1), (x, 0, -1, 1), (x, cols, 1, -1), (x, cols, -1, -1)]
    return out


def g20137(r):
    kind = r.randrange(4)
    if kind == 0:
        rows, cols = r.randint(1, 12), r.randint(1, 12)
    elif kind == 1:
        rows, cols = r.randint(40, 50), r.randint(40, 50)
    elif kind == 2:                       # 细长地图：r 或 c 很小
        rows, cols = r.choice([(1, r.randint(2, 50)), (r.randint(2, 50), 1), (2, r.randint(2, 50)), (r.randint(2, 50), 2)])
    else:
        rows, cols = r.randint(1, 50), r.randint(1, 50)
    st = starts(rows, cols)
    if not st:
        rows, cols = rows + 1, cols + 1
        st = starts(rows, cols)
    m, n, d1, d2 = r.choice(st)
    return f"{rows} {cols}\n{m} {n}\n{d1} {d2}\n"


FIXED = ['1 2\n0 1\n1 1\n', '2 1\n1 0\n1 1\n', '50 50\n0 1\n1 1\n', '50 50\n50 49\n-1 -1\n',
         '50 49\n0 1\n1 1\n', '49 50\n25 50\n-1 -1\n', '1 50\n1 25\n-1 1\n', '50 1\n30 1\n1 -1\n',
         '37 50\n0 18\n1 1\n', '50 37\n18 0\n-1 1\n',
         '50 49\n46 49\n-1 -1\n']                     # 全部合法输入里答案最大（148）的一组


def build_cases():
    cases = [SAMPLE, SAMPLE2] + FIXED
    seed = 1
    while len(cases) < 40:
        text = g20137(random.Random(seed)); seed += 1
        if text not in cases:
            cases.append(text)
    return cases

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        src=Path(d)/'main.py'; src.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(src)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=build_cases()
    assert all(valid(c) for c in cases)
    for i,text in enumerate(cases):
        (data/f'{i}.in').write_text(text); (data/f'{i}.out').write_text(run(text))
if __name__=='__main__': main()

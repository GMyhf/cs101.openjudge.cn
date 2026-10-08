import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/20121 statistics, Accepted solution 52495947.\n# Source: http://cs101.openjudge.cn/practice/solution/52495947/\n# Statistics: http://cs101.openjudge.cn/practice/20121/statistics/\n# License: not declared on submission page; no license inferred\nn=int(input())\nlis=[]\nfor i in range(n):\n    lis.append(input().split())\nvis=[[False for _ in range(n)] for _ in range(n)]\nans=""\nnow=0\nx=0\ny=-1\ndx=0\ndy=1\nfor _ in range(n*n):\n    if 0<=x+dx<=n-1 and 0<=y+dy<=n-1 and not vis[x+dx][y+dy]:\n        vis[x+dx][y+dy]=True\n        x=x+dx\n        y=y+dy\n        ans=ans+lis[x][y]\n        continue\n    else:\n        dx,dy=dy,-dx\n        vis[x+dx][y+dy]=True\n        x=x+dx\n        y=y+dy\n        ans=ans+lis[x][y]\n        continue\nprint(ans)\n'
SAMPLE='3\n2 5 7\n3 9 1\n8 6 4\n'
GENERATOR_NAME='g20121'
SAMPLE2='2\n7 5\n3 9\n'


def valid(text):
    """题面：第一行整数 n（30>=n>=2），此后 n 行每行 n 个整数 mi（0<mi<10）。"""
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    if not lines[0].isdigit():
        return False
    n = int(lines[0])
    if not 2 <= n <= 30 or len(lines) != n + 1:
        return False
    for line in lines[1:]:
        tok = line.split()
        if len(tok) != n or any(not (t.isdigit() and 0 < int(t) < 10) for t in tok):
            return False
    return True


def g20121(r, n=None):
    if n is None:
        n = r.randint(2, 30)
    return f"{n}\n" + "\n".join(" ".join(str(r.randint(1, 9)) for _ in range(n)) for _ in range(n)) + "\n"


def build_cases():
    # 前 39 组种子与旧版一致的随机规模换成 2..30 全范围，另外钉死上下界与奇偶边长
    cases = [SAMPLE, SAMPLE2]
    fixed = [2, 3, 4, 5, 29, 30, 30, 30]
    for i, n in enumerate(fixed):
        cases.append(g20121(random.Random(1000 + i), n))
    seed = 1
    while len(cases) < 40:
        text = g20121(random.Random(seed)); seed += 1
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

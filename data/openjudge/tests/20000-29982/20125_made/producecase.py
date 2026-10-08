import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE="# External reference: cs101.openjudge.cn practice/20125 statistics, Accepted solution 41484284.\n# Source: http://cs101.openjudge.cn/practice/solution/41484284/\n# Statistics: http://cs101.openjudge.cn/practice/20125/statistics/\n# License: not declared on submission page; no license inferred\n# 王楚惟\nl=int(input())\n'''a=[int(i)for i in input().split()]\ns=list(set(a))\nb=[a.count(i)for i in s]\nl=len(b)\nn=n//2'''\nb=[int(i)for i in input().split()]\nn=0\nfor i in b:\n    n+=i\nn=n//2\n\ncun=0\nif n==0:\n    print(1)\nelse:\n    \n    tem=0\n    def ans(i):\n        global cun\n        global tem\n        if i==l:\n            if tem==n:\n                cun=cun+1\n        else:\n            for j in range(b[i]+1):\n                if tem+j>n:\n                    break\n                else:\n                    tem=tem+j\n                    ans(i+1)\n                    tem=tem-j\n\n    if l==1:\n        print(1)\n    elif l==2:\n        print(min(b[0],b[1])+1)\n    else:\n        ans(0)\n        print(cun)\n"
SAMPLE='2\n100 100\n'
GENERATOR_NAME='g20125'
SAMPLE2='1\n100\n'


def valid(text):
    """题面没有给出 n、ai 的范围，只能核格式：第一行正整数 n，第二行恰好 n 个非负整数（等级种数）。"""
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    if len(lines) != 2 or not lines[0].isdigit():
        return False
    n = int(lines[0]); tok = lines[1].split()
    return n >= 1 and len(tok) == n and all(t.isdigit() for t in tok)


def g20125(r):
    kind = r.randrange(5)
    if kind == 0:                                   # 旧版形状：小 n 小 ai
        n, hi = r.randint(1, 8), 4
    elif kind == 1:                                 # 与样例同量级的大 ai，n=2/3（n=2 的 min+1 特判之外也要算对）
        n, hi = r.choice([2, 3, 3]), 100
    elif kind == 2:
        n, hi = r.randint(4, 5), 25
    elif kind == 3:                                 # 科目多、等级少
        n, hi = r.randint(9, 12), 3
    else:                                           # 各科等级差异悬殊
        n = r.randint(3, 5)
        return f"{n}\n" + " ".join(str(r.choice([1, 2, r.randint(30, 100)])) for _ in range(n)) + "\n"
    return f"{n}\n" + " ".join(str(r.randint(1, hi)) for _ in range(n)) + "\n"


FIXED = ['1\n1\n', '2\n1 1\n', '2\n1 100\n', '3\n1 1 1\n', '3\n100 100 100\n', '4\n1 1 1 1\n']


def build_cases():
    cases = [SAMPLE, SAMPLE2] + FIXED
    seed = 1
    while len(cases) < 40:
        text = g20125(random.Random(seed)); seed += 1
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

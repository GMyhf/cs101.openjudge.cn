import random, re, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/23997/\n# Accepted submission: 52997582\n# Source: http://cs101.openjudge.cn/practice/solution/52997582/\n# License: not declared on the submission page; no license is inferred.\n\nnn=int(input())\nl=[]\n\ndef dfs(n,ans):\n    if n==0:\n        l.append(ans[:])\n\n    for i in range(1,n+1):\n        if i%2==1 and (i not in ans) :\n            if ans:\n                if i > max(ans):\n                    nans=ans.copy()\n                    nans.append(i)\n                    dfs(n-i,nans)\n            else:\n                nans = ans.copy()\n                nans.append(i)\n                dfs(n - i, nans)\n\ndfs(nn,[])\nl=sorted(l)\nfor i in l:\n    print(" ".join(map(str,i)))\nprint(len(l))'
SAMPLE='15\n'
EXTRA_CASES=['100\n']
GENERATOR_NAME='g23997'
# 边界：最小、无解（2、4、6…偶数小值）、上限附近
EDGE_N=[1,2,3,4,5,6,7,8,99,98,97,96,95,94]

def valid(text):
    """题面：一个正整数 N，1 <= N <= 100。"""
    if not re.fullmatch(r'[1-9][0-9]*\n', text):
        return False
    return 1 <= int(text) <= 100

def build_cases():
    used={15,100}|set(EDGE_N)
    rest=[n for n in range(9,94) if n not in used]
    r=random.Random(23997)
    picks=r.sample(rest, 41-2-len(EDGE_N))
    return [SAMPLE]+EXTRA_CASES+[f"{n}\n" for n in EDGE_N]+[f"{n}\n" for n in picks]

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=build_cases()
    assert all(valid(c) for c in cases) and len(set(cases))==len(cases)
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()

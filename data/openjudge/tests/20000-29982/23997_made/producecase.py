import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/23997/\n# Accepted submission: 52997582\n# Source: http://cs101.openjudge.cn/practice/solution/52997582/\n# License: not declared on the submission page; no license is inferred.\n\nnn=int(input())\nl=[]\n\ndef dfs(n,ans):\n    if n==0:\n        l.append(ans[:])\n\n    for i in range(1,n+1):\n        if i%2==1 and (i not in ans) :\n            if ans:\n                if i > max(ans):\n                    nans=ans.copy()\n                    nans.append(i)\n                    dfs(n-i,nans)\n            else:\n                nans = ans.copy()\n                nans.append(i)\n                dfs(n - i, nans)\n\ndfs(nn,[])\nl=sorted(l)\nfor i in l:\n    print(" ".join(map(str,i)))\nprint(len(l))'
SAMPLE='15\n'
EXTRA_CASES=['100\n']
GENERATOR_NAME='g23997'
def g23997(r): return f"{r.randint(1,35)}\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+EXTRA_CASES+(['8\n','9\n'] if GENERATOR_NAME == 'g22007' else [])+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()

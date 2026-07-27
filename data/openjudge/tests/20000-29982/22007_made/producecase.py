import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE="# External reference: statistics page /practice/22007/\n# Accepted submission: 52245294\n# Source: http://cs101.openjudge.cn/practice/solution/52245294/\n# License: not declared on the submission page; no license is inferred.\n\nn=int(input())\nboard=[[0]*n for i in range(n)]\ndef issafe(lines,x,y):\n    for i in range(len(lines)):\n        if i-lines[i]==x-y or i+lines[i]==x+y:\n            return False\n    return True\n\nans=[]\ndef dfs(lines,count):\n    if count==n:\n        ans.append(lines[:])\n        return\n    if len(lines)>n:\n        return\n    for j in range(n):\n        if j not in lines and issafe(lines,len(lines),j):\n            lines.append(j)\n            dfs(lines,count+1)\n            lines.pop()\n\ndfs([],0)\nans.sort()\nif not ans:\n    print('NO ANSWER')\nelse:\n    for lines in ans:\n        print(*lines)"
SAMPLE='4\n'
GENERATOR_NAME='g22007'
def g22007(r):
    return f"{r.randint(1, 7)}\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+(['8\n','9\n'] if GENERATOR_NAME == 'g22007' else [])+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()

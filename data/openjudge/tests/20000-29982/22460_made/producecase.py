import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE="# External reference: statistics page /practice/22460/\n# Accepted submission: 45199466\n# Source: http://cs101.openjudge.cn/practice/solution/45199466/\n# License: not declared on the submission page; no license is inferred.\n\ndef valid(n,ls):\n    stack = []\n    for cha in ls:\n        if cha == '#' :\n            if not stack:\n                return False\n            stack[-1] -= 1\n        else:\n            if not stack and cha != ls[0]:\n                return False\n            if stack:\n                stack[-1] -= 1\n            stack.append(2)\n        \n        while stack and stack[-1] == 0:\n            stack.pop()\n    \n    return not stack\n\nwhile True:\n    n = int(input())\n    if n == 0:\n        break\n    ls = input().split()\n    \n    print('T' if valid(n,ls) else 'F')"
SAMPLE='13\n9 3 4 # # 1 # # 2 # 6 # #\n4\n9 # # 1\n2\n# 99\n0\n'
GENERATOR_NAME='g22460'
def g22460(r):
    def make(depth=0):
        if depth >= 4 or r.random() < .5:
            return [str(r.randint(1, 99)), "#", "#"]
        return [str(r.randint(1, 99))] + make(depth + 1) + make(depth + 1)
    tokens = make()
    if r.random() < .35:
        tokens = tokens[:-1] + [str(r.randint(1, 99))]
    return f"{len(tokens)}\n{' '.join(tokens)}\n0\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()

import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/28413/\n# Accepted submission: 52720583\n# Source: http://cs101.openjudge.cn/practice/solution/52720583/\n# License: not declared on the submission page; no license is inferred.\n\nfor _ in range(int(input())):\n    n = int(input())\n    names = []\n    edges = [[] for _ in range(n)]\n    for i in range(n):\n        s = input().split()\n        names.append(s[0])\n        for j in s[1:]:\n            j = int(j)-1\n            edges[i].append(j)\n    for i in range(n):\n        edges[i].sort()        \n    ans = []\n    part = []\n    for i in range(n):\n        cur = []\n        cur.append(names[i])\n        for ci in edges[i]:\n            cur.extend(part[ci])\n        part.append(cur)\n        ans.extend(part[-1])\n    print(len(ans))\n    print(*ans)'
SAMPLE='3\n3\nA\nB 1\nC 2 1\n4\nA\nB 1\nC 2\nD 3\n5\nTakamatsu\nKaname\nShiina 2\nChihaya 1\nNagasaki 1 4\n'
EXTRA_CASE=None
GENERATOR_NAME='g28413'
def g28413(r):
    t = r.randint(1, 6); rows = [str(t)]
    for _ in range(t):
        n = r.randint(1, 40); rows.append(str(n))
        for i in range(n):
            deps = sorted(r.sample(range(1, i + 1), r.randint(0, min(i, 3)))) if i else []
            rows.append("N" + str(i) + (" " + " ".join(map(str, deps)) if deps else ""))
    return "\n".join(rows) + "\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=120)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+([EXTRA_CASE] if EXTRA_CASE else [])+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()

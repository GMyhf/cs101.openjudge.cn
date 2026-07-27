import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE="# External reference: cs101.openjudge.cn practice/20136 statistics, Accepted solution 22633121.\n# Source: http://cs101.openjudge.cn/practice/solution/22633121/\n# Statistics: http://cs101.openjudge.cn/practice/20136/statistics/\n# License: not declared on submission page; no license inferred\ndef zoutong(z,x,y):\n    if x > y:\n        ans = zoutong(y,x)\n    ans = True\n    if z>x and y>z:\n        ans = False\n    else:\n        for i in range(x,y):\n            if (i+1) not in portal[i]:\n                ans = False\n                break\n    return ans\n\npolicerick,t = map(int,input().split())\ncheck = []\nportal = {}\nfor i in range(t):\n    tem = list(map(int,input().split()))\n    portal[i] = tem[1:]\n    if len(portal[i])>2:\n        check.append(i)\n\nif policerick == 1:\n    print('YES!')\nelse:\n    flag = False\n    for i in check:\n        if flag == False:\n            for x in range(len(portal[i])-1):\n                if flag == False:\n                    for y in range(len(portal[i])-x-1):\n                        if flag == False:\n                            if zoutong(i,portal[i][x],portal[i][x+y+1]):\n                                if portal[i][x+y+1]-portal[i][x]+1 >= policerick:\n                                    flag = True\n        else:\n            break\n\n    if flag == True:\n        print('YES!')\n    else:\n        print('NO!')\n"
SAMPLE='7 15\n0 1\n1 0 2 6\n2 1 3 7 14\n3 2 4\n4 3 5\n5 4 6\n6 1 5\n7 2 8\n8 7 9\n9 8 10\n10 9 11\n11 10 12\n12 11 13\n13 12 14\n14 2 13\n'
GENERATOR_NAME='g20136'
def g20136(r):
    kind = r.randrange(6)
    if kind == 0:
        t = r.randint(4, 12); edges = {(i, (i + 1) % t) for i in range(t)}
    elif kind == 1:
        t = r.randint(4, 12); edges = {(i, i + 1) for i in range(t - 1)}
    elif kind == 2:
        t = r.randint(5, 12); edges = {(0, i) for i in range(1, t)}
    elif kind == 3:
        t = 4; edges = {(i, j) for i in range(t) for j in range(i + 1, t)}
    elif kind == 4:
        t = 6; edges = {(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3)}
    else:
        t = r.randint(5, 12); edges = {(i, i + 1) for i in range(t - 1)}
        for _ in range(r.randint(1, t)):
            a, b = r.sample(range(t), 2); edges.add((min(a, b), max(a, b)))
    adj = [[] for _ in range(t)]
    for a, b in edges:
        adj[a].append(b); adj[b].append(a)
    police = 1 if r.random() < .5 else 2
    return f"{police} {t}\n" + "\n".join(
        f"{i} " + " ".join(map(str, sorted(adj[i]))) for i in range(t)
    ) + "\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        src=Path(d)/'main.py'; src.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(src)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1,21)]
    for i,text in enumerate(cases):
        (data/f'{i}.in').write_text(text); (data/f'{i}.out').write_text(run(text))
if __name__=='__main__': main()

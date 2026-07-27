import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/23163/\n# Accepted submission: 52702740\n# Source: http://cs101.openjudge.cn/practice/solution/52702740/\n# License: not declared on the submission page; no license is inferred.\n\nn, m = map(int, input().split())\nparent = list(range(n))\nrank = [0] * n\n\ndef find(x):\n    while parent[x] != x:\n        parent[x] = parent[parent[x]]\n        x = parent[x]\n    return x\n\ndef union(x, y):\n    rx, ry = find(x), find(y)\n    if rx == ry:\n        return False\n    if rank[rx] < rank[ry]:\n        parent[rx] = ry\n    elif rank[rx] > rank[ry]:\n        parent[ry] = rx\n    else:\n        parent[ry] = rx\n        rank[rx] += 1\n    return True\n\nhas_cycle = False\nfor _ in range(m):\n    u, v = map(int, input().split())\n    if not union(u, v):\n        has_cycle = True\n\n# 检查连通性：所有点是否属于同一集合\nroot = find(0)\nconnected = all(find(i) == root for i in range(n))\n\nprint("connected:yes" if connected else "connected:no")\nprint("loop:yes" if has_cycle else "loop:no")'
SAMPLE='3 2\n0 1\n0 2\n'
GENERATOR_NAME='g23163'
def g23163(r):
    n=r.randint(2,20); edges=[(i,i+1) for i in range(n-1) if r.random()<.65]
    edges += [tuple(r.sample(range(n),2)) for _ in range(r.randint(0,n))]
    if not edges: edges=[(0,1)]
    return f"{n} {len(edges)}\n"+"\n".join(f"{a} {b}" for a,b in edges)+"\n"

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

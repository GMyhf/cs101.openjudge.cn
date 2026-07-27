import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/20169/\n# Accepted submission: 52720771\n# Source: http://cs101.openjudge.cn/practice/solution/52720771/\n# License: not declared on the submission page; no license is inferred.\n\n# 逐行读入：每次读取一整行字符串\nimport sys\n\ninput = sys.stdin.readline\n\ndef find(parent, x):  # 查找编号x的祖先\n    if parent[x] != x:\n        parent[x] = find(parent, parent[x])\n    return parent[x]\n\ndef main():\n    T = int(input())\n\n    for _ in range(T):\n        n, m = map(int, input().split())\n\n        parent = list(range(n + 1))\n\n        for _ in range(m):\n            x, y = map(int, input().split())\n\n            rx, ry = find(parent, x), find(parent, y)\n\n            if rx != ry:\n                parent[rx] = ry\n\n        ans = [str(find(parent, i)) for i in range(1, n + 1)]\n        print(" ".join(ans))\n\nif __name__ == "__main__":\n    main()\n'
SAMPLE='2\n4 2\n1 2\n3 4\n5 4\n1 2\n2 3\n4 5\n1 3\n'
GENERATOR_NAME='g20169'
def g20169(r):
    cases = []
    for _ in range(r.randint(1, 4)):
        n = r.randint(2, 12)
        edges = [(i, i + 1) for i in range(1, n) if r.random() < .65]
        edges += [tuple(sorted(r.sample(range(1, n + 1), 2))) for _ in range(r.randint(0, n))]
        if not edges:
            edges = [(1, 2)]
        cases.append((n, edges))
    return str(len(cases)) + "\n" + "\n".join(
        f"{n} {len(edges)}\n" + "\n".join(f"{a} {b}" for a, b in edges)
        for n, edges in cases) + "\n"

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

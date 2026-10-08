import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE = 'n, m, k = map(int, input().split())\nA = [[int(x) for x in input().split()] for _ in range(n)]\nB = [[int(x) for x in input().split()] for _ in range(m)]\nC = [[0]*k for _ in range(n)]\nfor i in range(n):\n    for j in range(k):\n        C[i][j] = sum(A[i][t]*B[t][j] for t in range(m))\nfor i in range(n):\n    print(*C[i])'
SAMPLE = '3 2 3\n1 1\n1 1\n1 1\n1 1 1\n1 1 1\n'
GENERATOR_NAME = 'g7544'
def valid(text):
    """题面契约：首行 n m k（均小于 100，且为正）；随后 A 的 n 行、每行 m 个整数，B 的 m 行、每行 k 个整数；
    元素绝对值不大于 1000。"""
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    def ints(line, cnt):
        t = line.split(' ')
        if len(t) != cnt:
            return None
        try:
            v = [int(x) for x in t]
        except ValueError:
            return None
        return v if all(str(x) == y for x, y in zip(v, t)) else None
    h = ints(lines[0], 3)
    if h is None or not all(1 <= x < 100 for x in h):
        return False
    n, m, k = h
    if len(lines) != 1 + n + m:
        return False
    for idx, line in enumerate(lines[1:]):
        v = ints(line, m if idx < n else k)
        if v is None or any(abs(x) > 1000 for x in v):
            return False
    return True


def g7544(r, i=0):
    if i <= 12:
        n,m,k=[r.randint(1,6) for _ in range(3)]; lim=20
    elif i <= 20:
        n,m,k=[r.randint(1,6) for _ in range(3)]; lim=1000
    elif i <= 28:
        n,m,k=[r.randint(10,99) for _ in range(3)]; lim=r.choice([10,1000])
    elif i <= 32:
        # 退化形状：行/列向量
        n,m,k=[(1,99,1),(99,1,99),(1,1,1),(99,99,1)][i-29]; lim=1000
    else:
        n,m,k=99,99,99; lim=1000
    if i in (35, 36):
        # 全取极值，C 元素可达 ±99*10^6
        sgn = 1 if i == 35 else -1
        z=[[1000]*m for _ in range(n)]+[[1000*sgn]*k for _ in range(m)]
    else:
        z=[[r.randint(-lim,lim) for _ in range(m)] for _ in range(n)]+[[r.randint(-lim,lim) for _ in range(k)] for _ in range(m)]
    return f"{n} {m} {k}\n"+"\n".join(" ".join(map(str,x)) for x in z)+"\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"
        p.write_text(REFERENCE, encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed), seed) for seed in range(1, 40)]
    for i,text in enumerate(cases):
        assert valid(text), i
        (data/f"{i}.in").write_text(text, encoding="utf-8")
        (data/f"{i}.out").write_text(run(text), encoding="utf-8")
if __name__=="__main__": main()

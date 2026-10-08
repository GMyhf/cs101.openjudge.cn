import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='n = int(input())\n\nhp = list(map(int, input().split()))\ntime = list(map(int, input().split()))\n\nINF = 10**18\n\ndp = [INF] * (n + 1)\ndp[0] = 0\n\nfor i in range(n):\n    value = time[i] + 1\n    cost = hp[i]\n\n    ndp = dp[:]\n\n    for j in range(n + 1):\n        if dp[j] == INF:\n            continue\n\n        nj = min(n, j + value)\n        ndp[nj] = min(ndp[nj], dp[j] + cost)\n\n    dp = ndp\n\nprint(dp[n])'
SAMPLE='4\n1 2 3 2\n1 2 3 2\n'
GENERATOR_NAME='g27307'
# 题面：1 <= n <= 200，1 <= hp[i] <= 10^6，1 <= time[i] <= 500。
# time 多取小值：time 大到一只怪就能覆盖全部时，答案退化成 min(hp)，测不出 DP。
def g27307(r):
    n = r.choice([r.randint(1, 20), r.randint(1, 200), 200])
    hp_max = r.choice([10, 1000, 10**6])
    t_max = r.choice([1, 3, 10, 500])
    hp = [r.randint(1, hp_max) for _ in range(n)]; tm = [r.randint(1, t_max) for _ in range(n)]
    return f"{n}\n{' '.join(map(str, hp))}\n{' '.join(map(str, tm))}\n"

def fixed_27307():
    """两端：n=1；n=200 全部 time=1（恰好要打一半）；time=500、hp=10^6 取满。"""
    return ["1\n1000000\n500\n",
            "200\n" + " ".join(str(10**6 - i) for i in range(200)) + "\n" + " ".join(["1"] * 200) + "\n",
            "200\n" + " ".join(["1000000"] * 200) + "\n" + " ".join(["500"] * 200) + "\n",
            "200\n" + " ".join(str(i % 7 + 1) for i in range(200)) + "\n" + " ".join(str(i % 3 + 1) for i in range(200)) + "\n"]

def valid(text):
    lines = text.split("\n")
    if len(lines) != 4 or lines[3] != "":
        return False
    n = int(lines[0]); hp = list(map(int, lines[1].split())); tm = list(map(int, lines[2].split()))
    return (1 <= n <= 200 and len(hp) == len(tm) == n
            and all(1 <= x <= 10**6 for x in hp) and all(1 <= x <= 500 for x in tm))

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=60)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def scale_case():
    if GENERATOR_NAME == 'g26267': return 'A'*1000000+'\n'+'A'*1000+'\n'
    if GENERATOR_NAME == 'g26273': return ('abcdefghij'*10000)+'\n'
    if GENERATOR_NAME == 'g26835':
        e=[(i-1,i,float(i)) for i in range(1,99)]
        for i in range(99):
            for j in range(i+2,min(99,i+12)): e.append((i,j,float(10000+i*99+j)))
        return '99 %d\n'%len(e)+'\n'.join(f'{a} {b} {w:.3f}' for a,b,w in e)+'\n'
    if GENERATOR_NAME == 'g27311': return '100000\n'+' '.join(str(i%10001) for i in range(100000))+'\n'+' '.join(str((i*7)%10001) for i in range(100000))+'\n'
    return None
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    extra=scale_case(); fixed=fixed_27307(); cases=[SAMPLE]+fixed+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1, 40-len(fixed))]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()

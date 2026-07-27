import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='n = int(input())\n\nhp = list(map(int, input().split()))\ntime = list(map(int, input().split()))\n\nINF = 10**18\n\ndp = [INF] * (n + 1)\ndp[0] = 0\n\nfor i in range(n):\n    value = time[i] + 1\n    cost = hp[i]\n\n    ndp = dp[:]\n\n    for j in range(n + 1):\n        if dp[j] == INF:\n            continue\n\n        nj = min(n, j + value)\n        ndp[nj] = min(ndp[nj], dp[j] + cost)\n\n    dp = ndp\n\nprint(dp[n])'
SAMPLE='4\n1 2 3 2\n1 2 3 2\n'
GENERATOR_NAME='g27307'
def g27307(r):
    n = r.randint(1, 100); hp = [r.randint(1, 1000) for _ in range(n)]; tm = [r.randint(1, 1000) for _ in range(n)]
    return f"{n}\n{' '.join(map(str, hp))}\n{' '.join(map(str, tm))}\n"

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
    extra=scale_case(); cases=[SAMPLE]+([extra] if extra else [])+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()

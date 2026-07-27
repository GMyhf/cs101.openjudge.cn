import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE="m, c = map(int, input().split())\nchairs = [0]*(10**6+1)\nfor _ in range(m):\n    n, s, d = map(int, input().split())\n    for i in range(s,s+d):\n        chairs[i] += n\nif max(chairs) <= c:\n    print('Y')\nelse:\n    print('N')"
SAMPLE='2 3\n2 1 4\n3 5 3\n'
GENERATOR_NAME='g25684'
def g25684(r):
    m, c = r.randint(1, 20), r.randint(1, 100)
    rows = [f"{r.randint(1, 100)} {r.randint(0, 100000)} {r.randint(1, 10)}" for _ in range(m)]
    return f"{m} {c}\n" + "\n".join(rows) + "\n"

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

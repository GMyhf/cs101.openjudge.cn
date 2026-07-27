import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='n=int(input())\nbirs={}\nfor i in range(n):\n    num,m,d=map(str,input().split())\n    m,d=int(m),int(d)\n    if (m,d) not in birs.keys():\n        birs[(m,d)]=[num]\n    else:\n        birs[(m,d)].append(num)\ndays=list(birs.keys())\ndays.sort()\nfor m,d in days:\n    if len(birs[(m,d)])>1:\n        output=[m,d]\n        for num in birs[(m,d)]:\n            output.append(num)\n        print(*output)'
SAMPLE='5\n00508192 3 2\n00508153 4 5\n00508172 3 2\n00508023 4 5\n00509122 4 5\n'
GENERATOR_NAME='g25301'
def g25301(r):
    n = r.randint(2, 60); rows = []
    for i in range(n):
        month, day = r.randint(1, 12), r.randint(1, 28)
        rows.append(f"{50800000 + i:08d} {month} {day}")
    return f"{n}\n" + "\n".join(rows) + "\n"

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

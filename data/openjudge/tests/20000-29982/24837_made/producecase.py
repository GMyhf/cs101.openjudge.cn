import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='from collections import deque\np,q,x,y = map(int,input().split())\nqu = deque([p])\nans,found = 1,0\nvis = {p}\nwhile qu and ans <= 52:\n    l = len(qu)\n    for _ in range(l):\n        qi = qu.popleft()\n        if qi >= x and qi-x not in vis:\n            vis.add(qi-x)\n            qu.append(qi-x)\n            if qi-x == q:\n                found = 1\n                break\n        if qi*y not in vis and qi*y <= (52-ans)*x+q:\n            qu.append(qi*y)\n            vis.add(qi*y)\n            if qi*y == q:\n                found = 1\n                break\n    if found:\n        break\n    ans += 1\nprint(ans if found else "Failed")'
SAMPLE='2 2333 666 8\n'
GENERATOR_NAME='g24837'
def g24837(r):
    p = r.randint(100, 10**8); x = r.randint(1, 9); y = r.randint(2, 9)
    q = (p - x * r.randint(1, min(30, (p - 1) // x))
         if r.random() < .55 else r.randint(1, 10**8))
    return f"{p} {q} {x} {y}\n"

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

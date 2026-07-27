import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='n, m = map(int,input().split())\nd = [0] + list(map(int,input().split()))\na = [0] + list(map(int,input().split()))\ndef can(x):\n    last = [0] * (m + 1) #last[i]表示科目i在[1,x]中的最后出现位置 ，m科目数，x表示1~x天\n    for i in range(1, x + 1):\n        if d[i] != 0:\n            last[d[i]] = i\n    for i in range(1, m + 1): #有科目没出现\n        if last[i] == 0:\n            return False\n    free = 0  #可用的复习天数\n    done = [False] * (m + 1)\n    for i in range(1, x + 1):\n        subj = d[i]\n        if subj != 0 and last[subj] == i:  #这一天是某科目的最后可考日\n            need = a[subj]\n            if free < need:\n                return False\n            free -= need\n            done[subj] = True\n        else:\n            free += 1\n    return all(done[1:])\nlo, hi = 1, n \nans = -1\nwhile lo <= hi:\n    mid = (lo + hi) // 2\n    if can(mid):\n        ans = mid\n        hi = mid - 1\n    else:\n        lo = mid + 1\nprint(ans)'
SAMPLE='7 2\n0 1 0 2 1 0 2\n2 1\n'
GENERATOR_NAME='g27278'
def g27278(r):
    m = r.randint(1, 10); n = r.randint(m, 100); d = [r.randint(0, m) for _ in range(n)]
    for i in range(1, m + 1): d[r.randrange(n)] = i
    a = [r.randint(0, 100000) for _ in range(m)]
    if r.random() < .3:
        m, n = 1, r.randint(2, 100); d, a = [0] * (n - 1) + [1], [n - 1]
    return f"{n} {m}\n{' '.join(map(str, d))}\n{' '.join(map(str, a))}\n"

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

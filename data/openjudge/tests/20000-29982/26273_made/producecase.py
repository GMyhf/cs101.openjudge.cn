import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='def main():\n    import sys\n    s = sys.stdin.readline().strip()\n    n = len(s)\n    if n == 0:\n        print()\n        return\n\n    # 计算前缀函数（next数组）\n    pi = [0] * n\n    for i in range(1, n):\n        j = pi[i-1]\n        while j > 0 and s[i] != s[j]:\n            j = pi[j-1]\n        if s[i] == s[j]:\n            j += 1\n        pi[i] = j\n\n    res = []\n    cur = pi[-1]\n    while cur > 0:\n        res.append(n - cur)\n        cur = pi[cur - 1]\n    res.append(n)  # 自身一定是周期\n\n    res.sort()\n    print(\' \'.join(map(str, res)))\n\nif __name__ == "__main__":\n    main()'
SAMPLE='abcabca\n'
GENERATOR_NAME='g26273'
def g26273(r):
    n = r.randint(1, 10000)
    unit = "".join(r.choice("abc") for _ in range(r.randint(2, 30)))
    return (unit * ((n + len(unit) - 1) // len(unit)))[:n] + "\n"

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

import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='n = int(input())\nh = list(map(int, input().split()))\n# 环形处理，加倍\narr = h + h\n\nmax_len = 0\ncurrent = 0\n\nfor i in range(len(arr) - 1):\n    if arr[i] > arr[i + 1]:\n        current += 1\n        if current > max_len:\n            max_len = current\n    else:\n        current = 0\n\n# 最长不能超过一圈\nmax_len = min(max_len, n)\n# 全相等输出 0\nif max_len == 0:\n    print(0)\nelse:\n    print(max_len)'
SAMPLE='5\n2 1 5 6 3\n'
GENERATOR_NAME='g24830'
def g24830(r):
    n = r.randint(2, 100)
    h = [r.randint(0, 10000) for _ in range(n)]
    if r.random() < .65:
        start = r.randint(0, 9999); h = [max(0, start - i * r.randint(1, 100)) for i in range(n)]
    return f"{n}\n{' '.join(map(str, h))}\n"

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

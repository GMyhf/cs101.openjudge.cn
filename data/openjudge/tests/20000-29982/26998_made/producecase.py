import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='import sys\ninput = sys.stdin.read\ndata = input().split()\n\nidx = 0\nT = int(data[idx])\nidx += 1\n\nfor _ in range(T):\n    n = int(data[idx])\n    idx += 1\n    a = list(map(int, data[idx:idx+n]))\n    idx += n\n    \n    dp = [0] * 32  # 0~31位足够\n    \n    for num in a:\n        if num == 0:\n            continue  # 0 & 任何数 =0，不能选\n        \n        # 收集所有为1的二进制位\n        bits = []\n        for b in range(32):\n            if num & (1 << b):\n                bits.append(b)\n        \n        # 当前能达到的最大长度\n        max_len = 0\n        for b in bits:\n            if dp[b] > max_len:\n                max_len = dp[b]\n        cur = max_len + 1\n        \n        # 更新所有位\n        for b in bits:\n            if cur > dp[b]:\n                dp[b] = cur\n    \n    print(max(dp))'
SAMPLE='2\n3\n1 2 3\n5\n1 10 100 1000 10000\n'
GENERATOR_NAME='g26998'
def g26998(r):
    t = r.randint(1, 8); rows = [str(t)]
    for _ in range(t):
        n = r.randint(1, 100); rows += [str(n), " ".join(str(r.randint(1, 10**9)) for _ in range(n))]
    return "\n".join(rows) + "\n"

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

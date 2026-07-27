import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE="# 读取输入\ncoins = list(map(int, input().split()))\namount = int(input())\n\n# 边界：金额为0直接返回0\nif amount == 0:\n    print(0)\n    exit()\n\nINF = float('inf')\n# dp[i] = 凑出金额i需要的最小硬币数\ndp = [INF] * (amount + 1)\ndp[0] = 0\n\n# 完全背包\nfor coin in coins:\n    for i in range(coin, amount + 1):\n        if dp[i - coin] != INF:\n            dp[i] = min(dp[i], dp[i - coin] + 1)\n\n# 输出答案\nprint(dp[amount] if dp[amount] != INF else -1)"
SAMPLE='1 2 5\n11\n'
GENERATOR_NAME='g27277'
def g27277(r):
    coins = sorted(set(r.randint(1, 100) for _ in range(r.randint(2, 5))))
    return " ".join(map(str, coins)) + f"\n{r.randint(0, 10000)}\n"

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

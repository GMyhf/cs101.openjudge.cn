import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/27441/\n# Accepted submission: 52735735\n# Source: http://cs101.openjudge.cn/practice/solution/52735735/\n# License: not declared on the submission page; no license is inferred.\n\ndef main():\n    import sys\n    input = sys.stdin.read().split()\n    ptr = 0\n    N = int(input[ptr])\n    M = int(input[ptr+1])\n    ptr +=2\n    p = list(map(int,input[ptr:ptr+M]))\n    ptr += M\n    num = list(map(int,input[ptr:ptr+M]))\n\n    INF = 10**18\n    dp = [INF]*(N+1)\n    dp[0] = 0\n\n    for i in range(M):\n        pi = p[i]\n        ci = num[i]\n        # 二进制优化多重背包\n        k = 1\n        rest = ci\n        while rest>0:\n            take = min(k, rest)\n            cost = take*pi\n            cnt = take\n            # 倒序\n            for v in range(N, cost-1, -1):\n                if dp[v-cost] + cnt < dp[v]:\n                    dp[v] = dp[v-cost]+cnt\n            rest -= take\n            k *=2\n    if dp[N]==INF:\n        print("Fail")\n    else:\n        print(dp[N])\n\nif __name__=="__main__":\n    main()'
SAMPLE='40 3\n4 5 11\n5 4 1\n'
EXTRA_CASE='10000 20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20\n1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000\n'
GENERATOR_NAME='g27441'
def g27441(r):
    n, m = r.randint(1, 300), r.randint(1, 20)
    p = [r.randint(1, 40) for _ in range(m)]
    c = [r.randint(0, 30) for _ in range(m)]
    return f"{n} {m}\n{' '.join(map(str, p))}\n{' '.join(map(str, c))}\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=90)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def scale_case(): return EXTRA_CASE
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    extra=scale_case(); cases=[SAMPLE]+([extra] if extra else [])+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()

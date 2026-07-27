import random
REFERENCE='# External reference: /practice/30192/statistics/\n# Accepted submission: 52723659\n# Source: http://cs101.openjudge.cn/practice/solution/52723659/\n# License: not declared on the submission page; no license is inferred.\n\ndef main():\n    import sys\n    input = sys.stdin.read().split()\n    ptr = 0\n    W = int(input[ptr])\n    ptr += 1\n    n = int(input[ptr])\n    ptr += 1\n    t = []\n    w = []\n    for _ in range(n):\n        ti = int(input[ptr])\n        wi = int(input[ptr+1])\n        t.append(ti)\n        w.append(wi)\n        ptr += 2\n    \n    size = 1 << n\n    sumw = [0]*size\n    maxt = [0]*size\n    # 预处理所有子集的总重量、最大时间\n    for s in range(size):\n        sw = 0\n        mt = 0\n        for i in range(n):\n            if s & (1 << i):\n                sw += w[i]\n                if t[i] > mt:\n                    mt = t[i]\n        sumw[s] = sw\n        maxt[s] = mt\n    \n    INF = 10**18\n    dp = [INF]*size\n    dp[0] = 0\n    \n    for mask in range(size):\n        if dp[mask] == INF:\n            continue\n        rem = ((1<<n)-1) ^ mask  # 剩余没过去的人\n        # 枚举rem的所有非空子集sub\n        sub = rem\n        while sub:\n            if sumw[sub] <= W:\n                newmask = mask | sub\n                if dp[newmask] > dp[mask] + maxt[sub]:\n                    dp[newmask] = dp[mask] + maxt[sub]\n            sub = (sub-1) & rem\n    print(dp[(1<<n)-1])\n\nif __name__ == "__main__":\n    main()'
SAMPLE='100 3\n24 60\n10 40\n18 50\n'
GENERATOR_NAME='g30192'
CPP=False
def g30192(r):
    n = r.randint(1, 7); return f"{r.randint(20, 200)} {n}\n" + "\n".join(f"{r.randint(1,50)} {r.randint(1,30)}" for _ in range(n)) + "\n"

from pathlib import Path
import subprocess, sys, tempfile
def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-run-') as d:
        p=Path(d)/('main.cpp' if CPP else 'main.py'); p.write_text(REFERENCE)
        if CPP:
            exe=Path(d)/'main'; c=subprocess.run(['g++','-O2','-std=c++17',str(p),'-o',str(exe)],capture_output=True,text=True,timeout=30)
            if c.returncode: raise SystemExit(c.stderr)
            cmd=[str(exe)]
        else: cmd=[sys.executable,str(p)]
        x=subprocess.run(cmd,input=text,text=True,capture_output=True,timeout=120)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (data/f'{i}.in').write_text(c); (data/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()

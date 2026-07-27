import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/28200/\n# Accepted submission: 52734593\n# Source: http://cs101.openjudge.cn/practice/solution/52734593/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\n\ninput = sys.stdin.read\ndata = input().split()\n\nN = int(data[0])\nD = int(data[1])\nMOD = 998244353\n\nif D == 0:\n    print(0)\n    sys.exit(0)\n\n# Precompute powers of 2\nMAXN = max(N, D) + 5\npw = [1] * (MAXN + 1)\nfor i in range(1, MAXN + 1):\n    pw[i] = (pw[i-1] * 2) % MOD\n\n# ans[i+1] = sum for left path length 0 to i\nans = [0] * (D + 2)\nfor i in range(D + 1):\n    j = D - i\n    l = pw[max(0, i - 1)]\n    r = pw[max(0, j - 1)]\n    ans[i + 1] = (ans[i] + 2 * l * r % MOD) % MOD\n\nres = 0\nfor dep in range(1, N + 1):  # depth from 1 to N (root depth 0, but we skip root? wait)\n    # In code: for(int i=1;i<=n;i++)  i is depth?\n    l = max(0, dep + D - N)\n    r = min(D, N - dep)\n    if l > r:\n        continue\n    # res = number for one node at this depth\n    temp = (ans[min(D, N - dep) + 1] - ans[max(0, dep + D - N)] + MOD) % MOD\n    # multiply by number of nodes at this depth: 2^{dep-1}\n    res = (res + pw[dep - 1] * temp % MOD) % MOD\n\nprint(res)'
SAMPLE='3 2\n'
EXTRA_CASE='200000 400000\n'
GENERATOR_NAME='g28200'
def g28200(r): return f"{r.randint(2, 10000)} {r.randint(1, 20000)}\n"

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

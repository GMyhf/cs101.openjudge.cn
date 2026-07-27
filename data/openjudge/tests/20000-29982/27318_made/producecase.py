import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/27318/\n# Accepted submission: 52736004\n# Source: http://cs101.openjudge.cn/practice/solution/52736004/\n# License: not declared on the submission page; no license is inferred.\n\nMOD = 10**9 + 7\n\nn, k = map(int, input().split())\n\n# dp[i][j] 表示 1~i 恰好 j 个逆序对的方案数\ndp = [[0] * (k + 1) for _ in range(n + 1)]\ndp[0][0] = 1\n\nfor i in range(1, n + 1):\n    # 前缀和优化\n    pre_sum = [0] * (k + 1)\n    pre_sum[0] = dp[i-1][0]\n    for j in range(1, k + 1):\n        pre_sum[j] = (pre_sum[j-1] + dp[i-1][j]) % MOD\n\n    for j in range(0, k + 1):\n        # dp[i][j] = sum(dp[i-1][j-t])  t=0~min(i-1,j)\n        left = j - (i - 1)\n        if left <= 0:\n            dp[i][j] = pre_sum[j] % MOD\n        else:\n            dp[i][j] = (pre_sum[j] - pre_sum[left-1]) % MOD\n\n# 保证答案非负\nans = dp[n][k] % MOD\nprint(ans)'
SAMPLE='3 0\n'
EXTRA_CASE='1000 1000\n'
GENERATOR_NAME='g27318'
def g27318(r):
    return f"{r.randint(1, 1000)} {r.randint(0, 1000)}\n"

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

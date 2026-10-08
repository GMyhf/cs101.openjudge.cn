import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/27318/\n# Accepted submission: 52736004\n# Source: http://cs101.openjudge.cn/practice/solution/52736004/\n# License: not declared on the submission page; no license is inferred.\n\nMOD = 10**9 + 7\n\nn, k = map(int, input().split())\n\n# dp[i][j] 表示 1~i 恰好 j 个逆序对的方案数\ndp = [[0] * (k + 1) for _ in range(n + 1)]\ndp[0][0] = 1\n\nfor i in range(1, n + 1):\n    # 前缀和优化\n    pre_sum = [0] * (k + 1)\n    pre_sum[0] = dp[i-1][0]\n    for j in range(1, k + 1):\n        pre_sum[j] = (pre_sum[j-1] + dp[i-1][j]) % MOD\n\n    for j in range(0, k + 1):\n        # dp[i][j] = sum(dp[i-1][j-t])  t=0~min(i-1,j)\n        left = j - (i - 1)\n        if left <= 0:\n            dp[i][j] = pre_sum[j] % MOD\n        else:\n            dp[i][j] = (pre_sum[j] - pre_sum[left-1]) % MOD\n\n# 保证答案非负\nans = dp[n][k] % MOD\nprint(ans)'
SAMPLE='3 0\n'
EXTRA_CASE='1000 1000\n'
import re

def valid(text):
    """题面：一行两个整数 n k，1<=n<=1000，0<=k<=1000。"""
    m = re.fullmatch(r'(\d+) (\d+)\n', text)
    if not m:
        return False
    n, k = int(m.group(1)), int(m.group(2))
    return 1 <= n <= 1000 and 0 <= k <= 1000

def build_cases():
    # 第 0 组样例 1，第 1 组满规模
    fixed = [SAMPLE, EXTRA_CASE,
             '3 1\n',      # 样例 2
             '1 0\n', '1 1\n', '1 1000\n',          # n=1 边界
             '2 1\n', '2 2\n', '1000 0\n', '1000 1\n',
             '3 3\n', '3 4\n',                      # k 恰为最大逆序数 / 超过
             '45 990\n', '45 1000\n', '46 1000\n',  # 45*44/2=990
             '10 45\n', '10 46\n', '10 44\n',
             '999 1000\n', '1000 999\n', '500 1000\n', '1000 500\n',
             '7 21\n', '8 14\n', '12 33\n']
    r = random.Random(27318)
    seen = set(fixed); out = list(fixed)
    while len(out) < 41:
        if len(out) % 2:
            c = f"{r.randint(1, 60)} {r.randint(0, 1000)}\n"
        else:
            c = f"{r.randint(100, 1000)} {r.randint(300, 1000)}\n"
        if c not in seen:
            seen.add(c); out.append(c)
    return out

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=90)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout

def main():
    cases = build_cases()
    assert len(cases) == 41, len(cases)
    assert len(set(cases)) == len(cases), '组间有重复'
    for i, c in enumerate(cases):
        assert valid(c), f'第 {i} 组不合题面约束'
    d=Path('data'); d.mkdir(exist_ok=True)
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()

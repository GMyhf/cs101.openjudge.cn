import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE="# External reference: statistics page /practice/23807/\n# Accepted submission: 52686966\n# Source: http://cs101.openjudge.cn/practice/solution/52686966/\n# License: not declared on the submission page; no license is inferred.\n\nk, n = map(int, input().split())\n\n# 动态规划，dp[i][j] 表示 i 根柱子、j 个盘子的最少步数\n# 最大柱子数 100，最大盘子数 100\nMAX_K = 100\nMAX_N = 100\ndp = [[0] * (MAX_N + 1) for _ in range(MAX_K + 1)]\n\n# 初始化：任意不少于3根柱子，1个盘子需要1步\nfor i in range(3, MAX_K + 1):\n    dp[i][0] = 0\n    dp[i][1] = 1\n\n# 3根柱子的经典汉诺塔\nfor j in range(2, MAX_N + 1):\n    dp[3][j] = (1 << j) - 1   # 2^j - 1\n\n# 对于4根及以上柱子，使用 Frame-Stewart 递推\nfor i in range(4, MAX_K + 1):\n    for j in range(2, MAX_N + 1):\n        best = float('inf')\n        # 尝试将上面 x 个盘子先移到辅助柱\n        for x in range(1, j):\n            val = 2 * dp[i][x] + dp[i - 1][j - x]\n            if val < best:\n                best = val\n        dp[i][j] = best\n\nprint(dp[k][n])"
SAMPLE='3 3\n'
GENERATOR_NAME='g23807'
def g23807(r): return f"{r.randint(3,10)} {r.randint(1,12)}\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+(['8\n','9\n'] if GENERATOR_NAME == 'g22007' else [])+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()

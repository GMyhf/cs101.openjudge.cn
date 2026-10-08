import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE="# External reference: statistics page /practice/23807/\n# Accepted submission: 52686966\n# Source: http://cs101.openjudge.cn/practice/solution/52686966/\n# License: not declared on the submission page; no license is inferred.\n\nk, n = map(int, input().split())\n\n# 动态规划，dp[i][j] 表示 i 根柱子、j 个盘子的最少步数\n# 最大柱子数 100，最大盘子数 100\nMAX_K = 100\nMAX_N = 100\ndp = [[0] * (MAX_N + 1) for _ in range(MAX_K + 1)]\n\n# 初始化：任意不少于3根柱子，1个盘子需要1步\nfor i in range(3, MAX_K + 1):\n    dp[i][0] = 0\n    dp[i][1] = 1\n\n# 3根柱子的经典汉诺塔\nfor j in range(2, MAX_N + 1):\n    dp[3][j] = (1 << j) - 1   # 2^j - 1\n\n# 对于4根及以上柱子，使用 Frame-Stewart 递推\nfor i in range(4, MAX_K + 1):\n    for j in range(2, MAX_N + 1):\n        best = float('inf')\n        # 尝试将上面 x 个盘子先移到辅助柱\n        for x in range(1, j):\n            val = 2 * dp[i][x] + dp[i - 1][j - x]\n            if val < best:\n                best = val\n        dp[i][j] = best\n\nprint(dp[k][n])"
SAMPLE='3 3\n'
GENERATOR_NAME='g23807'
def _fs_table(M=100):
    # Frame-Stewart 递推，仅供 valid() 核 s<=2^31-1 与生成器筛选
    dp=[[0]*(M+1) for _ in range(M+1)]
    for i in range(3,M+1): dp[i][1]=1
    for j in range(2,M+1): dp[3][j]=(1<<j)-1
    for i in range(4,M+1):
        for j in range(2,M+1): dp[i][j]=min(2*dp[i][x]+dp[i-1][j-x] for x in range(1,j))
    return dp
_FS=None
def valid(text):
    # 题面：一行两个正整数 k n，空格隔开；3<=k<=100，1<=n<=100，答案 s<=2^31-1
    global _FS
    if not text.endswith('\n') or text.count('\n')!=1: return False
    parts=text[:-1].split(' ')
    if len(parts)!=2 or not all(p.isdigit() and p==str(int(p)) for p in parts): return False
    k,n=map(int,parts)
    if not (3<=k<=100 and 1<=n<=100): return False
    if _FS is None: _FS=_fs_table()
    return 1<=_FS[k][n]<=2**31-1
def g23807(r):
    # 全值域随机：k=3 时 n<=31（s 不超过 2^31-1），其余 n 取满 1..100
    k=r.choice([3,4,4,5,5,6,r.randint(7,20),r.randint(3,100),r.randint(3,100)])
    n=r.randint(1,31) if k==3 else r.choice([r.randint(1,100),r.randint(50,100),r.randint(1,k+2)])
    return f"{k} {n}\n"
FIXED=['4 5\n','6 2\n','3 1\n','100 1\n','3 31\n','3 30\n','4 100\n','5 100\n','100 100\n','100 99\n','4 99\n','6 5\n','6 6\n','3 20\n']

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+FIXED
    seed=1
    while len(cases)<40:
        c=g23807(random.Random(seed)); seed+=1
        if c not in cases and valid(c): cases.append(c)
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()

import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/27441/\n# Accepted submission: 52735735\n# Source: http://cs101.openjudge.cn/practice/solution/52735735/\n# License: not declared on the submission page; no license is inferred.\n\ndef main():\n    import sys\n    input = sys.stdin.read().split()\n    ptr = 0\n    N = int(input[ptr])\n    M = int(input[ptr+1])\n    ptr +=2\n    p = list(map(int,input[ptr:ptr+M]))\n    ptr += M\n    num = list(map(int,input[ptr:ptr+M]))\n\n    INF = 10**18\n    dp = [INF]*(N+1)\n    dp[0] = 0\n\n    for i in range(M):\n        pi = p[i]\n        ci = num[i]\n        # 二进制优化多重背包\n        k = 1\n        rest = ci\n        while rest>0:\n            take = min(k, rest)\n            cost = take*pi\n            cnt = take\n            # 倒序\n            for v in range(N, cost-1, -1):\n                if dp[v-cost] + cnt < dp[v]:\n                    dp[v] = dp[v-cost]+cnt\n            rest -= take\n            k *=2\n    if dp[N]==INF:\n        print("Fail")\n    else:\n        print(dp[N])\n\nif __name__=="__main__":\n    main()'
SAMPLE='40 3\n4 5 11\n5 4 1\n'
EXTRA_CASE='10000 20\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20\n1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000 1000\n'

def valid(text):
    """题面：第一行 N M（20<=N<=1000000）；第二行 M 个票价；第三行 M 个余票数。
    题面未给 M、票价、余量的上界，这里按“1<=M<=100，1<=p_i<=10^6，0<=n_i<=10^6”检查。"""
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    if len(lines) != 3:
        return False
    try:
        h = lines[0].split(' ')
        if len(h) != 2:
            return False
        N, M = map(int, h)
        if not (20 <= N <= 1000000 and 1 <= M <= 100):
            return False
        p = lines[1].split(' '); c = lines[2].split(' ')
        if len(p) != M or len(c) != M:
            return False
        if not all(1 <= int(v) <= 1000000 for v in p):
            return False
        if not all(0 <= int(v) <= 1000000 for v in c):
            return False
    except ValueError:
        return False
    return True

def fmt(N, p, c):
    return f"{N} {len(p)}\n{' '.join(map(str, p))}\n{' '.join(map(str, c))}\n"

def build_cases():
    r = random.Random(27441)
    out = [SAMPLE, EXTRA_CASE,
           fmt(20, [20], [1]), fmt(20, [3], [10]),          # N 下界：恰好 / 有余额
           fmt(100, [10], [5]),                              # 余票不足
           fmt(20, [7, 3], [1, 2]),                          # 组合不出
           fmt(30, [1, 15, 25], [30, 2, 1]),                 # 贪心取最大面额会错
           fmt(40, [4, 5, 11], [5, 4, 0]),                   # 余量为 0
           fmt(60, [6, 10, 15], [10, 6, 4]),
           fmt(21, [2, 4, 8], [100, 100, 100]),              # 奇偶 Fail
           fmt(1000000, [1], [1000000]),                     # N 上界，答案=余量
           fmt(1000000, [1], [999999]),                      # N 上界，差 1 张
           fmt(1000000, [999983, 17], [1, 1000]),             # 999983+17=1e6
           fmt(1000000, [500000, 3, 7], [1, 100000, 100000]),
           fmt(999999, [2, 4, 1000], [1000, 1000, 1000]),    # 大 N 的 Fail
           fmt(1000000, [7, 11], [150000, 1000]),
           ]
    while len(out) < 41:
        t = len(out) % 3
        if t == 0:
            N, M = r.randint(20, 300), r.randint(1, 20)
            p = [r.randint(1, 40) for _ in range(M)]; c = [r.randint(0, 30) for _ in range(M)]
        elif t == 1:
            N, M = r.randint(1000, 20000), r.randint(1, 20)
            p = [r.randint(1, 500) for _ in range(M)]; c = [r.randint(1, 60) for _ in range(M)]
        else:
            M = r.randint(1, 8)
            p = [r.randint(1, 60) for _ in range(M)]; c = [r.randint(1, 40) for _ in range(M)]
            # 让一部分数据能恰好凑成
            N = max(20, sum(x * r.randint(0, y) for x, y in zip(p, c)))
        c_ = fmt(N, p, c)
        if c_ not in out:
            out.append(c_)
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

import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/21508/\n# Accepted submission: 52213688\n# Source: http://cs101.openjudge.cn/practice/solution/52213688/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\nfrom collections import deque\n\ndef main():\n    data = sys.stdin.read().strip().split()\n    if not data:\n        return\n    \n    n, m = map(int, data[:2])\n    a = list(map(int, data[2:2+n]))\n    \n    # 计算前缀和\n    S = [0] * (n + 1)\n    for i in range(1, n + 1):\n        S[i] = S[i-1] + a[i-1]\n    \n    # 单调队列维护候选左端点\n    q = deque()\n    q.append(0)  # 初始左端点 S[0] = 0\n    ans = -float(\'inf\')\n    \n    for r in range(1, n + 1):\n        # 移除超出窗口的左端点\n        while q and q[0] < r - m:\n            q.popleft()\n        \n        # 更新答案\n        if q:\n            ans = max(ans, S[r] - S[q[0]])\n        \n        # 维护队列单调递增\n        while q and S[q[-1]] >= S[r]:\n            q.pop()\n        q.append(r)\n    \n    print(ans)\n\nif __name__ == "__main__":\n    main()'
SAMPLE='6 4\n1 -3 5 1 -2 3\n'
GENERATOR_NAME='g21508'
N_MAX = 200000


def valid(text):
    """题面：第一行 n m（1<=n,m<=2e5）；第二行 n 个整数，绝对值都小于 1000。"""
    try:
        lines = text.split('\n')
        while lines and lines[-1].strip() == '':
            lines.pop()
        if len(lines) != 2:
            return False
        head = lines[0].split()
        if len(head) != 2:
            return False
        n, m = map(int, head)
        if not (1 <= n <= N_MAX and 1 <= m <= N_MAX):
            return False
        a = lines[1].split()
        return len(a) == n and all(-1000 < int(v) < 1000 for v in a)
    except ValueError:
        return False


def fmt(m, a):
    return f"{len(a)} {m}\n" + " ".join(map(str, a)) + "\n"


def g21508(r):
    n = r.randint(1, 40)
    m = r.randint(1, n + 3)
    lo, hi = r.choice([(-999, 999), (-999, 999), (-300, 999), (-999, -1)])
    return fmt(m, [r.randint(lo, hi) for _ in range(n)])


def specials():
    r = random.Random(21508)
    out = []
    out.append(fmt(1, [-5]))                                          # n=m=1，负数
    out.append(fmt(200000, [0]))                                      # m>n
    out.append(fmt(N_MAX, [r.randint(-999, 999) for _ in range(N_MAX)]))           # n=m=2e5
    out.append(fmt(1000, [r.randint(-200, 999) for _ in range(N_MAX)]))            # 正数偏多：不限长度的 Kadane 会偏大
    out.append(fmt(1, [r.randint(-999, 999) for _ in range(N_MAX)]))               # m=1：答案即最大元素
    out.append(fmt(77777, [r.randint(-999, -1) for _ in range(N_MAX)]))           # 全负
    out.append(fmt(50000, [r.randint(-999, 980) for _ in range(N_MAX)]))
    out.append(fmt(N_MAX - 1, [999] * N_MAX))                        # 恰差 1 个够不到全长
    out.append(fmt(10000, [r.randint(-999, 999) for _ in range(10000)]))
    return out

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+[g21508(random.Random(s)) for s in range(1, 40)]+specials()
    assert all(valid(c) for c in cases) and len(set(cases)) == len(cases)
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()

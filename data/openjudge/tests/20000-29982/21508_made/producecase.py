import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/21508/\n# Accepted submission: 52213688\n# Source: http://cs101.openjudge.cn/practice/solution/52213688/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\nfrom collections import deque\n\ndef main():\n    data = sys.stdin.read().strip().split()\n    if not data:\n        return\n    \n    n, m = map(int, data[:2])\n    a = list(map(int, data[2:2+n]))\n    \n    # 计算前缀和\n    S = [0] * (n + 1)\n    for i in range(1, n + 1):\n        S[i] = S[i-1] + a[i-1]\n    \n    # 单调队列维护候选左端点\n    q = deque()\n    q.append(0)  # 初始左端点 S[0] = 0\n    ans = -float(\'inf\')\n    \n    for r in range(1, n + 1):\n        # 移除超出窗口的左端点\n        while q and q[0] < r - m:\n            q.popleft()\n        \n        # 更新答案\n        if q:\n            ans = max(ans, S[r] - S[q[0]])\n        \n        # 维护队列单调递增\n        while q and S[q[-1]] >= S[r]:\n            q.pop()\n        q.append(r)\n    \n    print(ans)\n\nif __name__ == "__main__":\n    main()'
SAMPLE='6 4\n1 -3 5 1 -2 3\n'
GENERATOR_NAME='g21508'
def g21508(r):
    n, m = r.randint(1, 40), r.randint(1, 12)
    return f"{n} {m}\n" + " ".join(str(r.randint(-999, 999)) for _ in range(n)) + "\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()

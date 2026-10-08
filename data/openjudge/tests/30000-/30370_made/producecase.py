import random
REFERENCE='# External reference: /practice/30370/statistics/\n# Accepted submission: 52723545\n# Source: http://cs101.openjudge.cn/practice/solution/52723545/\n# License: not declared on the submission page; no license is inferred.\n\nimport bisect\n\ndef main():\n    import sys\n    input = sys.stdin.read\n    data = input().split()\n    n = int(data[0])\n    a = list(map(int, data[1:n+1]))\n    \n    ans = 0\n    # 遍历所有可能的选中人数k\n    for k in range(0, n + 1):\n        # 二分查找：第一个 >=k 的位置 = 小于k的元素个数\n        cnt = bisect.bisect_left(a, k)\n        # 条件1：小于k的元素数量恰好等于k\n        # 条件2：数组中没有元素等于k\n        if cnt == k and (cnt == n or a[cnt] != k):\n            ans += 1\n    print(ans)\n\nif __name__ == "__main__":\n    main()'
SAMPLE='8\n0 2 3 3 6 6 7 7\n'
GENERATOR_NAME='g30370'
CPP=False
def g30370(r):
    n = r.randint(1, 100); return f"{n}\n{' '.join(map(str, sorted(r.randint(0,n) for _ in range(n))))}\n"


def valid(text):
    """题面契约：第一行 n（1<=n<=10^6）；第二行 n 个升序非负整数，每个不超过 n。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if len(lines) != 2:
        return False
    head = lines[0].split(" ")
    if len(head) != 1 or not head[0].isdigit():
        return False
    n = int(head[0])
    if not 1 <= n <= 10**6 or str(n) != head[0]:
        return False
    toks = lines[1].split(" ")
    if len(toks) != n or any(not t.isdigit() or str(int(t)) != t for t in toks):
        return False
    a = list(map(int, toks))
    return all(0 <= x <= n for x in a) and all(a[i] <= a[i + 1] for i in range(n - 1))


def _fmt(a):
    return f"{len(a)}\n{' '.join(map(str, a))}\n"


def special_cases():
    """规模与边界组：替换原第 30..39 组（原组均 n<=100，O(n^2) 也能过）。"""
    r = random.Random(30370)
    out = []
    out.append(_fmt([0]))                       # n=1，只能全选
    out.append(_fmt([1]))                       # n=1，只能不选
    n = 130000                                  # 值域 [0,n] 的满幅随机，受 .in<=1MB 限制
    out.append(_fmt(sorted(r.randint(0, n) for _ in range(n))))
    n = 450000                                  # 小值大 n：只有 k=0 / k=n 附近可能成立
    out.append(_fmt(sorted(r.randint(0, 9) for _ in range(n))))
    n = 450000                                  # 全 0：唯一方案是全选
    out.append(_fmt([0] * n))
    n = 130000                                  # 1 1 3 3 5 5 ...：k=0,2,4,... 都成立，答案约 n/2
    a = [2 * (i // 2) + 1 for i in range(n)]
    out.append(_fmt([min(x, n) for x in a]))
    n = 130000                                  # 含等于 n 的值：k=n 不成立
    a = sorted([r.randint(0, n) for _ in range(n - 3)] + [n, n, n])
    out.append(_fmt(a))
    n = 120000                                  # 中间若干个 k 成立：在 k 处留出“空位”
    a = []
    ks = sorted(r.sample(range(1, n), 40))
    prev = 0
    for k in ks:
        # 让小于 k 的元素恰好 k 个，且没有元素等于 k
        while len(a) < k:
            a.append(r.randint(prev, k - 1))
        prev = k + 1
    while len(a) < n:
        a.append(r.randint(min(prev, n), n))
    out.append(_fmt(sorted(a)))
    n = 140000                                  # 严格递增 0..n 去掉一个：考查 cnt==n 越界分支
    a = list(range(n + 1)); a.pop(r.randint(0, n))
    out.append(_fmt(a))
    n = 100000                                  # 全等于 n：只有 k=0
    out.append(_fmt([n] * n))
    return out

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
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1, 30)]+special_cases()
    assert len(cases)==40 and all(valid(c) for c in cases) and len(set(cases))==40
    for i,c in enumerate(cases): (data/f'{i}.in').write_text(c); (data/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()

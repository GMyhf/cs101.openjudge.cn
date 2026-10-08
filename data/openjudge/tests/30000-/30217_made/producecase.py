import random
REFERENCE='# External reference: /practice/30217/statistics/\n# Accepted submission: 52829473\n# Source: http://cs101.openjudge.cn/practice/solution/52829473/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\nimport bisect\n\ndef solve():\n    # 快速读取输入\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n    \n    N = int(input_data[0])\n    T = int(input_data[1])\n    \n    # 齿轮的最大齿数限制为 1,000,000\n    MAX_VAL = 1000000\n    pos = [None] * (MAX_VAL + 1)\n    \n    # 读取齿轮数据\n    A = [int(x) for x in input_data[2:2+N]]\n    \n    # 记录每个数值出现的所有 1-based 索引位置\n    for idx in range(1, N + 1):\n        val = A[idx - 1]\n        if pos[val] is None:\n            pos[val] = []\n        pos[val].append(idx)\n        \n    # 遍历每个 i，寻找符合条件的最小 j\n    for i in range(1, N + 1):\n        val = A[i - 1]\n        target = T - val\n        \n        # 目标值必须在合法范围内\n        if 1 <= target <= MAX_VAL:\n            lst = pos[target]\n            if lst is not None:\n                # 使用二分查找在递增的索引列表中寻找第一个大于 i 的位置\n                idx_in_lst = bisect.bisect_right(lst, i)\n                if idx_in_lst < len(lst):\n                    j = lst[idx_in_lst]\n                    print(f"{i} {j}")\n                    return\n\nif __name__ == \'__main__\':\n    solve()'
SAMPLE='4 10\n1 3 7 9\n'
GENERATOR_NAME='g30217'
CPP=False
def valid(text):
    # 题面：第一行 N T（1<=N<=1e5，1<T<=2e6）；第二行 N 个整数 1<=A_i<=1e6；输出要求一对 i<j 使 A_i+A_j=T，故须有解
    if not text.endswith('\n'): return False
    lines = text[:-1].split('\n')
    if len(lines) != 2: return False
    try:
        h = [int(x) for x in lines[0].split(' ')]
        a = [int(x) for x in lines[1].split(' ')]
    except ValueError: return False
    if len(h) != 2: return False
    n, T = h
    if not (1 <= n <= 100000 and 1 < T <= 2000000) or len(a) != n: return False
    if any(not (1 <= x <= 1000000) for x in a): return False
    seen = set()
    for x in a:
        if T - x in seen: return True
        seen.add(x)
    return False

def fmt(T, a): return f"{len(a)} {T}\n{' '.join(map(str,a))}\n"

def g30217(r):
    n = r.randint(2, 80); a = [r.randint(1, 1000) for _ in range(n)]; i = r.randrange(n-1); a[i+1] = 1001-a[i]
    return f"{n} {1001}\n{' '.join(map(str,a))}\n"

def extra_cases():
    r = random.Random(30217)
    N = 100000
    out = []
    out.append(fmt(2, [1, 1]))                                   # 最小 T、N=2
    out.append(fmt(2000000, [1000000, 1000000]))                 # 最大 T
    out.append(fmt(10, [5, 3, 7, 5]))                            # A_i = T/2：不能自己配自己，答案 1 4
    out.append(fmt(10, [5, 1, 9, 5]))                            # i 最小优先于 j 最小：答案 1 4 而不是 2 3
    out.append(fmt(8, [4, 6, 2, 2, 4]))                          # 答案 1 5（4+4），不是 2 3
    out.append(fmt(1500000, [1000000, 600000, 900000, 500000]))  # T-A_i 越界/为负的写法
    # 唯一解在最末两位：O(N^2) 双重循环必超时
    a = [r.randint(1, 400000) for _ in range(N - 2)] + [999999, 1000000]
    out.append(fmt(1999999, a))
    # 唯一解 i=1、j=N
    a = [999999] + [r.randint(1, 400000) for _ in range(N - 2)] + [1000000]
    out.append(fmt(1999999, a))
    # 多组解，检验 i 最小再 j 最小
    a = [r.randint(1, 1000000) for _ in range(N)]
    out.append(fmt(1000001, a))
    a = [r.randint(1, 1000000) for _ in range(N)]
    out.append(fmt(r.randint(2, 2000000), a))
    # 全部相等
    out.append(fmt(2000000, [1000000] * N))
    out.append(fmt(2, [1] * N))
    # 大量重复值、解的 j 要选最小的那个
    a = [r.choice([3, 7, 11, 13]) for _ in range(N)]
    out.append(fmt(14, a))
    # 唯一解在中间且相距很远
    a = [r.randint(1, 300000) for _ in range(N)]; a[N // 3] = 777777; a[N - 5] = 222224
    out.append(fmt(1000001, a))
    # 每个值只出现一次的大排列（解分散）
    a = r.sample(range(1, 1000001), N)
    out.append(fmt(1000001, a))
    out.append(fmt(r.randint(2, 2000000), r.sample(range(1, 1000001), N)))
    return [c for c in out if valid(c)]

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
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1, 40)]+extra_cases()
    assert all(valid(c) for c in cases) and len(set(cases))==len(cases)
    for i,c in enumerate(cases): (data/f'{i}.in').write_text(c); (data/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()

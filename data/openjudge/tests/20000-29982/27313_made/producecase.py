import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/27313/\n# Accepted submission: 52520937\n# Source: http://cs101.openjudge.cn/practice/solution/52520937/\n# License: not declared on the submission page; no license is inferred.\n\nMOD = 10**9 + 7\nmax_n = 50\n\n# 预处理阶乘和逆阶乘\nfact = [1] * (max_n + 1)\nfor i in range(1, max_n + 1):\n    fact[i] = fact[i-1] * i % MOD\n\ninv_fact = [1] * (max_n + 1)\ninv_fact[max_n] = pow(fact[max_n], MOD-2, MOD)\nfor i in range(max_n - 1, -1, -1):\n    inv_fact[i] = inv_fact[i+1] * (i+1) % MOD\n\ndef compute_f(sub_s):\n    """计算满足符号序列sub_s的排列数"""\n    m = len(sub_s)\n    if m == 0:\n        return 1  # 空序列对应1个元素，只有1种排列\n\n    # dp[i][j]：长度为i的排列，满足前i-1个符号，以第j小元素结尾的数量（1-based）\n    dp = [[0] * (m + 2) for _ in range(m + 2)]\n    dp[1][1] = 1\n\n    for i in range(2, m + 2):\n        # 计算前缀和优化求和\n        prefix = [0] * i\n        for k in range(1, i):\n            prefix[k] = (prefix[k-1] + dp[i-1][k]) % MOD\n\n        sym = sub_s[i-2]\n        for j in range(1, i + 1):\n            if sym == \'<\':\n                # 前一个元素小于当前元素，求和1..j-1\n                dp[i][j] = prefix[j-1] if j-1 >= 1 else 0\n            else:  # \'>\'\n                # 前一个元素大于当前元素，求和j..i-1\n                dp[i][j] = (prefix[i-1] - prefix[j-1]) % MOD\n\n    # 总和即为该符号序列的排列数\n    res = 0\n    for j in range(1, m + 2):\n        res = (res + dp[m+1][j]) % MOD\n    return res\n\ndef main():\n    import sys\n    input = sys.stdin.read().split()\n    ptr = 0\n    n = int(input[ptr])\n    ptr +=1\n    p = list(map(int, input[ptr:ptr+n]))\n    ptr +=n\n\n    # 计算逆置换pos：pos[x]是元素x在p中的位置\n    pos = [0] * n\n    for i in range(n):\n        pos[p[i]] = i\n\n    # 检查每个边界是否恰好有一个元素向右穿过\n    valid = True\n    for i in range(n-1):\n        cnt = 0\n        for x in range(n):\n            if x <= i < pos[x]:\n                cnt +=1\n        if cnt != 1:\n            valid = False\n            break\n    if not valid:\n        print(0)\n        return\n\n    # 构建约束符号序列s，s[k]表示交换k和k+1的约束：\'<\'表示k在k+1前，\'>\'表示k+1在k前\n    s = [None] * (n-2)  # 共n-2个相邻交换对\n    for x in range(n):\n        if pos[x] > x:\n            # 向右移动，穿过边界x到pos[x]-1，相邻对k从x到pos[x]-2\n            for k in range(x, pos[x]-1):\n                if s[k] is not None and s[k] != \'<\':\n                    valid = False\n                s[k] = \'<\'\n        elif pos[x] < x:\n            # 向左移动，穿过边界pos[x]到x-1，相邻对k从pos[x]到x-2\n            for k in range(pos[x], x-1):\n                if s[k] is not None and s[k] != \'>\':\n                    valid = False\n                s[k] = \'>\'\n\n    if not valid:\n        print(0)\n        return\n\n    # 分块：按None分隔成连续的块\n    blocks = []\n    current = []\n    for c in s:\n        if c is None:\n            if current:\n                blocks.append(current)\n                current = []\n        else:\n            current.append(c)\n    if current:\n        blocks.append(current)\n\n    # 处理n=2的特殊情况（没有相邻交换对，只有一个交换）\n    if n == 2:\n        blocks.append([])\n\n    # 计算每个块的排列数乘积和块大小\n    prod = 1\n    sizes = []\n    for block in blocks:\n        f = compute_f(block)\n        prod = prod * f % MOD\n        sizes.append(len(block) + 1)  # 块大小=符号长度+1\n\n    # 计算组合数：(n-1)! / (size1! * size2! * ... * sizek!)\n    comb = fact[n-1]\n    for size in sizes:\n        comb = comb * inv_fact[size] % MOD\n\n    ans = prod * comb % MOD\n    print(ans)\n\nif __name__ == "__main__":\n    main()'
SAMPLE='3\n1 2 0\n'
EXTRA_CASE=None
GENERATOR_NAME='g27313'
def valid(text):
    """题面：第一行 N (2<=N<=50)；第二行 N 个整数，是 0..N-1 的排列（无重复）。"""
    lines = text.split('\n')
    if len(lines) != 3 or lines[2] != '':
        return False
    if not lines[0].isdigit() or lines[0] != str(int(lines[0])):
        return False
    n = int(lines[0])
    if not 2 <= n <= 50:
        return False
    toks = lines[1].split(' ')
    if len(toks) != n or any(not t.isdigit() or t != str(int(t)) for t in toks):
        return False
    return sorted(map(int, toks)) == list(range(n))

def apply_swaps(n, q):
    a = list(range(n))
    for i in q:
        a[i], a[i + 1] = a[i + 1], a[i]
    return a

def fmt(p):
    return f"{len(p)}\n{' '.join(map(str, p))}\n"

def zigzag_case(n):
    # 兔子顺序使相邻兔子先后关系交替（答案为欧拉锯齿数，最大的一类）
    q = list(range(0, n - 1, 2)) + list(range(1, n - 1, 2))
    return fmt(apply_swaps(n, q))

# 固定特例：最小规模、题面样例 2、不可达（答案 0）、满规模各类答案
SPECIAL_CASES = [
    '2\n1 0\n',            # n=2 唯一可达排列，答案 1
    '2\n0 1\n',            # n=2 恒等排列不可达，答案 0
    '4\n2 0 3 1\n',        # 题面样例 2，答案 2
    fmt(list(range(50))),   # n=50 恒等排列，答案 0
    fmt(apply_swaps(50, list(range(49)))),           # 兔子 0..48 依次，答案 1
    fmt(apply_swaps(50, list(range(48, -1, -1)))),   # 兔子 48..0 依次，答案 1
    zigzag_case(50),
    zigzag_case(49),
]

def g27313(r):
    kind = r.random()
    n = r.choice([r.randint(2, 50), r.randint(40, 50)])
    q = list(range(n - 1)); r.shuffle(q)
    p = apply_swaps(n, q)
    if kind < 0.15:
        # 任意排列（几乎都不可达）
        p = list(range(n)); r.shuffle(p)
    elif kind < 0.3 and n >= 3:
        # 可达排列再随机交换两个位置，构造“差一点”的不可达情形
        i, j = r.sample(range(n), 2)
        p[i], p[j] = p[j], p[i]
    return fmt(p)

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=90)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def scale_case(): return EXTRA_CASE
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    extra=scale_case(); fixed=[SAMPLE]+([extra] if extra else [])+SPECIAL_CASES
    cases=list(fixed); s=0
    while len(cases)<40:
        s+=1; c=globals()[GENERATOR_NAME](random.Random(s))
        if c not in cases: cases.append(c)
    assert len(cases)==40 and len(set(cases))==40 and all(valid(c) for c in cases)
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()

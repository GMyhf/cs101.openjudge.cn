import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# External reference: statistics page /practice/20169/\n# Accepted submission: 52720771\n# Source: http://cs101.openjudge.cn/practice/solution/52720771/\n# License: not declared on the submission page; no license is inferred.\n\n# 逐行读入：每次读取一整行字符串\nimport sys\n\ninput = sys.stdin.readline\n\ndef find(parent, x):  # 查找编号x的祖先（迭代写法：链长可达 n=30000，递归会超过默认递归深度）\n    root = x\n    while parent[root] != root:\n        root = parent[root]\n    while parent[x] != root:\n        parent[x], x = root, parent[x]\n    return root\n\ndef main():\n    T = int(input())\n\n    for _ in range(T):\n        n, m = map(int, input().split())\n\n        parent = list(range(n + 1))\n\n        for _ in range(m):\n            x, y = map(int, input().split())\n\n            rx, ry = find(parent, x), find(parent, y)\n\n            if rx != ry:\n                parent[rx] = ry\n\n        ans = [str(find(parent, i)) for i in range(1, n + 1)]\n        print(" ".join(ans))\n\nif __name__ == "__main__":\n    main()\n'
SAMPLE='2\n4 2\n1 2\n3 4\n5 4\n1 2\n2 3\n4 5\n1 3\n'
GENERATOR_NAME='g20169'

# 题面：第一行 T (T<=5)；每组第一行 n m (n,m<=30000)，接着 m 行 x y (1<=x,y<=n)。
# 题面另说「最终的队列数量远远小于 n」，这句话没有可操作的界（样例本身就是 n=4 剩 2 队），valid() 不核。


def valid(text):
    import re
    if not text.endswith("\n") or text.endswith("\n\n"):
        return False
    lines = text[:-1].split("\n")
    num = re.compile(r"0|[1-9]\d*")
    if not num.fullmatch(lines[0]):
        return False
    t = int(lines[0])
    if not 1 <= t <= 5:
        return False
    i = 1
    for _ in range(t):
        if i >= len(lines):
            return False
        hd = lines[i].split(" ")
        if len(hd) != 2 or not all(num.fullmatch(x) for x in hd):
            return False
        n, m = map(int, hd)
        if not 1 <= n <= 30000 or not 0 <= m <= 30000 or i + 1 + m > len(lines):
            return False
        for line in lines[i + 1:i + 1 + m]:
            xy = line.split(" ")
            if len(xy) != 2 or not all(num.fullmatch(x) for x in xy):
                return False
            if not all(1 <= int(x) <= n for x in xy):
                return False
        i += 1 + m
    return i == len(lines)


def _fmt(cases):
    return str(len(cases)) + "\n" + "\n".join(
        f"{n} {len(ops)}" + "".join(f"\n{a} {b}" for a, b in ops) for n, ops in cases) + "\n"


def _rand_ops(r, n, m, same_p=.05):
    ops = []
    for _ in range(m):
        if r.random() < same_p:
            x = r.randint(1, n)
            ops.append((x, x))
        else:
            ops.append((r.randint(1, n), r.randint(1, n)))
    return ops


def _chain(n, rev):
    return [(i + 1, i) if rev else (i, i + 1) for i in range(1, n)]


def _merge_tree(r, n, m):
    """先随机两两合并成少数几队（最终队列数远小于 n），剩下的操作随机重复（大多同队被忽略）。"""
    ops = []
    items = list(range(1, n + 1))
    r.shuffle(items)
    k = r.randint(1, 5)
    for idx in range(k, n):
        ops.append((items[idx], items[r.randrange(idx)]) if r.random() < .5 else (items[r.randrange(idx)], items[idx]))
    r.shuffle(ops)
    ops = ops[:m]
    while len(ops) < m:
        ops.append((r.randint(1, n), r.randint(1, n)))
    return ops


def g20169(r, s):
    if s == 1:         # 最小：n=1；m=0；x==y 的指令
        return _fmt([(1, []), (1, [(1, 1)]), (2, []), (2, [(2, 1)]), (3, [(1, 1), (3, 2), (2, 3), (1, 3)])])
    if s <= 12:        # 原来的形状，但 x、y 两个方向都有、含 x==y
        cases = []
        for _ in range(r.randint(1, 5)):
            n = r.randint(2, 12)
            cases.append((n, _rand_ops(r, n, r.randint(0, 2 * n), .15)))
        return _fmt(cases)
    if s <= 20:        # 中等规模
        cases = []
        for _ in range(r.randint(1, 5)):
            n = r.randint(50, 2000)
            cases.append((n, _merge_tree(r, n, r.randint(n, 2 * n)) if r.random() < .6 else _rand_ops(r, n, r.randint(1, n))))
        return _fmt(cases)
    if s <= 25:        # 长链：1→2→…→n 或反向，并查集不按秩合并时深度可达 n，递归 find 会爆栈
        n = r.choice((20000, 30000))
        ops = _chain(n, s % 2 == 0)
        ops += _rand_ops(r, n, 30000 - len(ops))
        return _fmt([(n, ops)] + ([(n, _chain(n, s % 2 == 1))] if s >= 24 else []))
    # data/ 合计须 <= 10MB：满规模（单个 .in 近 1MB）只留 24、25（双长链）、26、36 四组，其余缩到中等规模
    if s == 26:        # 满规模 n=m=30000，两组（单个 .in 控制在 1MB 内）
        return _fmt([(30000, _merge_tree(r, 30000, 30000)), (30000, _rand_ops(r, 30000, 30000))])
    if s <= 31:        # n=m=10000，两组
        return _fmt([(10000, _merge_tree(r, 10000, 10000)), (10000, _rand_ops(r, 10000, 10000))])
    if s <= 35:        # T=5，规模稍小
        return _fmt([(4000, _merge_tree(r, 4000, 4000) if i % 2 else _rand_ops(r, 4000, 4000)) for i in range(5)])
    if s == 36:
        return _fmt([(30000, _merge_tree(r, 30000, 30000)), (30000, _chain(30000, s % 2 == 0))])
    return _fmt([(10000, _merge_tree(r, 10000, 10000)), (10000, _chain(10000, s % 2 == 0))])

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=[SAMPLE]+(['8\n','9\n'] if GENERATOR_NAME == 'g22007' else [])+[g20169(random.Random(s), s) for s in range(1, 40)]
    for i,c in enumerate(cases): assert valid(c) and len(c) <= 1 << 20, i
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()

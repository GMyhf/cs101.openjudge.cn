import random
REFERENCE='# External reference: /practice/30934/statistics/\n# Accepted submission: 52760566\n# Source: http://cs101.openjudge.cn/practice/solution/52760566/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\n\ndef solve():\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n    \n    it = iter(input_data)\n    T = int(next(it))\n    results = []\n    \n    for _ in range(T):\n        N = int(next(it))\n        # 使用数组存储每个节点的左右孩子，索引从 1 到 N\n        left_child = [0] * (N + 1)\n        right_child = [0] * (N + 1)\n        \n        for i in range(1, N + 1):\n            l = int(next(it))\n            r = int(next(it))\n            left_child[i] = l\n            right_child[i] = r\n            \n        # 定义递归检查镜像的函数\n        def is_mirror(n1, n2):\n            # 两个节点都为空，说明这部分是对称的\n            if n1 == -1 and n2 == -1:\n                return True\n            # 只有一个为空，不对称\n            if n1 == -1 or n2 == -1:\n                return False\n            # 都不为空，继续递归检查：\n            # n1的左孩子 对应 n2的右孩子\n            # n1的右孩子 对应 n2的左孩子\n            return (is_mirror(left_child[n1], right_child[n2]) and \n                    is_mirror(right_child[n1], left_child[n2]))\n        \n        # 如果只有根节点，天然对称；否则比较根的左右孩子\n        if N == 1:\n            results.append("YES")\n        else:\n            if is_mirror(left_child[1], right_child[1]):\n                results.append("YES")\n            else:\n                results.append("NO")\n                \n    print("\\n".join(results))\n\nif __name__ == "__main__":\n    solve()'
SAMPLE='2\n7\n2 3\n4 5\n6 7\n-1 -1\n-1 -1\n-1 -1\n-1 -1\n4\n2 3\n-1 4\n-1 -1\n-1 -1\n'
GENERATOR_NAME='g30934'
CPP=False
import re, sys
_INT = re.compile(r'(0|-?[1-9][0-9]*)$')
def valid(text):
    """题面约束：第 1 行 T（1<=T<=30）；每棵树：一行 N（1<=N<=1000），接下来 N 行每行两个整数
    （节点 i 的左、右孩子编号，没有用 -1）。结构性：1 号为根，编号 1~N 构成一棵二叉树
    （孩子编号在 2..N 或 -1，每个非根结点恰有一个父亲，且都能从根到达）。"""
    lines = text.split('\n')
    if lines and lines[-1] == '':
        lines.pop()
    if not lines:
        return False
    def ints(line, k):
        tok = line.split()
        if len(tok) != k or not all(_INT.match(t) for t in tok):
            return None
        return list(map(int, tok))
    p = 0
    t = ints(lines[p], 1); p += 1
    if t is None or not (1 <= t[0] <= 30):
        return False
    for _ in range(t[0]):
        if p >= len(lines):
            return False
        n = ints(lines[p], 1); p += 1
        if n is None or not (1 <= n[0] <= 1000):
            return False
        n = n[0]
        if p + n > len(lines):
            return False
        ch = [None]
        for i in range(n):
            row = ints(lines[p + i], 2)
            if row is None:
                return False
            ch.append(row)
        p += n
        par = [0] * (n + 1)
        for i in range(1, n + 1):
            for c in ch[i]:
                if c == -1:
                    continue
                if not (2 <= c <= n) or par[c]:
                    return False
                par[c] = i
        if any(par[i] == 0 for i in range(2, n + 1)):
            return False
        seen = {1}; st = [1]
        while st:
            u = st.pop()
            for c in ch[u]:
                if c != -1 and c not in seen:
                    seen.add(c); st.append(c)
        if len(seen) != n:
            return False
    return p == len(lines)

# ---- 形状工具：形状用嵌套 (左, 右) 元组表示，None 表示空 ----
def _mirror(s):
    return None if s is None else (_mirror(s[1]), _mirror(s[0]))

def _rand_shape(r, k):
    """k 个结点的随机形状：逐个挂到随机空位上。"""
    if k == 0:
        return None
    kids = [[None, None]]; slots = [(0, 0), (0, 1)]
    for v in range(1, k):
        j = r.randrange(len(slots)); u, side = slots[j]; slots[j] = slots[-1]; slots.pop()
        kids.append([None, None]); kids[u][side] = v
        slots.append((v, 0)); slots.append((v, 1))
    def build(u):
        return (None if kids[u][0] is None else build(kids[u][0]),
                None if kids[u][1] is None else build(kids[u][1]))
    return build(0)

def _chain(r, k):
    s = None
    for _ in range(k):
        s = (s, None) if r.random() < 0.5 else (None, s)
    return s

def _emit(r, s):
    """把形状写成题目格式：根编号 1，其余结点随机编号（形状里可能共享子元组，按遍历位置编号）。"""
    kids = []; st = [(s, -1, 0)]
    while st:
        x, par, side = st.pop()
        k = len(kids); kids.append([-1, -1])
        if par >= 0:
            kids[par][side] = k
        if x[1] is not None: st.append((x[1], k, 1))
        if x[0] is not None: st.append((x[0], k, 0))
    n = len(kids); ids = [1] + r.sample(range(2, n + 1), n - 1)
    rows = [None] * (n + 1)
    for k, (a, b) in enumerate(kids):
        rows[ids[k]] = f"{-1 if a < 0 else ids[a]} {-1 if b < 0 else ids[b]}"
    return [str(n)] + rows[1:]

def _sym(r, k, chain=False):
    a = _chain(r, k) if chain else _rand_shape(r, k)
    return (a, _mirror(a))

def _break(r, s):
    """沿随机路径走到一个空位挂上新叶子。对称树结点数为奇数，加一个后必不对称。"""
    side = r.randrange(2)
    new = (None, None) if s[side] is None else _break(r, s[side])
    return (new, s[1]) if side == 0 else (s[0], new)

def _same(r, k):
    """左右子树形状相同但不是镜像（除非该形状自身镜像对称）。"""
    while True:
        a = _rand_shape(r, k)
        if a != _mirror(a):
            return (a, a)

def _file(trees):
    out = [str(len(trees))]
    for t in trees:
        out += t
    return '\n'.join(out) + '\n'

def build_cases():
    sys.setrecursionlimit(20000)
    r = random.Random(30934)
    E = lambda s: _emit(r, s)
    cases = [SAMPLE]
    leaf = (None, None)
    cases.append(_file([E(leaf)]))                                          # N=1
    cases.append(_file([E((leaf, None)), E((None, leaf))]))                 # N=2，都是 NO
    cases.append(_file([E((leaf, leaf)), E(((leaf, None), None)), E((None, (None, leaf))),
                        E(((None, leaf), (leaf, None))), E(((leaf, None), (leaf, None)))]))
    # 小规模混合（YES/NO 各半）
    for k in range(16):
        trees = []
        for j in range(30):
            m = r.randint(0, 7)
            kind = j % 4
            if kind == 0: trees.append(E(_sym(r, m)))
            elif kind == 1: trees.append(E(_break(r, _sym(r, m))))
            elif kind == 2: trees.append(E(_rand_shape(r, r.randint(1, 15))))
            else: trees.append(E(_same(r, max(m, 2))))
        cases.append(_file(trees))
    # 中等规模
    for k in range(9):
        trees = []
        for j in range(30):
            m = r.randint(10, 50)
            kind = j % 3
            if kind == 0: trees.append(E(_sym(r, m)))
            elif kind == 1: trees.append(E(_break(r, _sym(r, m))))
            else: trees.append(E(_same(r, m)))
        cases.append(_file(trees))
    # 大规模：N 接近 1000，每个文件 30 棵
    cases.append(_file([E(_sym(r, 499)) for _ in range(30)]))                # 全 YES
    cases.append(_file([E(_break(r, _sym(r, 499))) for _ in range(30)]))     # 全 NO，N=1000
    cases.append(_file([E(_same(r, 499)) for _ in range(30)]))               # 左右相同而非镜像
    cases.append(_file([E(_sym(r, 499, chain=True)) for _ in range(30)]))    # 两条镜像长链，递归深 ~500
    cases.append(_file([E(_break(r, _sym(r, 499, chain=True))) for _ in range(30)]))
    cases.append(_file([E(_chain(r, 1000)) for _ in range(30)]))             # 单链 N=1000
    cases.append(_file([E(_rand_shape(r, 1000)) for _ in range(30)]))
    mix = []
    for j in range(30):
        mix.append(E(_sym(r, 499)) if j % 2 == 0 else E(_break(r, _sym(r, 499))))
    cases.append(_file(mix))
    # 完全二叉树（按 1..N 层序编号），N 遍历 1..30：只有 2^k-1 是 YES
    rows = []
    for n in range(1, 31):
        rows.append([str(n)] + [f"{2*i if 2*i<=n else -1} {2*i+1 if 2*i+1<=n else -1}" for i in range(1, n + 1)])
    cases.append(_file(rows))
    # 满二叉树 N=511（YES）、N=1000 的完全二叉树（NO）
    for n in (511, 1000):
        cases.append(_file([[str(n)] + [f"{2*i if 2*i<=n else -1} {2*i+1 if 2*i+1<=n else -1}" for i in range(1, n + 1)]]))
    return cases

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
    cases=build_cases()
    assert cases[0]==SAMPLE
    assert len(set(cases))==len(cases), "存在重复测试组"
    for i,c in enumerate(cases):
        assert valid(c), f"第 {i} 组不满足题面约束"
        (data/f'{i}.in').write_text(c); (data/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()

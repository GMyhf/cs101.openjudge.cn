"""4081 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 31 组数据。

出处：build_001a
生成器与循环取自 scripts/build_001a.py（批次 001a），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 4081
SAMPLE_IN = 'dudduduudu\n'
SAMPLE_OUT = '2 => 4\n'
REFERENCE_SOURCE = """# 迭代实现（原递归版在 1 万层的链上会爆栈）：
# 左儿子右兄弟中，第 k 个孩子的二叉深度 = 父结点二叉深度 + k
s = input().strip()
h1 = h2 = 0
stack = [[0, 0]]  # [二叉深度, 已见孩子数]
for c in s:
    if c == 'd':
        top = stack[-1]
        top[1] += 1
        bd = top[0] + top[1]
        stack.append([bd, 0])
        h1 = max(h1, len(stack) - 1)
        h2 = max(h2, bd)
    else:
        stack.pop()
print(h1, '=>', h2)
"""

def g4081(r):
    node_count = r.randint(2, 80)
    children = [[] for _ in range(node_count)]
    for node in range(1, node_count):
        children[r.randrange(node)].append(node)

    def encode(node):
        result = []
        for child in children[node]:
            result.append("d")
            result.append(encode(child))
            result.append("u")
        return "".join(result)

    return encode(0) + "\n"

def valid(text):
    """题面契约：一行由 u/d 组成的合法 DFS 序列，结点数 2..10000。"""
    if not text.endswith("\n") or text.count("\n") != 1:
        return False
    s = text[:-1]
    if not s or set(s) - {"u", "d"}:
        return False
    depth = 0
    for c in s:
        depth += 1 if c == "d" else -1
        if depth < 0:
            return False
    if depth != 0:
        return False
    nodes = len(s) // 2 + 1
    return 2 <= nodes <= 10000


def encode_parents(parent):
    """parent[i] < i（i>=1），按孩子编号顺序做 DFS，迭代输出 u/d 串。"""
    n = len(parent)
    children = [[] for _ in range(n)]
    for v in range(1, n):
        children[parent[v]].append(v)
    out = []
    stack = [(0, 0)]
    while stack:
        v, k = stack.pop()
        if k < len(children[v]):
            stack.append((v, k + 1))
            out.append("d")
            stack.append((children[v][k], 0))
        elif v != 0:
            out.append("u")
    return "".join(out) + "\n"


# 二叉高度上限：平台 Accepted 的 samplecode.py 用递归求二叉树高度，
# 递归深度约为 h2+2，Python 默认上限 1000。平台数据显然没有超过这个深度，
# 这里把 h2 压在 CAP 以内，保证参考实现（samplecode.py）在全部数据上可复算。
CAP = 900


def binary_height(parent):
    """parent[i] < i，孩子按编号排序：第 k 个孩子的二叉深度 = 父结点二叉深度 + k。"""
    bd = [0] * len(parent)
    last = {}
    for v in range(1, len(parent)):
        p = parent[v]
        bd[v] = (bd[last[p]] if p in last else bd[p]) + 1
        last[p] = v
    return max(bd)


def capped(parent):
    assert binary_height(parent) <= CAP, binary_height(parent)
    return encode_parents(parent)


def extra_cases():
    """补规模与形状：题面上限 10000 个结点，原数据最多 80 个。
    所有大组的二叉高度都不超过 CAP（见上）。"""
    r = random.Random(NUMBER * 7 + 1)
    N = 10000
    cases = []
    cases.append("du\n")                                       # 最小：2 个结点
    cases.append("dudu\n")                                     # 3 个结点，根有两个孩子
    # 12 条长链挂在根下：h1=833，h2=12+833 附近
    par = [-1]
    heads = 12
    length = (N - 1) // heads
    for k in range(heads):
        prev = 0
        for _ in range(length + (1 if k < (N - 1) % heads else 0)):
            par.append(prev)
            prev = len(par) - 1
    cases.append(capped(par))
    # 宽菊花：根有 880 个孩子，前几个孩子再挂一大把孩子；h1=2，h2≈880
    par = [-1] + [0] * 880
    child = 1
    while len(par) < N:
        room = CAP - 20 - child          # 第 child 个孩子二叉深度为 child
        for _ in range(min(room, N - len(par))):
            par.append(child)
        child += 1
    cases.append(capped(par))
    cases.append(capped([-1] + [r.randrange(v) for v in range(1, N)]))           # 随机树
    # 偏深：优先挂在最近几个结点下，超出 CAP 时改挂到随机的浅结点
    par = [-1]
    bd = [0]
    last = {}
    for v in range(1, N):
        p = max(0, v - r.randint(1, 3))
        while (bd[last[p]] if p in last else bd[p]) + 1 > CAP:
            p = r.randrange(v)
        par.append(p)
        bd.append((bd[last[p]] if p in last else bd[p]) + 1)
        last[p] = v
    cases.append(capped(par))
    cases.append(capped([-1] + [(v - 1) // 2 for v in range(1, N)]))             # 完全二叉
    cases.append(capped([-1] + [(v - 1) // 10 for v in range(1, N)]))            # 十叉
    # 毛毛虫：主干 800 节，每节先接下一节主干、再挂若干叶子；h1≈800
    par = [-1]
    spine = 0
    for step in range(800):
        if len(par) >= N:
            break
        par.append(spine)
        nxt = len(par) - 1
        for _ in range(r.randint(8, 14)):
            if len(par) < N:
                par.append(spine)
        spine = nxt
    while len(par) < N:                  # 余下的作为根的孩子补齐（二叉深度只到几百）
        par.append(0)
    cases.append(capped(par))
    # 前段是链、中间结点挂一大把兄弟：二叉高度由兄弟数主导
    par = [-1] + list(range(299)) + [150] * 600
    extra = list(range(300, 900))        # 结点 150 新挂的孩子，二叉深度 152..751
    i = 0
    while len(par) < N:
        e = extra[i]
        room = CAP - (e - 300 + 152) - 1
        for _ in range(min(max(room, 0), N - len(par))):
            par.append(e)
        i += 1
    cases.append(capped(par))
    cases.append(capped([-1] + [r.randrange(max(0, v - 50), v) for v in range(1, 5001)]))
    return cases


def build_cases():
    return [SAMPLE_IN] + [g4081(random.Random(NUMBER + i)) for i in range(1, 20)] + extra_cases()

def solve_reference(content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE)
        handle.flush()
        result = subprocess.run(["python3", handle.name], input=content, text=True,
                                capture_output=True, timeout=120, check=True)
    return result.stdout


def main():
    cases = build_cases()
    assert cases[0] == SAMPLE_IN, "第 0 组必须是题面样例"
    assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split(), "参考解法跑不出样例输出"
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for index, content in enumerate(cases):
        assert valid(content), index
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")


if __name__ == "__main__":
    main()

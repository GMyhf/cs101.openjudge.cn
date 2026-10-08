import random
REFERENCE='# External reference: /practice/29656/statistics/\n# Accepted submission: 52686108\n# Source: http://cs101.openjudge.cn/practice/solution/52686108/\n# License: not declared on the submission page; no license is inferred.\n\nn = int(input())\nleft = [0] * (n + 1)\nright = [0] * (n + 1)\nparent = [0] * (n + 1)\n\nfor i in range(1, n + 1):\n    l, r = map(int, input().split())\n    left[i] = l\n    right[i] = r\n    if l:\n        parent[l] = i\n    if r:\n        parent[r] = i\n\n# 后序遍历计算 left_len 和 right_len（一直向左/右的节点数，包括自身）\nleft_len = [1] * (n + 1)\nright_len = [1] * (n + 1)\nstack = [(1, 0)]  # (node, state) 0=未处理子节点, 1=子节点已处理\norder = []\nwhile stack:\n    u, state = stack.pop()\n    if state == 0:\n        stack.append((u, 1))\n        if right[u]:\n            stack.append((right[u], 0))\n        if left[u]:\n            stack.append((left[u], 0))\n    else:\n        order.append(u)\n\nfor u in order:\n    if left[u]:\n        left_len[u] = 1 + left_len[left[u]]\n    if right[u]:\n        right_len[u] = 1 + right_len[right[u]]\n\n# 计算 up_len（向上直线可达节点数，包括自身）\n# 修正：题面不保证父节点编号小于子节点，须按自顶向下的顺序（后序的逆序）计算，\n# 原写法 for v in range(2, n + 1) 会在父亲编号更大时读到未计算的 up_len[p]。\nup_len = [1] * (n + 1)  # 根节点 up_len[1]=1\nfor v in reversed(order):\n    if v == 1:\n        continue\n    p = parent[v]\n    # 判断是否与父节点的方向一致，且父节点也满足相同方向（或父节点为根）\n    if (left[p] == v and (p == 1 or (parent[p] and left[parent[p]] == p))) or \\\n       (right[p] == v and (p == 1 or (parent[p] and right[parent[p]] == p))):\n        up_len[v] = up_len[p] + 1\n    else:\n        up_len[v] = 2   # 只能到自身和父节点\n\nbest_cnt = -1\nbest_node = -1\nfor v in range(1, n + 1):\n    cnt = left_len[v] + right_len[v] + up_len[v] - 2   # 减去重复的自身（被加了3次，应只算1次）\n    if cnt > best_cnt or (cnt == best_cnt and v < best_node):\n        best_cnt = cnt\n        best_node = v\n\nprint(best_node, best_cnt)'
SAMPLE='10\n2 3\n4 5\n0 0\n0 0\n6 7\n8 9\n0 0\n10 0\n0 0\n0 0\n'
GENERATOR_NAME='g29656'
def g29656(r):
    n = r.randint(1, 100); left = [0] * (n + 1); right = [0] * (n + 1)
    free = [1]
    for node in range(2, n + 1):
        while True:
            parent = r.choice(free)
            side = r.choice((0, 1))
            if side == 0 and not left[parent]: left[parent] = node; break
            if side == 1 and not right[parent]: right[parent] = node; break
        free.append(node)
        if left[parent] and right[parent]: free.remove(parent)
    return f"{n}\n" + "\n".join(f"{left[i]} {right[i]}" for i in range(1, n + 1)) + "\n"

from pathlib import Path
import random, subprocess, sys, tempfile


def valid(text):
    """题面：第一行 N（1<=N<=100000），节点编号 1~N，根为 1；接下来 N 行，第 i 行为 i 的左、右子节点编号（0 表示无）；
    保证构成一棵合理的二叉树：除根外每个节点恰好作为一次子节点，根不作子节点，全部从 1 可达。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    try:
        if len(lines[0].split()) != 1:
            return False
        n = int(lines[0])
        if not 1 <= n <= 100000 or len(lines) != n + 1:
            return False
        seen = [0] * (n + 1)
        kids = [()] * (n + 1)
        for i in range(1, n + 1):
            toks = lines[i].split()
            if len(toks) != 2:
                return False
            l, r = int(toks[0]), int(toks[1])
            for c in (l, r):
                if not 0 <= c <= n or c == 1:
                    return False
                if c:
                    if seen[c]:
                        return False
                    seen[c] = 1
            kids[i] = (l, r)
    except ValueError:
        return False
    if sum(seen) != n - 1:
        return False
    stack, cnt = [1], 0
    vis = [0] * (n + 1)
    while stack:
        u = stack.pop()
        if vis[u]:
            return False
        vis[u] = 1; cnt += 1
        stack.extend(c for c in kids[u] if c)
    return cnt == n


def _emit(r, left, right, relabel=True):
    """left/right 以 0..n-1 编号（0 为根，-1 表示无），随机重标号（根固定为 1）后输出。"""
    n = len(left)
    lab = list(range(2, n + 1))
    if relabel:
        r.shuffle(lab)
    lab = [1] + lab
    L = [0] * (n + 1); R = [0] * (n + 1)
    for u in range(n):
        L[lab[u]] = lab[left[u]] if left[u] >= 0 else 0
        R[lab[u]] = lab[right[u]] if right[u] >= 0 else 0
    return f"{n}\n" + "\n".join(f"{L[i]} {R[i]}" for i in range(1, n + 1)) + "\n"


def _grow(r, n, keep):
    """随机生长：新节点以概率 keep 沿父亲所在方向继续延伸，形成较长的直线段。"""
    left = [-1] * n; right = [-1] * n; side = [0] * n
    free = [0]
    pos = {0: 0}
    last = 0
    for v in range(1, n):
        if r.random() < keep and (left[last] < 0 or right[last] < 0):
            u = last
            d = side[u] if (left[u] < 0 if side[u] == 0 else right[u] < 0) else (1 - side[u])
        else:
            u = free[r.randrange(len(free))]
            d = r.randint(0, 1)
            if (left[u] if d == 0 else right[u]) >= 0:
                d = 1 - d
        if d == 0: left[u] = v
        else: right[u] = v
        side[v] = d
        if left[u] >= 0 and right[u] >= 0:
            i = pos.pop(u); tail = free.pop()
            if tail != u:
                free[i] = tail; pos[tail] = i
        pos[v] = len(free); free.append(v)
        last = v
    return left, right


def special_case(index):
    """第 25..39 组：补 N=1/2、N=1e5 长链、之字形、完全二叉树、长直线段随机树、并列最大（取最小编号）等。"""
    r = random.Random(296560 + index)
    k = index - 25
    if k == 0:
        return "1\n0 0\n"
    if k == 1:
        return "2\n2 0\n0 0\n"
    if k == 2:
        return "2\n0 2\n0 0\n"
    if k in (3, 4):                           # 小规模长直线段树，可暴力核对
        return _emit(r, *_grow(r, [60, 500][k - 3], 0.7))
    if k == 5:                                # N=1e5 一条向左的长链
        n = 100000
        return _emit(r, list(range(1, n)) + [-1], [-1] * n)
    if k == 6:                                # 之字形链：每条直线最多 3 个点，大量并列
        n = 100000
        left = [-1] * n; right = [-1] * n
        for u in range(n - 1):
            if u % 2: left[u] = u + 1
            else: right[u] = u + 1
        return _emit(r, left, right)
    if k == 7:                                # 完全二叉树
        n = 100000
        left = [2 * u + 1 if 2 * u + 1 < n else -1 for u in range(n)]
        right = [2 * u + 2 if 2 * u + 2 < n else -1 for u in range(n)]
        return _emit(r, left, right)
    if k == 8:                                # 根先向右走一段，再在末端分出很长的左链和右链（最佳点在深处）
        n = 100000
        left = [-1] * n; right = [-1] * n
        a = 30000
        for u in range(a - 1): right[u] = u + 1
        b = a - 1                             # 拐点
        cur = b; nxt = a
        for _ in range(35000):                # 左链
            left[cur] = nxt; cur = nxt; nxt += 1
        cur = b
        while nxt < n:                        # 继续右链
            right[cur] = nxt; cur = nxt; nxt += 1
        return _emit(r, left, right)
    if k == 9:                                # 两段等长的独立直线，并列最大，考察取最小编号
        n = 99999
        left = [-1] * n; right = [-1] * n
        h = (n - 1) // 2
        right[0] = 1; left[0] = 1 + h
        for i in range(1, h):                 # 根右孩子起一条左链
            left[i] = i + 1
        for i in range(1 + h, n - 1):         # 根左孩子起一条右链
            right[i] = i + 1
        return _emit(r, left, right)
    if k in (10, 11):
        return _emit(r, *_grow(r, 100000, 0.0))
    if k in (12, 13):
        return _emit(r, *_grow(r, 100000, [0.9, 0.99][k - 12]))
    return _emit(r, *_grow(r, 100000, 0.6))

REFERENCE = REFERENCE
def solve(text):
    with tempfile.TemporaryDirectory(prefix='producecase-run-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        result=subprocess.run([sys.executable, str(p)], input=text, text=True, capture_output=True, timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) if seed < 25 else special_case(seed) for seed in range(1, 40)]
    assert all(valid(c) for c in cases) and len(set(cases)) == len(cases)
    for i, case in enumerate(cases):
        (data/f'{i}.in').write_text(case); (data/f'{i}.out').write_text(solve(case))
if __name__=='__main__': main()

import random
REFERENCE="# External reference: /practice/29647/statistics/\n# Accepted submission: 52829529\n# Source: http://cs101.openjudge.cn/practice/solution/52829529/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\n\ndef solve():\n    # 增加递归深度限制，防止树退化为链时导致栈溢出\n    sys.setrecursionlimit(2000)\n    \n    # 一次性读取所有输入数据\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n    \n    n = int(input_data[0])\n    \n    # 存储快乐指数，下标从 1 开始\n    r = [0] * (n + 1)\n    for i in range(1, n + 1):\n        r[i] = int(input_data[i])\n    \n    # 构建邻接表和记录是否有上司\n    adj = [[] for _ in range(n + 1)]\n    has_parent = [False] * (n + 1)\n    \n    idx = n + 1\n    # 读取 n - 1 条关系\n    for _ in range(n - 1):\n        if idx >= len(input_data):\n            break\n        l = int(input_data[idx])\n        k = int(input_data[idx + 1])\n        adj[k].append(l)  # k 是 l 的直接上司\n        has_parent[l] = True\n        idx += 2\n        \n    # 寻找根节点（没有直接上司的职员）\n    root = 1\n    for i in range(1, n + 1):\n        if not has_parent[i]:\n            root = i\n            break\n            \n    # 定义树形 DP 的 DFS 函数\n    # 返回一个元组 (dp[u][0], dp[u][1])\n    # dp[u][0] 表示 u 不参加的最大值，dp[u][1] 表示 u 参加的最大值\n    def dfs(u):\n        dp_u_0 = 0\n        dp_u_1 = r[u]\n        \n        for v in adj[u]:\n            dp_v_0, dp_v_1 = dfs(v)\n            # u 不参加：子节点 v 可以参加，也可以不参加\n            dp_u_0 += max(dp_v_0, dp_v_1)\n            # u 参加：子节点 v 绝对不能参加\n            dp_u_1 += dp_v_0\n            \n        return dp_u_0, dp_u_1\n\n    # 从根节点开始搜索\n    ans_0, ans_1 = dfs(root)\n    \n    # 输出最大快乐指数\n    print(max(ans_0, ans_1))\n\nif __name__ == '__main__':\n    solve()"
SAMPLE='7\n1\n1\n1\n1\n1\n1\n1\n1 3\n2 3\n6 4\n7 4\n4 5\n3 5\n'
GENERATOR_NAME='g29647'
def g29647(r):
    n = r.randint(2, 80); value = [r.randint(0, 100) for _ in range(n)]
    edges = [f"{i} {r.randint(1, i - 1)}" for i in range(2, n + 1)]
    return f"{n}\n" + "\n".join(map(str, value)) + "\n" + "\n".join(edges) + "\n"

from pathlib import Path
import random, subprocess, sys, tempfile


def valid(text):
    """题面：第一行 n（1<=n<=1000）；接下来 n 行各一个整数 ri（-128<=ri<=127）；
    再 n-1 行，每行 l k（1<=l,k<=n），k 是 l 的直接上司；关系保证是一棵树。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    try:
        if len(lines[0].split()) != 1:
            return False
        n = int(lines[0])
        if not 1 <= n <= 1000 or len(lines) != 2 * n:
            return False
        for line in lines[1:n + 1]:
            toks = line.split()
            if len(toks) != 1 or not -128 <= int(toks[0]) <= 127:
                return False
        parent = [0] * (n + 1)
        for line in lines[n + 1:]:
            toks = line.split()
            if len(toks) != 2:
                return False
            l, k = map(int, toks)
            if not (1 <= l <= n and 1 <= k <= n) or l == k or parent[l]:
                return False
            parent[l] = k
    except ValueError:
        return False
    roots = [v for v in range(1, n + 1) if not parent[v]]
    if len(roots) != 1:
        return False
    # 无环：从每个点沿上司走，必须走到根
    state = [0] * (n + 1)          # 0 未访问，1 在路径上，2 已确认可达根
    state[roots[0]] = 2
    for v in range(1, n + 1):
        path = []
        while state[v] == 0:
            state[v] = 1; path.append(v); v = parent[v]
        if state[v] == 1:
            return False
        for u in path:
            state[u] = 2
    return True


def _emit(r, n, par, value, shuffle=True):
    """par[v] 为 v 的上司（根为 0）；随机重标号使根不总是 1，并打乱关系行的顺序。"""
    perm = list(range(1, n + 1))
    r.shuffle(perm)
    lab = [0] + perm
    val = [0] * (n + 1)
    for v in range(1, n + 1):
        val[lab[v]] = value[v - 1]
    edges = [(lab[v], lab[par[v]]) for v in range(1, n + 1) if par[v]]
    if shuffle:
        r.shuffle(edges)
    body = "\n".join(map(str, val[1:])) + "\n"
    if edges:
        body += "\n".join(f"{a} {b}" for a, b in edges) + "\n"
    return f"{n}\n" + body


def _values(r, n, lo=-128, hi=127):
    v = [r.randint(lo, hi) for _ in range(n)]
    if max(v) <= 0:                 # 保证至少一人快乐指数为正，避免“一个都不请”的歧义
        v[r.randrange(n)] = r.randint(1, 127)
    return v


def special_case(index):
    """第 25..39 组：补 n=1、n=1000、负快乐指数、链/菊花/二叉/随机深树、根不为 1 等情形。"""
    r = random.Random(296470 + index)
    k = index - 25
    if k == 0:
        return "1\n5\n"
    if k == 1:
        return "2\n-3\n7\n2 1\n"            # 根值为负，子为正
    if k in (2, 3, 4, 5):                     # 小规模、带负值，可暴力核对
        n = [3, 8, 12, 16][k - 2]
        par = [0, 0] + [r.randint(1, v - 1) for v in range(2, n + 1)]
        return _emit(r, n, par, _values(r, n))
    n = 1000
    if k == 6:                                # 长链（深度 1000）
        par = [0, 0] + list(range(1, n))
        val = _values(r, n)
    elif k == 7:                              # 长链，正负交替
        par = [0, 0] + list(range(1, n))
        val = [127 if i % 2 else -128 for i in range(n)]
    elif k == 8:                              # 菊花：根值很大，叶子小
        par = [0, 0] + [1] * (n - 1)
        val = [127] + [r.randint(-128, 0) for _ in range(n - 1)]
        val[r.randrange(1, n)] = 1
    elif k == 9:                              # 菊花：根值小、叶子正
        par = [0, 0] + [1] * (n - 1)
        val = [-128] + [r.randint(-5, 127) for _ in range(n - 1)]
    elif k == 10:                             # 完全二叉树
        par = [0, 0] + [v // 2 for v in range(2, n + 1)]
        val = _values(r, n)
    elif k == 11:                             # 全为 127
        par = [0, 0] + [r.randint(1, v - 1) for v in range(2, n + 1)]
        val = [127] * n
    elif k == 12:                             # 绝大多数为负
        par = [0, 0] + [r.randint(max(1, v - 5), v - 1) for v in range(2, n + 1)]
        val = _values(r, n, -128, 10)
    elif k == 13:                             # 深随机树（父亲在前 3 个之内）
        par = [0, 0] + [r.randint(max(1, v - 3), v - 1) for v in range(2, n + 1)]
        val = _values(r, n)
    else:                                     # 均匀随机树
        par = [0, 0] + [r.randint(1, v - 1) for v in range(2, n + 1)]
        val = _values(r, n)
    return _emit(r, n, par, val)

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

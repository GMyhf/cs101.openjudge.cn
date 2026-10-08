import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE="# External reference: cs101.openjudge.cn practice/20136 statistics, Accepted solution 22633121.\n# Source: http://cs101.openjudge.cn/practice/solution/22633121/\n# Statistics: http://cs101.openjudge.cn/practice/20136/statistics/\n# License: not declared on submission page; no license inferred\ndef zoutong(z,x,y):\n    if x > y:\n        ans = zoutong(y,x)\n    ans = True\n    if z>x and y>z:\n        ans = False\n    else:\n        for i in range(x,y):\n            if (i+1) not in portal[i]:\n                ans = False\n                break\n    return ans\n\npolicerick,t = map(int,input().split())\ncheck = []\nportal = {}\nfor i in range(t):\n    tem = list(map(int,input().split()))\n    portal[i] = tem[1:]\n    if len(portal[i])>2:\n        check.append(i)\n\nif policerick == 1:\n    print('YES!')\nelse:\n    flag = False\n    for i in check:\n        if flag == False:\n            for x in range(len(portal[i])-1):\n                if flag == False:\n                    for y in range(len(portal[i])-x-1):\n                        if flag == False:\n                            if zoutong(i,portal[i][x],portal[i][x+y+1]):\n                                if portal[i][x+y+1]-portal[i][x]+1 >= policerick:\n                                    flag = True\n        else:\n            break\n\n    if flag == True:\n        print('YES!')\n    else:\n        print('NO!')\n"
SAMPLE='7 15\n0 1\n1 0 2 6\n2 1 3 7 14\n3 2 4\n4 3 5\n5 4 6\n6 1 5\n7 2 8\n8 7 9\n9 8 10\n10 9 11\n11 10 12\n12 11 13\n13 12 14\n14 2 13\n'
GENERATOR_NAME='g20136'
SAMPLE2='2 3\n0 1\n1 0 2\n2 1\n'


def parse_graph(text):
    """解析输入；格式不对返回 None。"""
    if not text.endswith('\n'):
        return None
    lines = text[:-1].split('\n')
    try:
        head = list(map(int, lines[0].split()))
        if len(head) != 2:
            return None
        n, t = head
        if n <= 0 or t <= 2 or len(lines) != t + 1:
            return None
        adj = []
        for i, line in enumerate(lines[1:]):
            v = list(map(int, line.split()))
            if not v or v[0] != i:
                return None
            nb = v[1:]
            if len(set(nb)) != len(nb) or any(not (0 <= u < t) or u == i for u in nb):
                return None
            adj.append(nb)
    except ValueError:
        return None
    return n, t, adj


def cycle_blocks(t, adj):
    """返回所有双连通分量（以边集表示）。"""
    disc = [-1] * t; low = [0] * t; timer = [0]; stack = []; blocks = []
    def dfs(root):
        it = [(root, -1, iter(adj[root]))]
        disc[root] = low[root] = timer[0]; timer[0] += 1
        while it:
            u, pu, nbrs = it[-1]
            advanced = False
            for w in nbrs:
                if disc[w] == -1:
                    stack.append((u, w)); disc[w] = low[w] = timer[0]; timer[0] += 1
                    it.append((w, u, iter(adj[w]))); advanced = True; break
                elif w != pu and disc[w] < disc[u]:
                    stack.append((u, w)); low[u] = min(low[u], disc[w])
            if advanced:
                continue
            it.pop()
            if it:
                p = it[-1][0]
                low[p] = min(low[p], low[u])
                if low[u] >= disc[p]:
                    comp = []
                    while True:
                        e = stack.pop(); comp.append(e)
                        if e == (p, u):
                            break
                    blocks.append(comp)
    dfs(0)
    return blocks, all(d != -1 for d in disc)


def valid(text):
    """题面：第一行 n（n>0）、t（t>2）；接下来 t 行，首个数为宇宙代号、其后为相邻宇宙（代号互不相同；
    参考解按第 i 行即 i 号宇宙读，样例亦然）。平行宇宙相互连通（0 号瑞城可到 1 号）。
    提示 3：两个闭环之间最多一个公共点；提示 4：每个闭环中除代号最小的分叉宇宙（联通数>2）外，
    其余宇宙沿某个方向递增。闭环里没有任何分叉宇宙时提示 4 无从谈起，按越界处理。"""
    g = parse_graph(text)
    if g is None:
        return False
    n, t, adj = g
    sets = [set(a) for a in adj]
    if any(i not in sets[u] for i in range(t) for u in adj[i]):
        return False                      # 邻接必须对称
    blocks, connected = cycle_blocks(t, adj)
    if not connected:
        return False
    for comp in blocks:
        if len(comp) == 1:
            continue
        verts = {x for e in comp for x in e}
        if len(comp) != len(verts):
            return False                  # 块里不止一个环 → 有两个闭环共用 >=2 个点
        branch = [v for v in verts if len(adj[v]) > 2]
        if not branch:
            return False
        b = min(branch)
        loc = {v: [w for w in adj[v] if w in verts and ((v, w) in comp or (w, v) in comp)] for v in verts}
        order = [b]; prev, cur = b, loc[b][0]
        while cur != b:
            order.append(cur); nxt = [w for w in loc[cur] if w != prev][0]; prev, cur = cur, nxt
        rest = order[1:]
        if not (all(x < y for x, y in zip(rest, rest[1:])) or all(x > y for x, y in zip(rest, rest[1:]))):
            return False
    return True


def build_cactus(r, t_target, p_cycle, cyc_len):
    """0 是挂在 1 上的叶子；从 1 出发按 BFS 依次挂桥边或闭环，闭环新点连续编号，挂点是该环代号最小的分叉宇宙。"""
    adj = {0: [1], 1: [0]}
    nxt = 2
    queue = [1]
    while nxt < t_target and queue:
        v = queue.pop(0) if r.random() < .6 else queue.pop(r.randrange(len(queue)))
        for _ in range(r.choice([1, 1, 2, 3])):
            if nxt >= t_target:
                break
            if r.random() < p_cycle and t_target - nxt >= 2:
                L = min(cyc_len(r), t_target - nxt + 1)     # 环上点数（含挂点 v）
                if L < 3:
                    L = 3
                if nxt + L - 1 > t_target:
                    break
                new = list(range(nxt, nxt + L - 1)); nxt += L - 1
                for a in new:
                    adj[a] = []
                for a, b in zip(new, new[1:]):
                    adj[a].append(b); adj[b].append(a)
                adj[v].append(new[0]); adj[new[0]].append(v)
                adj[v].append(new[-1]); adj[new[-1]].append(v)
                queue.extend(new)
            else:
                adj[nxt] = [v]; adj[v].append(nxt); queue.append(nxt); nxt += 1
        queue.append(v) if r.random() < .3 else None
    t = nxt
    return t, [sorted(adj[i]) for i in range(t)]


def max_cycle(t, adj):
    """生成结构下：环 = 挂点 v + 连续编号段 x..y（v 与 x、y 相邻，x..y 逐个相连）。"""
    best = 0
    for v in range(t):
        for x in adj[v]:
            if x <= v:
                continue
            y = x
            while y + 1 < t and (y + 1) in adj[y] and y + 1 not in adj[v]:
                y += 1
            if y + 1 < t and (y + 1) in adj[y] and y + 1 in adj[v] and y + 1 != x:
                best = max(best, y + 1 - x + 2)
    return best


def g20136(r):
    kind = r.randrange(5)
    if kind == 0:                                   # 小图
        t, adj = build_cactus(r, r.randint(3, 15), r.random(), lambda r: r.randint(3, 8))
    elif kind == 1:                                 # 中等
        t, adj = build_cactus(r, r.randint(50, 300), r.uniform(.1, .6), lambda r: r.randint(3, 40))
    elif kind == 2:                                 # 大图、长环
        t, adj = build_cactus(r, r.randint(1000, 3000), r.uniform(.05, .3), lambda r: r.choice([r.randint(3, 10), r.randint(100, 800)]))
    elif kind == 3:                                 # 树（没有闭环）
        t, adj = build_cactus(r, r.randint(3, 500), 0, None)
    else:                                           # 很多三角形 / 小环
        t, adj = build_cactus(r, r.randint(20, 400), .8, lambda r: r.randint(3, 5))
    c = max_cycle(t, adj)
    choice = r.randrange(6)
    if choice == 0:
        n = 1
    elif c and choice in (1, 2):
        n = c - 1                                   # 刚好够：环上点数 = n+1 → YES!
    elif c and choice == 3:
        n = c                                       # 差一个 → NO!
    elif choice == 4:
        n = 2
    else:
        n = r.randint(2, max(2, t))
    return f"{n} {t}\n" + "\n".join(f"{i} " + " ".join(map(str, adj[i])) for i in range(t)) + "\n"


def build_cases():
    cases = [SAMPLE, SAMPLE2]
    seed = 1
    while len(cases) < 40:
        text = g20136(random.Random(seed)); seed += 1
        if text not in cases and valid(text):
            cases.append(text)
    return cases

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        src=Path(d)/'main.py'; src.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(src)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=build_cases()
    assert all(valid(c) for c in cases)
    for i,text in enumerate(cases):
        (data/f'{i}.in').write_text(text); (data/f'{i}.out').write_text(run(text))
if __name__=='__main__': main()

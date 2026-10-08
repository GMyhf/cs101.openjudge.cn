import random,subprocess,sys,tempfile
from pathlib import Path
def generate(number, seed):
    r = random.Random(number * 1_000_003 + seed)
    letters = "abcdefghijklmnopqrstuvwxyz"
    word = lambda a=2,b=8: "".join(r.choice(letters) for _ in range(r.randint(a,b)))
    if number==2184:
        a=[(r.randint(-20,30),r.randint(-20,30)) for _ in range(r.randint(2,14))];return f"{len(a)}\n"+"\n".join(f"{x} {y}" for x,y in a)+"\n"
    if number==2313:
        a=[r.randint(-10000,10000) for _ in range(r.randint(1,40))];return f"{len(a)}\n"+"\n".join(map(str,a))+"\n"
    if number==2755:
        a=[r.randint(1,40) for _ in range(r.randint(1,18))];return f"{len(a)}\n"+"\n".join(map(str,a))+"\n"
    if number==1837:
        c=r.randint(2,8);g=r.randint(2,8);p=sorted(r.sample(range(-15,16),c));w=sorted(r.sample(range(1,26),g));return f"{c} {g}\n"+" ".join(map(str,p))+"\n"+" ".join(map(str,w))+"\n"
    if number==2373:
        L=2*r.randint(8,35);a=r.randint(1,max(1,L//6));b=r.randint(a,min(L//2,a+8));rows=[]
        for _ in range(r.randint(1,8)):
            x,y=sorted(r.sample(range(L+1),2));rows.append((x,y))
        return f"{len(rows)} {L}\n{a} {b}\n"+"\n".join(f"{x} {y}" for x,y in rows)+"\n"
    if number==1204:
        h,w=8+r.randrange(5),8+r.randrange(5);grid=[[r.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(w)] for _ in range(h)];words=[]
        for y in range(min(6,h)):
            x=r.randrange(0,w-3);s="".join(grid[y][x:x+4]);words.append(s)
        return f"{h} {w} {len(words)}\n"+"\n".join("".join(x) for x in grid)+"\n"+"\n".join(words)+"\n"
    if number==2992:
        n=r.randint(2,16);a=[[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(i):a[i][j],a[j][i]=(3,r.randrange(3)) if r.randrange(2) else (r.randrange(3),3)
        return f"{n}\n"+"\n".join(" ".join(map(str,row)) for row in a)+"\n"
    if number==1084:
        rows=[]
        for _ in range(r.randint(1,3)):
            n=r.randint(1,3);total=2*n*(n+1);gone=sorted(r.sample(range(1,total+1),r.randint(0,min(total,5))));rows.append(f"{n}\n{len(gone)}"+(" "+" ".join(map(str,gone)) if gone else ""))
        return f"{len(rows)}\n"+"\n".join(rows)+"\n"
    if number==1251:
        n=r.randint(2,12);rows=[]
        for i in range(n-1):
            edges=[(j,r.randint(1,100)) for j in range(i+1,n) if j==i+1 or r.random()<.25];rows.append(chr(65+i)+f" {len(edges)} "+" ".join(f"{chr(65+j)} {c}" for j,c in edges))
        return f"{n}\n"+"\n".join(x.rstrip() for x in rows)+"\n0\n"
    if number==1390:
        cases=[]
        for _ in range(r.randint(1,3)):
            n=r.randint(1,20);cases.append(f"{n}\n"+" ".join(str(r.randint(1,n)) for _ in range(n)))
        return f"{len(cases)}\n"+"\n".join(cases)+"\n"
    if number==2191:return f"{r.randint(2,63)}\n"
    if number==2503:
        foreign=[word() for _ in range(5)];rows=[f"{word()} {x}" for x in foreign];queries=foreign[:3]+[word()];return "\n".join(rows)+"\n\n"+"\n".join(queries)+"\n"
    if number==2724:
        n=r.randint(3,20);rows=[f"s{seed}_{i} {r.randint(1,12)} {r.randint(1,28)}" for i in range(n)];return f"{n}\n"+"\n".join(rows)+"\n"
    if number==1273:
        n=r.randint(2,10);edges=[(i,i+1,r.randint(1,1000)) for i in range(1,n)];edges += [(r.randint(1,n-1),r.randint(2,n),r.randint(0,1000)) for _ in range(r.randint(0,8))];return f"{len(edges)} {n}\n"+"\n".join(f"{a} {b} {c}" for a,b,c in edges)+"\n"
    if number==1835:
        cases=[];cmds="forward back left right up down".split()
        for _ in range(r.randint(1,4)):
            a=[f"{r.choice(cmds)} {r.randint(1,10000)}" for _ in range(r.randint(1,20))];cases.append(f"{len(a)}\n"+"\n".join(a))
        return f"{len(cases)}\n"+"\n".join(cases)+"\n"
    if number==1905:
        rows=[f"{r.randint(1,10000)} {r.random()*20:.3f} {r.random()/10000:.7f}" for _ in range(r.randint(1,6))];return "\n".join(rows)+"\n-1 -1 -1\n"
    if number==1922:
        n=r.randint(1,15);rows=[(r.randint(1,40),r.randint(-200,500)) for _ in range(n)];rows[0]=(rows[0][0],r.randint(0,500));return f"{n}\n"+"\n".join(f"{a} {b}" for a,b in rows)+"\n0\n"
    if number==1936:return "\n".join(f"{word()} {word(5,18)}" for _ in range(r.randint(1,8)))+"\n"
    if number==2538:
        chars="1234567890-=WERTYUIOP[]\\SDFGHJKL;'XCVBNM,./ ";return "\n".join("".join(r.choice(chars) for _ in range(r.randint(1,60))) for _ in range(r.randint(1,6)))+"\n"
    if number==2982:
        base="534678912 672195348 198342567 859761423 426853791 713924856 961537284 287419635 345286179".split();shift=seed%9;grid=[row[shift:]+row[:shift] for row in base];
        for _ in range(12+seed%20):
            y,x=r.randrange(9),r.randrange(9);grid[y]=grid[y][:x]+"0"+grid[y][x+1:]
        return "1\n"+"\n".join(grid)+"\n"
    if number in NO_INPUT:return ""
    if number==1006:return "\n".join(" ".join(str(r.randint(0,365)) for _ in range(4)) for _ in range(r.randint(1,5)))+"\n-1 -1 -1 -1\n"
    if number==2159:
        n=r.randint(2,100);a="".join(r.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(n));b="".join(r.sample(list(a),len(a))) if seed%2 else a[:-1]+("A" if a[-1]!="A" else "B");return a+"\n"+b+"\n"
    if number==1113:
        w,h=r.randint(2,200),r.randint(2,200);x,y=r.randint(-100,100),r.randint(-100,100);return f"4 {r.randint(1,100)}\n{x} {y}\n{x} {y+h}\n{x+w} {y+h}\n{x+w} {y}\n"
    if number==2381:
        m=r.randint(2,20000);a=r.randint(0,min(10000,(2**32-2)//m));c=r.randint(0,10000);return f"{a} {c} {m} {r.randrange(m)}\n"
    if number==2186:
        n=r.randint(2,20);edges={(i,i+1) for i in range(1,n)}|{(n,1)}
        for _ in range(r.randint(0,30)):edges.add((r.randint(1,n),r.randint(1,n)))
        return f"{n} {len(edges)}\n"+"\n".join(f"{a} {b}" for a,b in sorted(edges))+"\n"
    if number==1236:
        n=r.randint(2,18);rows=[]
        for i in range(1,n+1):
            a=sorted({j for j in range(1,n+1) if j!=i and r.random()<.2});rows.append((" ".join(map(str,a))+" " if a else "")+"0")
        return f"{n}\n"+"\n".join(rows)+"\n"
    if number==1062:
        n=r.randint(1,12);rows=[f"{r.randint(1,10000)} {r.randint(1,20)} 0" for _ in range(n)];return f"{r.randint(1,10)} {n}\n"+"\n".join(rows)+"\n"
    if number==1067:return "\n".join(f"{r.randint(0,10**9)} {r.randint(0,10**9)}" for _ in range(r.randint(1,10)))+"\n"
    if number==1091:return f"{r.randint(1,15)} {r.randint(1,100000000)}\n"
    if number==1154:
        h,w=r.randint(1,7),r.randint(1,7);return f"{h} {w}\n"+"\n".join("".join(r.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(w)) for _ in range(h))+"\n"
    if number==1183:return f"{r.randint(1,60000)}\n"
    if number==1184:return f"{r.randint(0,999999):06d} {r.randint(0,999999):06d}\n"
    if number==2001:
        a={word(2,15) for _ in range(12)}
        while len(a)<8:a.add(word(2,15))
        return "\n".join(sorted(a))+"\n"
    if number==2141:
        key=list(letters);r.shuffle(key);msg="".join(r.choice(letters+letters.upper()+" ") for _ in range(r.randint(1,80)));return "".join(key)+"\n"+msg+"\n"
    if number==1164:
        h,w=1+(seed-1)%8,2+(seed-1)//8;return f"{h}\n{w}\n"+"\n".join(" ".join(["15"]*w) for _ in range(h))+"\n"
    if number==1166:return "\n".join(" ".join(str(r.randrange(4)) for _ in range(3)) for _ in range(3))+"\n"
    if number==1193:
        N=r.randint(5,100);rows=[];t=0
        for _ in range(r.randint(2,20)):t+=r.randint(0,4);rows.append(f"{t} {r.randint(1,N)} {r.randint(1,30)}")
        return f"{N}\n"+"\n".join(rows)+"\n0 0 0\n"
    if number==2002:
        pts=set()
        while len(pts)<r.randint(2,30):pts.add((r.randint(-30,30),r.randint(-30,30)))
        if seed%2:pts.update({(0,0),(0,seed),(seed,0),(seed,seed)})
        return f"{len(pts)}\n"+"\n".join(f"{x} {y}" for x,y in sorted(pts))+"\n0\n"
    if number==2000:return "\n".join(str(r.randint(1,10000)) for _ in range(r.randint(1,10)))+"\n0\n"
    if number==1324:
        L=2+(seed-1)%6;n,m=10,12;row=2+(seed-1)%5;col=2+(seed-1)//5;body=[(row,col+i) for i in range(L)];return f"{n} {m} {L}\n"+"\n".join(f"{a} {b}" for a,b in body)+"\n0\n\n0 0 0\n"
    if number==2318:
        n=r.randint(1,8);m=r.randint(1,15);xs=sorted(r.sample(range(5,95),n));toys=[(r.randint(1,99),r.randint(1,9)) for _ in range(m)];return f"{n} {m} 0 10 100 0\n"+"\n".join(f"{x} {x}" for x in xs)+"\n"+"\n".join(f"{x} {y}" for x,y in toys)+"\n0\n"
    if number==3129:
        cases=[f"{r.randint(1,10000)}\n"+" ".join(str(r.randint(1,10000)) for _ in range(5)) for _ in range(r.randint(1,4))];return f"{len(cases)}\n"+"\n".join(cases)+"\n"
    if number==1001:return "\n".join(f"{r.randint(1,999999)/10000:.4f} {r.randint(1,25)}" for _ in range(r.randint(1,6)))+"\n"
    if number==1004:return "\n".join(f"{r.randint(1,100000000)/100:.2f}" for _ in range(12))+"\n"
    if number==1005:
        rows=[]
        for _ in range(r.randint(1,8)):
            x,y=r.uniform(-100,100),r.uniform(0,100);rows.append(f"{x:.3f} {y:.3f}")
        return f"{len(rows)}\n"+"\n".join(rows)+"\n"
    if number==1021:
        cases=[]
        for _ in range(r.randint(1,3)):
            w=h=r.randint(4,12);n=r.randint(1,min(12,w*h));p=r.sample([(x,y) for x in range(w) for y in range(h)],n);q=p[:] if r.random()<.5 else r.sample([(x,y) for x in range(w) for y in range(h)],n);cases.append(f"{w} {h} {n}\n"+" ".join(f"{x} {y}" for x,y in p)+"\n"+" ".join(f"{x} {y}" for x,y in q))
        return f"{len(cases)}\n"+"\n".join(cases)+"\n"
    if number==2251:
        R,C=3+(seed-1)%7,3+(seed-1)//7;grid=[["."]*C for _ in range(R)];grid[0][0]="S";grid[-1][-1]="E";return f"1 {R} {C}\n"+"\n".join("".join(x) for x in grid)+"\n0 0 0\n"
    if number==2663:return "\n".join(str(r.randint(0,30)) for _ in range(r.randint(1,10)))+"\n-1\n"
    if number==2745:return "\n".join(f"{r.randint(1,10)} {r.randint(0,99999999)}" for _ in range(r.randint(1,5)))+"\n0 0\n"
    if number==2977:return " ".join(str(r.randint(0,365)) for _ in range(4))+"\n"
    if number==2352:
        pts=sorted({(r.randint(0,100),r.randint(0,100)) for _ in range(30)},key=lambda p:(p[1],p[0]));return f"{len(pts)}\n"+"\n".join(f"{x} {y}" for x,y in pts)+"\n"
    if number==2599:
        n=r.randint(2,40);edges=[(i,r.randint(1,i-1)) for i in range(2,n+1)];return f"{n} {r.randint(1,n)}\n"+"\n".join(f"{a} {b}" for a,b in edges)+"\n"
    if number==2937:
        n=r.randint(3,12);return f"{n}\n"+"\n".join(" ".join(str(r.randint(0,255)) for _ in range(n)) for _ in range(n))+"\n"
    if number==2943:
        n=r.randint(1,20);weights=r.sample(range(1,1001),n);return f"{n}\n"+"\n".join(f"{x} c{i}" for i,x in enumerate(weights))+"\n"
    if number==1007:
        n,m=r.randint(1,30),r.randint(1,30);return f"{n} {m}\n"+"\n".join("".join(r.choice("ACGT") for _ in range(n)) for _ in range(m))+"\n"
    if number==1836:
        n=r.randint(2,50);return f"{n}\n"+" ".join(f"{r.uniform(.5,2.5):.5f}" for _ in range(n))+"\n"
    raise KeyError(number)

NO_INPUT={3225, 2698}
REFERENCE='# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md\n# Heading: 2186: Popular Cows\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md\n# Upstream problem: http://cs101.openjudge.cn/practice/02186/\n# License: not declared; no license is inferred.\nimport sys\n\n# 增加递归深度\nsys.setrecursionlimit(100000)\n\ndef solve():\n    # 使用快读\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n\n    n = int(input_data[0])\n    m = int(input_data[1])\n\n    adj = [[] for _ in range(n + 1)]\n    edges = []\n    idx = 2\n    for _ in range(m):\n        u = int(input_data[idx])\n        v = int(input_data[idx+1])\n        adj[u].append(v)\n        edges.append((u, v))\n        idx += 2\n\n    # --- Tarjan 算法变量 ---\n    dfn = [0] * (n + 1)\n    low = [0] * (n + 1)\n    stack = []\n    in_stack = [False] * (n + 1)\n    timer = 0\n\n    scc_id = [0] * (n + 1)\n    scc_size = {} # 记录每个 SCC 包含的节点数\n    scc_count = 0\n\n    def tarjan(u):\n        nonlocal timer, scc_count\n        timer += 1\n        dfn[u] = low[u] = timer\n        stack.append(u)\n        in_stack[u] = True\n\n        for v in adj[u]:\n            if not dfn[v]:\n                tarjan(v)\n                low[u] = min(low[u], low[v])\n            elif in_stack[v]:\n                low[u] = min(low[u], dfn[v])\n\n        if dfn[u] == low[u]:\n            scc_count += 1\n            count = 0\n            while True:\n                node = stack.pop()\n                in_stack[node] = False\n                scc_id[node] = scc_count\n                count += 1\n                if node == u:\n                    break\n            scc_size[scc_count] = count\n\n    # 寻找 SCC\n    for i in range(1, n + 1):\n        if not dfn[i]:\n            tarjan(i)\n\n    # --- 统计缩点后各 SCC 的出度 ---\n    out_degree = [0] * (scc_count + 1)\n    for u, v in edges:\n        if scc_id[u] != scc_id[v]:\n            out_degree[scc_id[u]] += 1\n\n    # --- 分析结论 ---\n    zero_out_count = 0\n    target_scc = 0\n\n    for i in range(1, scc_count + 1):\n        if out_degree[i] == 0:\n            zero_out_count += 1\n            target_scc = i\n\n    if zero_out_count == 1:\n        # 只有一个出度为 0 的 SCC，该 SCC 里的牛就是答案\n        print(scc_size[target_scc])\n    else:\n        # 如果有多个出度为 0 的点，说明它们之间互不到达，没有牛能被所有人崇拜\n        print(0)\n\nif __name__ == "__main__":\n    solve()\n'
LANGUAGE='Python3'
NUMBER=2186
SAMPLE='3 3\n1 2\n2 1\n2 3\n'
def valid(text):
    """题面契约：第 1 行 N M（1 <= N <= 10000，1 <= M <= 50000），随后恰 M 行 A B，
    1 <= A, B <= N（单空格分隔）。题面未禁止自环与重边。"""
    if not text.endswith('\n') or '\r' in text:
        return False
    lines = text[:-1].split('\n')
    def nums(line):
        toks = line.split(' ')
        if len(toks) != 2 or not all(t.isdigit() and t[0] != '0' for t in toks):
            return None
        return int(toks[0]), int(toks[1])
    head = nums(lines[0])
    if head is None:
        return False
    n, m = head
    if not (1 <= n <= 10000 and 1 <= m <= 50000) or len(lines) != m + 1:
        return False
    for line in lines[1:]:
        e = nums(line)
        if e is None or not (1 <= e[0] <= n and 1 <= e[1] <= n):
            return False
    return True


def _fmt2186(n, edges, r, shuffle=True):
    edges = list(edges)
    if shuffle:
        r.shuffle(edges)
    return f"{n} {len(edges)}\n" + "".join(f"{a} {b}\n" for a, b in edges)


def _relabel2186(r, n, edges):
    p = list(range(1, n + 1)); r.shuffle(p)
    return [(p[a - 1], p[b - 1]) for a, b in edges]


def _sccdag2186(r, n, k, total, sinks=1):
    """把 1..n 分成 k 个强连通块（每块内一个环），块按拓扑序编号，最后 sinks 块是汇点块（不向外连边）。
    每个非汇点块至少连向后面某一块，故都能走到汇点；sinks=1 时答案为汇点块大小，否则为 0。
    总边数补到 total（只加块内边或「非汇点块 -> 更后面块」的边，不破坏结构）。"""
    cuts = sorted(r.sample(range(1, n), k - 1)) if k > 1 else []
    bounds = [0] + cuts + [n]
    blocks = [list(range(bounds[i] + 1, bounds[i + 1] + 1)) for i in range(k)]
    edges = []
    for b in blocks:
        if len(b) > 1:
            edges += [(b[i], b[(i + 1) % len(b)]) for i in range(len(b))]
    body = k - sinks
    for i in range(body):
        j = r.randrange(i + 1, k)
        edges.append((r.choice(blocks[i]), r.choice(blocks[j])))
    while len(edges) < total:
        i = r.randrange(k)
        j = i if i >= body else r.randrange(i, k)
        edges.append((r.choice(blocks[i]), r.choice(blocks[j])))
    return edges


def gen2186(seed):
    r = random.Random(2186_000 + seed)
    N, M = 10000, 50000
    if seed == 1:  return "1 1\n1 1\n"                                   # N=1：唯一一头牛，答案 1
    if seed == 2:  return "2 1\n1 2\n"                                   # 答案 1
    if seed == 3:  return "2 2\n1 2\n2 1\n"                              # 答案 2
    if seed == 4:  return "3 2\n1 2\n3 2\n"                              # 汇点 2：答案 1
    if seed == 5:  return "3 2\n2 1\n2 3\n"                              # 两个汇点：答案 0
    if seed == 6:  return "4 3\n1 2\n2 1\n3 4\n"                         # 两个不连通块：0
    if seed == 7:  return "3 1\n1 1\n"                                   # 只有自环，还有孤立牛：0
    if seed == 8:  return "5 4\n1 2\n2 3\n3 4\n4 5\n"                    # 链：1
    if seed == 9:                                                        # 满规模长链（深递归）：答案 1
        e = [(i, i + 1) for i in range(1, N)]
        e += [(r.randint(1, N - 1), 0) for _ in range(M - len(e))]
        e = [(a, b if b else r.randint(a + 1, N)) for a, b in e]
        return _fmt2186(N, _relabel2186(r, N, e), r)
    if seed == 10:                                                       # 满规模大环 + 一头只被指向的牛：答案 1
        e = [(i, i % (N - 1) + 1) for i in range(1, N)] + [(r.randint(1, N - 1), N) for _ in range(M - (N - 1))]
        return _fmt2186(N, _relabel2186(r, N, e), r)
    if seed == 11:                                                       # 满规模单个大环：答案 N
        e = [(i, i % N + 1) for i in range(1, N + 1)] + [(r.randint(1, N), r.randint(1, N)) for _ in range(M - N)]
        return _fmt2186(N, e, r)
    if seed == 12:                                                       # 满规模，最后一头牛孤立（出入度 0）：答案 0
        e = [(i, i % (N - 1) + 1) for i in range(1, N)] + [(r.randint(1, N - 1), r.randint(1, N - 1)) for _ in range(M - (N - 1))]
        return _fmt2186(N, _relabel2186(r, N, e), r)
    if seed == 13:                                                       # 星形：所有牛都指向 1 头牛
        e = [(i, 1) for i in range(2, N + 1)]
        return _fmt2186(N, _relabel2186(r, N, e), r)
    if seed == 14:                                                       # 星形反过来：一头牛指向所有牛，N-1 个汇点：0
        e = [(1, i) for i in range(2, N + 1)]
        return _fmt2186(N, _relabel2186(r, N, e), r)
    if seed == 15:                                                       # 重边 + 自环
        e = [(1, 2)] * 5 + [(2, 2)] * 3 + [(3, 1)] * 2 + [(2, 3)]
        return _fmt2186(3, e, r)
    if seed <= 22:                                                       # 满规模 SCC 拓扑结构，单汇点块（答案为汇点块大小）
        k = [2, 5, 50, 500, 3000, 9000, 10000][seed - 16]
        e = _sccdag2186(r, N, k, M)
        return _fmt2186(N, _relabel2186(r, N, e), r)
    if seed <= 27:                                                       # 满规模多汇点块：答案 0
        k = [3, 20, 400, 5000, 10000][seed - 23]; sinks = [2, 3, 2, 2, 100][seed - 23]
        e = _sccdag2186(r, N, k, M, sinks=sinks)
        return _fmt2186(N, _relabel2186(r, N, e), r)
    if seed <= 34:                                                       # 中小规模随机图
        n = r.randint(2, 60); m = r.randint(1, min(M, n * 3))
        e = [(r.randint(1, n), r.randint(1, n)) for _ in range(m)]
        return _fmt2186(n, e, r)
    # 中规模 SCC 结构，答案非零
    n = r.randint(100, 3000); k = r.randint(2, 40)
    e = _sccdag2186(r, n, k, r.randint(0, 3 * n))
    return _fmt2186(n, _relabel2186(r, n, e[:M]), r)

def main():
 with tempfile.TemporaryDirectory() as d:
  d=Path(d);src=d/('s.py' if LANGUAGE=='Python3' else 's.cpp');src.write_text(REFERENCE);cmd=[sys.executable,'-I',str(src)]
  if LANGUAGE!='Python3':
   exe=d/'s';subprocess.run(['g++','-std=c++20','-O2','-pipe',str(src),'-o',str(exe)],check=True);cmd=[str(exe)]
  out=Path('data');out.mkdir(exist_ok=True)
  for p in out.glob('*'):p.unlink()
  cases=([SAMPLE] if SAMPLE or NUMBER in (2698,3225) else [])+([] if NUMBER in (2698,3225) else [gen2186(s) for s in range(1, 40)])
  for i,x in enumerate(cases):
   q=subprocess.run(cmd,input=x,text=True,capture_output=True,timeout=120,check=True);(out/f'{i}.in').write_text(x);(out/f'{i}.out').write_text(q.stdout.rstrip()+'\n')
if __name__=='__main__':main()

import random,subprocess,sys,tempfile
from pathlib import Path
def generate(n, seed):
    r=random.Random(seed)
    if n==2694:
        return f"+ * {r.randint(-20,20)} {r.randint(-20,20)} / {r.randint(-20,20)} {r.randint(1,20)}\n"
    if n==2945:
        k=r.randint(3,25);return f"{k}\n"+' '.join(str(r.randint(1,500)) for _ in range(k))+'\n'
    if n==2746:
        return '\n'.join(f"{r.randint(1,80)} {r.randint(1,80)}" for _ in range(r.randint(1,5)))+'\n0 0\n'
    if n==2773:
        T=r.randint(20,300);m=r.randint(2,20);return f"{T} {m}\n"+'\n'.join(f"{r.randint(1,100)} {r.randint(1,100)}" for _ in range(m))+'\n'
    if n==2734:return f"{r.randint(1,65535)}\n"
    if n==2488:
        z=[(r.randint(1,6),r.randint(1,6)) for _ in range(r.randint(1,4))];return str(len(z))+'\n'+'\n'.join(f'{a} {b}' for a,b in z)+'\n'
    if n==2810:return f"{r.randint(2,45)}\n"
    if n==2299:
        a=[r.randint(0,10**9) for _ in range(r.randint(2,40))];return f"{len(a)}\n"+'\n'.join(map(str,a))+'\n0\n'
    if n==2775:return f"file{seed}\ndir{seed}\nfileA\n]\nfileZ\n*\n#\n"
    if n==2815:
        rows,cols=r.randint(2,7),r.randint(2,7);g=[[0]*cols for _ in range(rows)]
        for i in range(rows):
            for j in range(cols):
                if j==0:g[i][j]|=1
                if i==0:g[i][j]|=2
                if j==cols-1:g[i][j]|=4
                if i==rows-1:g[i][j]|=8
                if j+1<cols and r.random()<.35:g[i][j]|=4;g[i][j+1]|=1
                if i+1<rows and r.random()<.35:g[i][j]|=8;g[i+1][j]|=2
        return f"{rows}\n{cols}\n"+'\n'.join(' '.join(map(str,x)) for x in g)+'\n'
    if n==2524:
        out=[]
        for _ in range(r.randint(1,3)):
            a=r.randint(2,30);edges={(r.randint(1,a),r.randint(1,a)) for _ in range(r.randint(0,a))};edges={(x,y) for x,y in edges if x!=y};out.append(f'{a} {len(edges)}');out += [f'{x} {y}' for x,y in edges]
        return '\n'.join(out)+'\n0 0\n'
    if n==1088:
        a,b=r.randint(2,12),r.randint(2,12);return f'{a} {b}\n'+'\n'.join(' '.join(str(r.randint(0,500)) for _ in range(b)) for _ in range(a))+'\n'
    if n==1182:
        N=r.randint(3,50);k=r.randint(2,70);return f'{N} {k}\n'+'\n'.join(f'{r.randint(1,2)} {r.randint(1,N+3)} {r.randint(1,N+3)}' for _ in range(k))+'\n'
    if n==1760:
        paths=[]
        for i in range(r.randint(2,20)):paths.append('\\'.join(f'D{r.randint(1,8)}' for _ in range(r.randint(1,5))))
        return str(len(paths))+'\n'+'\n'.join(paths)+'\n'
    if n==2386:
        a,b=r.randint(2,15),r.randint(2,15);return f'{a} {b}\n'+'\n'.join(''.join(r.choice('W..') for _ in range(b)) for _ in range(a))+'\n'
    if n==2456:
        N=r.randint(3,30);C=r.randint(2,N);x=sorted(r.sample(range(1,10000),N));return f'{N} {C}\n'+'\n'.join(map(str,x))+'\n'
    if n==2808:
        L=r.randint(10,1000);m=r.randint(1,15);return f'{L} {m}\n'+'\n'.join(f'{(a:=r.randint(0,L))} {r.randint(a,L)}' for _ in range(m))+'\n'
    if n==2995:
        N=r.randint(2,80);return f'{N}\n'+' '.join(str(r.randint(1,1000)) for _ in range(N))+'\n'
    if n==2760:
        N=r.randint(2,20);return f'{N}\n'+'\n'.join(' '.join(str(r.randint(0,100)) for _ in range(i)) for i in range(1,N+1))+'\n'
    if n==3151:
        A,B=r.randint(2,30),r.randint(2,30);C=r.randint(1,max(A,B));return f'{A} {B} {C}\n'
    if n==2733:return f'{r.randint(1,2999)}\n'
    if n==2774:
        N=r.randint(2,30);K=r.randint(1,100);return f'{N} {K}\n'+'\n'.join(str(r.randint(1,10000)) for _ in range(N))+'\n'
    if n==2806:
        return '\n'.join(f"{''.join(r.choice('abcd') for _ in range(r.randint(1,20)))} {''.join(r.choice('abcd') for _ in range(r.randint(1,20)))}" for _ in range(r.randint(1,6)))+'\n'
    if n==1426:return '\n'.join(str(r.randint(1,200)) for _ in range(r.randint(1,6)))+'\n0\n'
    if n==1852:
        out=[str(r.randint(1,4))]
        for _ in range(int(out[0])):
            L=r.randint(10,1000);x=sorted(r.sample(range(1,L),r.randint(1,min(20,L-1))));out += [f'{L} {len(x)}',' '.join(map(str,x))]
        return '\n'.join(out)+'\n'
    if n==2039:
        c=r.randint(2,20);s=''.join(r.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(c*r.randint(1,10)));return f'{c}\n{s}\n'
    if n==2754:
        q=[r.randint(1,92) for _ in range(r.randint(1,8))];return str(len(q))+'\n'+'\n'.join(map(str,q))+'\n'
    if n==2783:
        N=r.randint(2,30);return f'{N}\n'+'\n'.join(f'{r.randint(1,10000)} {r.randint(1,10000)}' for _ in range(N))+'\n0\n'
    if n==1094:
        N=r.randint(3,10);rels=[]
        for _ in range(r.randint(1,20)):
            a,b=r.sample(range(N),2);rels.append(f'{chr(65+a)}<{chr(65+b)}')
        return f'{N} {len(rels)}\n'+'\n'.join(rels)+'\n0 0\n'
    if n==1376:
        a,b=r.randint(5,12),r.randint(5,12);g=[[0]*b for _ in range(a)];sx,sy=1,1;tx,ty=a-2,b-2
        return f'{a} {b}\n'+'\n'.join(' '.join(map(str,x)) for x in g)+f'\n{sx} {sy} {tx} {ty} east\n0 0\n'
    if n==1833:
        out=[str(r.randint(1,4))]
        for _ in range(int(out[0])):
            N=r.randint(2,30);p=list(range(1,N+1));r.shuffle(p);out += [f'{N} {r.randint(1,min(20,N))}',' '.join(map(str,p))]
        return '\n'.join(out)+'\n'
    if n==1961:
        out=[]
        for _ in range(r.randint(1,4)):
            s=''.join(r.choice('abc') for _ in range(r.randint(2,100)));out += [str(len(s)),s]
        return '\n'.join(out)+'\n0\n'
    if n==2255:
        def traversals(vals):
            if not vals:return '',''
            k=r.randrange(len(vals));a,b=traversals(vals[:k]);c,d=traversals(vals[k+1:]);return vals[k]+a+c,a+vals[k]+d
        rows=[]
        for _ in range(r.randint(1,4)):
            s=''.join(r.sample('ABCDEFGHIJKLMNOPQRSTUVWXYZ',r.randint(1,12)));rows.append(' '.join(traversals(s)))
        return '\n'.join(rows)+'\n'
    if n==2811:return '\n'.join(' '.join(str(r.randint(0,1)) for _ in range(6)) for _ in range(5))+'\n'
    if n==3248:return '\n'.join(f'{r.randint(1,2**31-1)} {r.randint(1,2**31-1)}' for _ in range(r.randint(1,8)))+'\n'
    if n==2692:
        coins=list('ABCDEFGHIJKL');coin=r.choice(coins);heavy=r.choice([True,False]);normal=[x for x in coins if x!=coin];r.shuffle(normal);x=normal[0]
        state='down' if heavy else 'up'
        a,b,c,d=map(''.join,(normal[:4],normal[4:8],normal[3:7],normal[7:11]))
        return f'1\n{coin} {x} {state}\n{a} {b} even\n{c} {d} even\n'
    if n==3143:return f'{r.randint(4,2000)}\n'
    if n==1860:
        N=r.randint(2,8);edges=[]
        for _ in range(r.randint(N-1,20)):
            a,b=r.sample(range(1,N+1),2);edges.append(f'{a} {b} {r.uniform(.5,1.6):.2f} {r.uniform(0,2):.2f} {r.uniform(.5,1.6):.2f} {r.uniform(0,2):.2f}')
        return f'{N} {len(edges)} 1 {r.uniform(10,100):.2f}\n'+'\n'.join(edges)+'\n'
    if n==1035:
        words=['cat','dog','apple','word'+chr(97+seed%26)];queries=[words[-1],words[-1][:-1]+'z','dogs'];return '\n'.join(words+['#']+queries+['#'])+'\n'
    if n==2431:
        N=r.randint(1,20);L=r.randint(20,500);stops=sorted({r.randint(1,L-1):r.randint(1,100) for _ in range(N)}.items(),reverse=True);return str(len(stops))+'\n'+'\n'.join(f'{d} {f}' for d,f in stops)+f'\n{L} {r.randint(1,100)}\n'
    if n==2756:return f'{r.randint(1,1000)} {r.randint(1,1000)}\n'
    if n==2757:
        N=r.randint(1,80);return f'{N}\n'+' '.join(str(r.randint(0,10000)) for _ in range(N))+'\n'
    if n==1159:
        N=r.randint(3,100);s=''.join(r.choice('abcXYZ09') for _ in range(N));return f'{N}\n{s}\n'
    if n==1724:
        N=r.randint(2,12);K=r.randint(0,50);edges=[]
        for i in range(1,N):edges.append((i,i+1,r.randint(1,30),r.randint(0,10)))
        for _ in range(r.randint(0,20)):
            a,b=r.sample(range(1,N+1),2);edges.append((a,b,r.randint(1,50),r.randint(0,15)))
        return f'{K}\n{N}\n{len(edges)}\n'+'\n'.join(' '.join(map(str,e)) for e in edges)+'\n'
    if n==2706:return f"{1000+seed}\n"
    if n==2996:
        N=r.randint(2,80);p=list(range(1,N+1));r.shuffle(p);return f'{N}\n{r.randint(1,min(30,N))}\n'+' '.join(map(str,p))+'\n'
    if n==3254:return '\n'.join(f'{r.randint(2,100)} {r.randint(1,100)} {r.randint(1,100)}' for _ in range(r.randint(1,5)))+'\n0 0 0\n'
    if n==2502:
        hx,hy,sx,sy=[r.randint(0,10000) for _ in range(4)];return f'{hx} {hy} {sx} {sy}\n{r.randint(0,10000)} {r.randint(0,10000)} {r.randint(0,10000)} {r.randint(0,10000)} -1 -1\n'
    if n==2748:return ''.join(r.sample('abcdefghi',r.randint(1,5)))+'\n'
    if n==1191:return f'{r.randint(2,10)}\n'+'\n'.join(' '.join(str(r.randint(0,99)) for _ in range(8)) for _ in range(8))+'\n'
    if n==2287:
        N=r.randint(1,30);return f'{N}\n'+' '.join(str(r.randint(1,100)) for _ in range(N))+'\n'+' '.join(str(r.randint(1,100)) for _ in range(N))+'\n0\n'
    if n==2981:return str(r.randrange(10**50))+'\n'+str(r.randrange(10**50))+'\n'
    if n==2750:return f'{r.randint(1,32767)}\n'
    if n==2788:
        rows=[]
        for _ in range(r.randint(1,6)):
            m=r.randint(1,100000);rows.append(f'{m} {r.randint(m,1000000000)}')
        return '\n'.join(rows)+'\n0 0\n'
    if n==2802:
        w,h=r.randint(2,8),r.randint(2,8);board=[' '*w for _ in range(h)];y2=1 if seed%2==0 else h
        return f'{w} {h}\n'+'\n'.join(board)+f'\n1 1 {w} {y2}\n0 0 0 0\n0 0\n'
    if n==1003:return '\n'.join(f'{r.uniform(.01,5.20):.2f}' for _ in range(r.randint(1,6)))+'\n0.00\n'
    if n==1011:
        a=[r.randint(1,30) for _ in range(r.randint(3,20))];return f'{len(a)}\n'+' '.join(map(str,a))+'\n0\n'
    if n==1017:return ' '.join(str(r.randint(0,20)) for _ in range(6))+'\n0 0 0 0 0 0\n'
    if n==1065:
        out=[str(r.randint(1,3))]
        for _ in range(int(out[0])):
            N=r.randint(1,30);out += [str(N),' '.join(f'{r.randint(1,30)} {r.randint(1,30)}' for _ in range(N))]
        return '\n'.join(out)+'\n'
    if n==1218:
        q=[r.randint(5,100) for _ in range(r.randint(1,10))];return str(len(q))+'\n'+'\n'.join(map(str,q))+'\n'
    raise KeyError(n)

REFERENCE="# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md\n# Heading: 2502: Subway\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md\n# Upstream problem: http://cs101.openjudge.cn/2024sp_routine/02502/\n# License: not declared in source collection; no license is inferred.\nimport sys\nimport math\nimport heapq\n\n# 计算两点之间的欧几里得距离\ndef get_distance(x1, y1, x2, y2):\n    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)\n\n# 读取起点（家）和终点（学校）坐标\nsx, sy, ex, ey = map(int, input().split())\n\n# min_time: 记录从起点到每个地铁站/终点的最短时间（单位：小时）\nmin_time = {}\n\n# rails: 记录所有地铁连接（双向）\nrails = set()\n\n# 读取所有地铁线路\nwhile True:\n    try:\n        rail = list(map(int, input().split()))\n        if rail == [-1, -1]:\n            break\n        # 解析当前地铁线路的所有站点\n        stations = [(rail[2 * i], rail[2 * i + 1]) for i in range(len(rail) // 2 - 1)]\n\n        for j, station in enumerate(stations):\n            # 初始化所有地铁站点的最短时间为无穷大\n            min_time[station] = float('inf')\n            # 添加地铁线路中相邻站点的双向连接\n            if j != len(stations) - 1:\n                rails.add((station, stations[j + 1]))\n                rails.add((stations[j + 1], station))\n    except EOFError:\n        break  # 输入结束\n\n# 把起点和终点加入时间表中\nmin_time[(sx, sy)] = 0  # 起点时间为 0\nmin_time[(ex, ey)] = float('inf')  # 终点初始化为无穷大\n\n# 使用小根堆实现 Dijkstra 算法，按时间升序处理节点\nmin_heap = [(0, sx, sy)]  # (当前耗时, 当前x, 当前y)\n\nwhile min_heap:\n    curr_time, x, y = heapq.heappop(min_heap)\n\n    # 如果当前耗时不是最短路径中记录的值，说明已经被更新，跳过\n    if curr_time > min_time[(x, y)]:\n        continue\n\n    # 如果已经到达终点，提前结束\n    if (x, y) == (ex, ey):\n        break\n\n    # 遍历所有可达点（隐式图）\n    for position in min_time.keys():\n        if position == (x, y):\n            continue  # 自己跳过\n        nx, ny = position\n\n        # 计算当前位置到下一个点的距离\n        dis = get_distance(x, y, nx, ny)\n\n        # 判断是否为地铁连接：地铁速度是步行的4倍\n        rail_factor = 4 if ((position, (x, y)) in rails or ((x, y), position) in rails) else 1\n\n        # 计算到该点的所需时间（单位：小时）\n        new_time = curr_time + dis / (10000 * rail_factor)\n\n        # 如果时间更短，则更新并加入堆中\n        if new_time < min_time[position]:\n            min_time[position] = new_time\n            heapq.heappush(min_heap, (new_time, nx, ny))\n\n# 输出从起点到终点的最短时间，转换为分钟并四舍五入\nprint(round(min_time[(ex, ey)] * 60))\n"
import math, re

def valid(text):
    """题面：首先是家、学校的 x y 坐标（整数）；随后若干条地铁线，每条线是若干个非负整数坐标 x y（至少两站），
    以哑坐标 -1 -1 结束；全城地铁站总数至多 200。"""
    toks = text.split()
    if not all(re.fullmatch(r"-?[0-9]+", t) for t in toks):
        return False
    v = [int(t) for t in toks]
    if len(v) < 4 or len(v) % 2:
        return False
    total = 0
    cur = 0
    for k in range(4, len(v), 2):
        x, y = v[k], v[k + 1]
        if (x, y) == (-1, -1):
            if cur < 2:
                return False
            cur = 0
        elif x >= 0 and y >= 0:
            cur += 1
            total += 1
        else:
            return False
    if cur != 0:  # 最后一条线没有以 -1 -1 结束
        return False
    return total <= 200


def solve2502(text):
    """独立的 O(V^2) Dijkstra，返回精确分钟数（未取整）。"""
    v = list(map(int, text.split()))
    home, school = (v[0], v[1]), (v[2], v[3])
    pts = [home, school]
    idx = {home: 0}
    idx.setdefault(school, 1)
    adj = set()
    line = []
    def node(p):
        if p not in idx:
            idx[p] = len(pts); pts.append(p)
        return idx[p]
    for k in range(4, len(v), 2):
        p = (v[k], v[k + 1])
        if p == (-1, -1):
            for a, b in zip(line, line[1:]):
                adj.add((a, b)); adj.add((b, a))
            line = []
        else:
            line.append(node(p))
    n = len(pts)
    INF = float("inf")
    dist = [INF] * n
    dist[0] = 0.0
    done = [False] * n
    for _ in range(n):
        u = min((i for i in range(n) if not done[i]), key=lambda i: dist[i])
        done[u] = True
        for w in range(n):
            if not done[w]:
                d = math.hypot(pts[u][0] - pts[w][0], pts[u][1] - pts[w][1])
                speed = 40000.0 if (u, w) in adj else 10000.0
                nd = dist[u] + d / speed * 60
                if nd < dist[w]:
                    dist[w] = nd
    return dist[idx[school]]


def make_lines(r, lines):
    return "".join(" ".join(f"{x} {y}" for x, y in ln) + " -1 -1\n" for ln in lines)


def g2502(r, kind, W):
    """kind: small/random/commute/zigzag/transfer/max1/maxmany"""
    def pt():
        return (r.randint(0, W), r.randint(0, W))
    def walk(start, k, step):
        out = [start]; seen = {start}
        while len(out) < k:
            x, y = out[-1]
            q = (min(W, max(0, x + r.randint(-step, step))), min(W, max(0, y + r.randint(-step, step))))
            if q not in seen:
                out.append(q); seen.add(q)
        return out
    while True:
        home, school = pt(), pt()
        if home == school:
            continue
        lines = []
        if kind == "small":
            a = pt(); b = pt()
            if a == b:
                continue
            lines = [[a, b]]
        elif kind == "random":
            budget = r.randint(10, 120)
            while budget >= 2:
                k = r.randint(2, min(budget, 25)); budget -= k
                lines.append(walk(pt(), k, max(1, W // 8)))
        elif kind == "commute":
            # 一条从家附近到学校附近的线，站与站之间有轻微抖动，外加若干干扰线
            k = r.randint(5, 40)
            ln = []
            for i in range(k):
                t = i / (k - 1)
                x = home[0] + (school[0] - home[0]) * t + r.randint(-W // 50 - 1, W // 50 + 1)
                y = home[1] + (school[1] - home[1]) * t + r.randint(-W // 50 - 1, W // 50 + 1)
                q = (min(W, max(0, int(x))), min(W, max(0, int(y))))
                if not ln or ln[-1] != q:
                    ln.append(q)
            if len(ln) < 2:
                continue
            lines.append(ln)
            for _ in range(r.randint(0, 5)):
                lines.append(walk(pt(), r.randint(2, 15), max(1, W // 6)))
        elif kind == "zigzag":
            # 站点来回折返：只能沿相邻站乘车，直接把同线不相邻站连成地铁边的写法会错
            k = r.randint(6, 60)
            ln = []
            for i in range(k):
                t = i / (k - 1)
                x = home[0] + (school[0] - home[0]) * t
                y = home[1] + (school[1] - home[1]) * t
                off = (W // 3) * (1 if i % 2 else -1)
                dx, dy = school[1] - home[1], home[0] - school[0]
                L = math.hypot(dx, dy) or 1
                q = (min(W, max(0, int(x + off * dx / L))), min(W, max(0, int(y + off * dy / L))))
                if not ln or ln[-1] != q:
                    ln.append(q)
            if len(ln) < 2 or len(set(ln)) != len(ln):
                continue
            lines.append(ln)
        elif kind == "transfer":
            # 两条线在共享站点处换乘
            mid = pt()
            a = walk(home, r.randint(2, 20), max(1, W // 10))
            b = walk(mid, r.randint(2, 20), max(1, W // 10))
            a.append(mid) if mid not in a else None
            b2 = [mid] + [q for q in walk(school, r.randint(2, 20), max(1, W // 10)) if q != mid]
            lines = [a, b2] if len(b2) >= 2 else [a, b]
            for _ in range(r.randint(0, 4)):
                lines.append(walk(pt(), r.randint(2, 10), max(1, W // 6)))
        elif kind == "max1":
            lines = [walk(pt(), 200, max(1, W // 10))]
        elif kind == "maxmany":
            budget = 200
            while budget >= 2:
                k = min(budget, r.randint(2, 30))
                if budget - k == 1:
                    k += 1
                budget -= k
                lines.append(walk(pt(), k, max(1, W // 8)))
        r.shuffle(lines)
        text = f"{home[0]} {home[1]} {school[0]} {school[1]}\n" + make_lines(r, lines)
        ans = solve2502(text)
        # 避开 x.5 分钟附近的取整歧义
        if abs(ans - math.floor(ans) - 0.5) < 1e-4:
            continue
        return text


PLAN2502 = (["small"] * 4 + ["random"] * 8 + ["commute"] * 8 + ["zigzag"] * 5 + ["transfer"] * 6
            + ["max1"] * 4 + ["maxmany"] * 4)

NUMBER=2502
SAMPLE='0 0 10000 1000\n0 200 5000 200 7000 200 -1 -1\n2000 600 5000 600 10000 600 -1 -1\n'
def run(x):
 with tempfile.TemporaryDirectory() as d:
  p=Path(d)/'m.py';p.write_text(REFERENCE);q=subprocess.run([sys.executable,'-I',str(p)],input=x,text=True,capture_output=True,timeout=120)
  if q.returncode:raise SystemExit(q.stderr)
  return q.stdout
def main():
 d=Path('data');d.mkdir(exist_ok=True)
 for p in d.glob('*'):p.unlink()
 cases=[SAMPLE]
 for s,kind in enumerate(PLAN2502, start=1):
  r=random.Random(2502000+s);W=r.choice([10000,10000,20000,100000]) if kind not in ('small',) else r.choice([100,10000])
  cases.append(g2502(r,kind,W))
 assert all(valid(x) for x in cases)
 for i,x in enumerate(cases):
  (d/f'{i}.in').write_text(x);(d/f'{i}.out').write_text(run(x))
if __name__=='__main__':main()

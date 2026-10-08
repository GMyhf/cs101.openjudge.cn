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
    if n==2788:return '\n'.join(f'{r.randint(1,100000)} {r.randint(1,1000000000)}' for _ in range(r.randint(1,6)))+'\n0 0\n'
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


_DIRS1376 = ("north", "west", "south", "east")


def _ok1376(g, i, j):
    """交点 (i,j)（方格 (i,j) 的西北角）可站：不在外墙上，周围四个方格都无障碍。"""
    M, N = len(g), len(g[0])
    return (1 <= i <= M - 1 and 1 <= j <= N - 1 and not g[i - 1][j - 1] and not g[i - 1][j]
            and not g[i][j - 1] and not g[i][j])


def valid(text):
    """题面契约：多块，每块 M N（M,N<=50；起终点要是方格的西北角且为正整数，故 M,N>=2），
    M 行各 N 个 0/1，然后 B1 B2 E1 E2 与朝向（north/west/south/east），四个坐标为正整数且是存在的方格；
    以 0 0 结束。另按物理意义要求起点交点机器人放得下（四周无障碍）。"""
    t = text.split()
    i, blocks = 0, 0
    try:
        while True:
            if i + 2 > len(t):
                return False
            M, N = int(t[i]), int(t[i + 1]); i += 2
            if M == 0 and N == 0:
                return i == len(t) and blocks >= 1
            if not (2 <= M <= 50 and 2 <= N <= 50) or i + M * N + 5 > len(t):
                return False
            cells = t[i:i + M * N]; i += M * N
            if any(c not in ("0", "1") for c in cells):
                return False
            g = [[int(c) for c in cells[k * N:(k + 1) * N]] for k in range(M)]
            b1, b2, e1, e2 = map(int, t[i:i + 4]); d = t[i + 4]; i += 5
            if d not in _DIRS1376:
                return False
            if not (1 <= b1 <= M - 1 and 1 <= e1 <= M - 1 and 1 <= b2 <= N - 1 and 1 <= e2 <= N - 1):
                return False
            if not _ok1376(g, b1, b2):
                return False
            blocks += 1
    except ValueError:
        return False


def _blk1376(g, s, e, d):
    return (f"{len(g)} {len(g[0])}\n" + "".join(" ".join(map(str, row)) + "\n" for row in g) +
            f"{s[0]} {s[1]} {e[0]} {e[1]} {d}\n")


def _rand1376(r, M, N, dens, need_valid_end=True):
    for _ in range(1000):
        g = [[1 if r.random() < dens else 0 for _ in range(N)] for _ in range(M)]
        pts = [(i, j) for i in range(1, M) for j in range(1, N) if _ok1376(g, i, j)]
        if len(pts) < 1:
            continue
        s = r.choice(pts)
        e = r.choice(pts) if need_valid_end or r.random() < .5 else (r.randint(1, M - 1), r.randint(1, N - 1))
        return _blk1376(g, s, e, r.choice(_DIRS1376))
    g = [[0] * N for _ in range(M)]
    return _blk1376(g, (1, 1), (M - 1, N - 1), r.choice(_DIRS1376))


def g1376_v2(seed):
    r = random.Random(1376 * 1_000_003 + seed)
    bl = []
    if seed == 1:     # 边界：最小 2x2（唯一交点，起点即终点 0）；掉头需两次转向；GO 3 一步到位；被墙隔开 -1
        bl.append(_blk1376([[0, 0], [0, 0]], (1, 1), (1, 1), "north"))
        z = [[0] * 5 for _ in range(2)]
        bl.append(_blk1376(z, (1, 4), (1, 1), "east"))       # 掉头 2 + GO 3 = 3
        bl.append(_blk1376(z, (1, 1), (1, 4), "east"))       # 1
        bl.append(_blk1376([[0] * 6 for _ in range(2)], (1, 1), (1, 5), "north"))   # 转 1 + GO3 + GO1 = 3
        w = [[0] * 7 for _ in range(7)]
        for i in range(7): w[i][3] = 1                         # 竖墙把左右隔开
        bl.append(_blk1376(w, (2, 1), (2, 6), "east"))
        w2 = [[0] * 7 for _ in range(4)]; w2[0][3] = 1         # 只挡最北一行：交点 (1,3)/(1,4) 不可站，必须绕到第 2、3 行
        bl.append(_blk1376(w2, (1, 1), (1, 6), "east"))
        bl.append(_blk1376([[0] * 4 for _ in range(4)], (1, 1), (3, 3), "west"))
        bl.append(_blk1376([[1 if (i, j) == (2, 2) else 0 for j in range(5)] for i in range(5)], (1, 1), (2, 2), "south"))  # 终点贴障碍 -1
    elif seed <= 20:  # 随机中小规模多组
        for _ in range(r.randint(2, 8)):
            bl.append(_rand1376(r, r.randint(2, 25), r.randint(2, 25), r.choice([0, .05, .1, .2, .3]), r.random() < .8))
    elif seed <= 32:  # 50x50 满规模
        for _ in range(r.randint(1, 4)):
            bl.append(_rand1376(r, 50, 50, r.choice([0, .03, .06, .1, .15]), r.random() < .9))
    elif seed <= 35:  # 蛇形走廊：路很长、转向很多
        M = N = 50
        g = [[0] * N for _ in range(M)]
        for k, row in enumerate(range(3, M - 2, 4)):
            for j in range(N):
                g[row][j] = 1
            gap = (N - 3) if k % 2 == 0 else 1
            g[row][gap] = g[row][gap + 1] = 0
            g[row][gap - 1] = 0
            g[row][gap + 2 if gap + 2 < N else gap - 2] = 0
        s, e = (1, 1), (M - 1, 1 if seed % 2 else N - 1)
        if not _ok1376(g, *e): e = next((i, j) for i in range(M - 1, 0, -1) for j in range(1, N) if _ok1376(g, i, j))
        bl.append(_blk1376(g, s, e, _DIRS1376[seed % 4]))
    else:             # 多组 50x50（卡每组重新分配的低效写法）
        for _ in range(20):
            bl.append(_rand1376(r, 50, 50, r.choice([.02, .08, .12]), True))
    return "".join(bl) + "0 0\n"

REFERENCE="# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md\n# Heading: 1376: Robot\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md\n# Upstream problem: http://cs101.openjudge.cn/2024sp_routine/01376/\n# License: not declared in source collection; no license is inferred.\nimport sys\nfrom collections import deque\n\n\ndef bfs_min_time(grid, start, end, direction):\n    N, M = len(grid), len(grid[0])\n    # 定义朝向：0-东, 1-南, 2-西, 3-北\n    dir_map = {'E': 0, 'S': 1, 'W': 2, 'N': 3}\n    start_dir = dir_map[direction]\n    sr, sc, tr, tc = start[0], start[1], end[0], end[1]\n\n    # 机器人中心只能位于网格交点，合法交点要求其周围四个相邻的格子都不能有障碍。\n    # 对于交点 (i, j) (i,j均从1开始计数，i∈[1,N-1], j∈[1,M-1])，对应的格子为\n    # (i-1,j-1), (i-1,j), (i,j-1), (i,j)\n    valid = [[False] * (M) for _ in range(N)]\n    for i in range(1, N):\n        for j in range(1, M):\n            if grid[i - 1][j - 1] == 0 and grid[i - 1][j] == 0 and grid[i][j - 1] == 0 and grid[i][j] == 0:\n                valid[i][j] = True\n\n    # 检查起始点和目标点是否合法\n    if not valid[sr][sc] or not valid[tr][tc]:\n        return -1\n\n    # 定义方向移动，顺序：东, 南, 西, 北\n    dr = [0, 1, 0, -1]\n    dc = [1, 0, -1, 0]\n\n    # BFS: 状态 (r, c, d)\n    visited = [[[False] * 4 for _ in range(M)] for _ in range(N)]\n    q = deque()\n    q.append((sr, sc, start_dir, 0))\n    visited[sr][sc][start_dir] = True\n\n    while q:\n        r, c, d, steps = q.popleft()\n        # 判断是否到达目标位置（朝向不要求匹配）\n        if r == tr and c == tc:\n            return steps\n\n        # 转向操作\n        # Left: d_new = (d+3)%4, Right: d_new = (d+1)%4\n        for nd in [(d + 3) % 4, (d + 1) % 4]:\n            if not visited[r][c][nd]:\n                visited[r][c][nd] = True\n                q.append((r, c, nd, steps + 1))\n\n        # 前进1,2,3步，每一步中间都必须合法\n        for k in range(1, 4):\n            nr = r + dr[d] * k\n            nc = c + dc[d] * k\n            # 判断越界\n            if nr < 1 or nr >= N or nc < 1 or nc >= M:\n                break\n            # 如果当前位置不合法，则不能继续向前走\n            if not valid[nr][nc]:\n                break\n            if not visited[nr][nc][d]:\n                visited[nr][nc][d] = True\n                q.append((nr, nc, d, steps + 1))\n    return -1\n\n\n# 读取输入数据\nwhile True:\n    n, m = map(int, input().split())\n    if n == 0 and m == 0:\n        break\n    grid = [list(map(int, input().split())) for _ in range(n)]\n    sx, sy, ex, ey, direction = input().split()\n    sx, sy, ex, ey = map(int, [sx, sy, ex, ey])\n\n    direction = direction.upper()  # 确保方向是大写\n\n    # 计算最短时间\n    result = bfs_min_time(grid, (sx, sy), (ex, ey), direction[0])\n    print(result)\n"
NUMBER=1376
SAMPLE='9 10\n0 0 0 0 0 0 1 0 0 0\n0 0 0 0 0 0 0 0 1 0\n0 0 0 1 0 0 0 0 0 0\n0 0 1 0 0 0 0 0 0 0\n0 0 0 0 0 0 1 0 0 0\n0 0 0 0 0 1 0 0 0 0\n0 0 0 1 1 0 0 0 0 0\n0 0 0 0 0 0 0 0 0 0\n1 0 0 0 0 0 0 0 1 0\n7 2 2 7 south\n0 0\n'
def run(x):
 with tempfile.TemporaryDirectory() as d:
  p=Path(d)/'m.py';p.write_text(REFERENCE);q=subprocess.run([sys.executable,'-I',str(p)],input=x,text=True,capture_output=True,timeout=120)
  if q.returncode:raise SystemExit(q.stderr)
  return q.stdout
def main():
 d=Path('data');d.mkdir(exist_ok=True)
 for p in d.glob('*'):p.unlink()
 for i,x in enumerate([SAMPLE]+[g1376_v2(s) for s in range(1, 40)]):
  (d/f'{i}.in').write_text(x);(d/f'{i}.out').write_text(run(x))
if __name__=='__main__':main()

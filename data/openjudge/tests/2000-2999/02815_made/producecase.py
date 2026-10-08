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

REFERENCE='# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md\n# Heading: 2815: 城堡问题\n# Fenced code block index: 3\n# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md\n# Upstream problem: http://cs101.openjudge.cn/2024sp_routine/02815/\n# License: not declared in source collection; no license is inferred.\nimport sys\nfrom collections import deque\n\n# 四个方向：西、北、东、南\ndirs = [(0, -1), (-1, 0), (0, 1), (1, 0)]\nwalls = [1, 2, 4, 8]  # 按顺序对应西北东南\n\ndef bfs(start_r, start_c, m, n, castle, visited):\n    q = deque()\n    q.append((start_r, start_c))\n    visited[start_r][start_c] = True\n    area = 0\n\n    while q:\n        r, c = q.popleft()\n        area += 1\n        val = castle[r][c]\n\n        for d, (dr, dc) in enumerate(dirs):\n            nr, nc = r + dr, c + dc\n            if 0 <= nr < m and 0 <= nc < n:\n                # 如果这个方向没有墙，并且未访问过\n                if not (val & walls[d]) and not visited[nr][nc]:\n                    visited[nr][nc] = True\n                    q.append((nr, nc))\n    return area\n\ndef main():\n    m = int(input().strip())  # 行数（南北）\n    n = int(input().strip())  # 列数（东西）\n\n    castle = [list(map(int, input().split())) for _ in range(m)]\n    visited = [[False] * n for _ in range(m)]\n\n    room_count = 0\n    max_area = 0\n\n    for r in range(m):\n        for c in range(n):\n            if not visited[r][c]:\n                room_count += 1\n                area = bfs(r, c, m, n, castle, visited)\n                max_area = max(max_area, area)\n\n    print(room_count)\n    print(max_area)\n\nif __name__ == "__main__":\n    main()\n'
NUMBER=2815
SAMPLE='4\n7\n11 6 11 6 3 10 6\n7 9 6 13 5 15 5\n1 10 12 7 13 7 5\n13 11 10 8 10 12 13\n'
def run(x):
 with tempfile.TemporaryDirectory() as d:
  p=Path(d)/'m.py';p.write_text(REFERENCE);q=subprocess.run([sys.executable,'-I',str(p)],input=x,text=True,capture_output=True,timeout=120)
  if q.returncode:raise SystemExit(q.stderr)
  return q.stdout
import re as _re
_NAT = _re.compile(r'(0|[1-9][0-9]*)\Z')
def _rooms(m, n, g):
    seen = [[False] * n for _ in range(m)]; sizes = []
    for si in range(m):
        for sj in range(n):
            if seen[si][sj]: continue
            seen[si][sj] = True; st = [(si, sj)]; cnt = 0
            while st:
                i, j = st.pop(); cnt += 1
                for bit, di, dj in ((1, 0, -1), (2, -1, 0), (4, 0, 1), (8, 1, 0)):
                    a, b = i + di, j + dj
                    if not g[i][j] & bit and 0 <= a < m and 0 <= b < n and not seen[a][b]:
                        seen[a][b] = True; st.append((a, b))
            sizes.append(cnt)
    return sizes

def valid(text):
    """题面契约：第 1、2 行各一个整数 m（南北向）、n（东西向），m,n<=50；
    其后 m 行各 n 个整数 p（0<=p<=50），单空格分隔；
    内墙计算两次（东墙与右邻西墙、南墙与下邻北墙一致）；至少两个房间。"""
    if not text.endswith('\n') or '\r' in text: return False
    lines = text[:-1].split('\n')
    if len(lines) < 3 or not _NAT.match(lines[0]) or not _NAT.match(lines[1]): return False
    m, n = int(lines[0]), int(lines[1])
    if not (1 <= m <= 50 and 1 <= n <= 50) or len(lines) != m + 2: return False
    g = []
    for ln in lines[2:]:
        p = ln.split(' ')
        if len(p) != n or not all(_NAT.match(t) for t in p): return False
        row = list(map(int, p))
        if not all(0 <= v <= 50 for v in row): return False
        g.append(row)
    for i in range(m):
        for j in range(n):
            if j + 1 < n and bool(g[i][j] & 4) != bool(g[i][j + 1] & 1): return False
            if i + 1 < m and bool(g[i][j] & 8) != bool(g[i + 1][j] & 2): return False
    return len(_rooms(m, n, g)) >= 2

def _grid(m, n, east, south):
    """east[i][j]/south[i][j] 为 True 表示 (i,j) 与右/下邻之间有墙；外墙一律存在。"""
    g = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if j == 0: g[i][j] |= 1
            if i == 0: g[i][j] |= 2
            if j == n - 1: g[i][j] |= 4
            if i == m - 1: g[i][j] |= 8
            if j + 1 < n and east[i][j]: g[i][j] |= 4; g[i][j + 1] |= 1
            if i + 1 < m and south[i][j]: g[i][j] |= 8; g[i + 1][j] |= 2
    return g

def _fmt(m, n, g):
    return f"{m}\n{n}\n" + "\n".join(" ".join(map(str, row)) for row in g) + "\n"

def _random(r, m, n, prob):
    while True:
        east = [[r.random() < prob for _ in range(n)] for _ in range(m)]
        south = [[r.random() < prob for _ in range(n)] for _ in range(m)]
        g = _grid(m, n, east, south)
        if len(_rooms(m, n, g)) >= 2: return _fmt(m, n, g)

def _snake(m, n):
    """蛇形长走廊占满除右下角外的全部方块（一个 m*n-1 的大房间 + 一个 1 格房间），递归 DFS 会很深。"""
    east = [[False] * n for _ in range(m)]
    south = [[True] * n for _ in range(m)]
    for i in range(m - 1):
        south[i][n - 1 if i % 2 == 0 else 0] = False
    last = m - 1
    # 最后一行与走廊相连，单独隔出右下角或左下角（走廊末端的另一端）
    lone = 0 if (m - 1) % 2 == 0 else n - 1   # 走廊进入最后一行的位置是 n-1 或 0
    lone = n - 1 - lone if n > 1 else 0
    if lone == n - 1: east[last][n - 2] = True
    else: east[last][0] = True
    return _fmt(m, n, _grid(m, n, east, south))

def _halves(m, n, vertical):
    east = [[False] * n for _ in range(m)]; south = [[False] * n for _ in range(m)]
    if vertical:
        for i in range(m): east[i][n // 2 - 1] = True
    else:
        for j in range(n): south[m // 2 - 1][j] = True
    return _fmt(m, n, _grid(m, n, east, south))

def cases():
    r = random.Random(2815_2026)
    out = []
    # 最小规模：两个单格房间
    out.append(_fmt(1, 2, _grid(1, 2, [[True, False]], [[False, False]])))
    out.append(_fmt(2, 1, _grid(2, 1, [[False], [False]], [[True], [False]])))
    # 每格都是独立房间
    out.append(_random(r, 3, 4, 1.0))
    # 小规模随机，墙密度各异
    for _ in range(16):
        m, n = r.randint(1, 10), r.randint(1, 10)
        while m * n < 4: m, n = r.randint(1, 10), r.randint(1, 10)
        out.append(_random(r, m, n, r.choice((.15, .3, .5, .7))))
    # 行列不等的中大规模（m、n 读反会出错）
    for m, n, p in ((50, 20, .3), (20, 50, .3), (50, 1, .2), (1, 50, .2), (37, 50, .45), (50, 43, .25)):
        out.append(_random(r, m, n, p))
    # 满规模 50x50：不同墙密度
    for p in (.05, .2, .35, .5, .7, .95):
        out.append(_random(r, 50, 50, p))
    out.append(_random(r, 50, 50, 1.0))              # 2500 个单格房间
    # 满规模蛇形长走廊（大房间 2499 格，递归 DFS 默认栈深会爆）
    out.append(_snake(50, 50))
    out.append(_snake(49, 50))
    out.append(_snake(50, 2))
    # 两半对称
    out.append(_halves(50, 50, True))
    out.append(_halves(50, 50, False))
    out.append(_halves(2, 50, True))
    # 大房间不在左上角
    out.append(_random(r, 50, 50, .12))
    return out

def main():
 d=Path('data');d.mkdir(exist_ok=True)
 for p in d.glob('*'):p.unlink()
 for i,x in enumerate([SAMPLE]+cases()):
  assert valid(x),i
  (d/f'{i}.in').write_text(x);(d/f'{i}.out').write_text(run(x))
if __name__=='__main__':main()

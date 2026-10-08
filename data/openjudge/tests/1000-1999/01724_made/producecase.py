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

# ---- 题面契约与 1724 专用生成器 ----
def valid(text):
    """K（0..10000）、N（2..100）、R（1..10000）各占一行，其后恰 R 行 “S D L T”（单空格分隔），
    1<=S,D<=N，1<=L<=100，0<=T<=100。"""
    try:
        if not text.endswith('\n') or '\r' in text: return False
        lines = text[:-1].split('\n')
        if len(lines) < 3 or not all(lines[i].isdigit() and lines[i] == str(int(lines[i])) for i in range(3)): return False
        k, n, r = int(lines[0]), int(lines[1]), int(lines[2])
        if not (0 <= k <= 10000 and 2 <= n <= 100 and 1 <= r <= 10000) or len(lines) != 3 + r: return False
        for ln in lines[3:]:
            f = ln.split(' ')
            if len(f) != 4 or not all(x.isdigit() and x == str(int(x)) for x in f): return False
            s, d, l, t = map(int, f)
            if not (1 <= s <= n and 1 <= d <= n and 1 <= l <= 100 and 0 <= t <= 100): return False
        return True
    except Exception:
        return False

def _brute(text):
    """暴力：枚举 1 出发的全部简单路径（只用于小图核对）。"""
    v = list(map(int, text.split())); k, n, r = v[:3]
    adj = [[] for _ in range(n + 1)]
    for i in range(r):
        s, d, l, t = v[3 + 4 * i:7 + 4 * i]; adj[s].append((d, l, t))
    best = [None]; seen = {1}
    def go(u, L, C):
        if u == n:
            if best[0] is None or L < best[0]: best[0] = L
            return
        for d, l, t in adj[u]:
            if d not in seen and C + t <= k:
                seen.add(d); go(d, L + l, C + t); seen.discard(d)
    go(1, 0, 0)
    return f"{best[0] if best[0] is not None else -1}\n"

def _fmt(k, n, edges):
    return f"{k}\n{n}\n{len(edges)}\n" + "\n".join("%d %d %d %d" % e for e in edges) + "\n"

def gen_file(seed):
    r = random.Random(1724 * 1_000_003 + seed)
    if seed == 1:   # 最小：N=2、R=1，过路费恰好等于 K
        return "7\n2\n1\n1 2 5 7\n"
    if seed == 2:   # K=0：只能走免费路
        return "0\n3\n4\n1 3 10 1\n1 2 4 0\n2 3 9 0\n2 2 1 0\n"
    if seed == 3:   # 到不了 N（只有反向边）
        return "100\n4\n3\n2 1 3 0\n4 1 2 0\n1 3 1 0\n"
    if seed == 4:   # 能到但钱不够
        return "5\n3\n3\n1 2 1 3\n2 3 1 3\n1 3 50 6\n"
    if seed <= 18:  # 小图随机，含自环、重边
        n = r.randint(2, 9); k = r.choice([0, r.randint(0, 30), r.randint(0, 300)])
        edges = [(r.randint(1, n), r.randint(1, n), r.randint(1, 100), r.choice([0, r.randint(0, 100), r.randint(0, 20)]))
                 for _ in range(r.randint(1, 30))]
        if seed % 3:  # 多数小图补一条 1→…→N 的链，免得 -1 太多
            edges += [(i, i + 1, r.randint(1, 100), r.randint(0, 40)) for i in range(1, n)]
            r.shuffle(edges)
        return _fmt(k, n, edges)
    if seed <= 25:  # 分层“贵而短 / 便宜而长”：每城的帕累托前沿很长，卡掉只记最短或只记最省的贪心
        n = 100; k = r.choice([r.randint(500, 3000), 10000, r.randint(50, 400)]); edges = []
        layers = [[1]] + [list(range(2 + 3 * i, 5 + 3 * i)) for i in range(33)] + [[100]]
        for a, b in zip(layers, layers[1:]):
            for u in a:
                for v in b:
                    for _ in range(r.randint(2, 6)):
                        l = r.randint(1, 100); t = max(0, min(100, 100 - l + r.randint(-10, 10)))
                        edges.append((u, v, l, t))
        while len(edges) < 10000:   # 干扰边只向回连（或自环），不提供捷径
            u = r.randint(2, 100); v = r.randint(1, u)
            edges.append((u, v, r.randint(1, 100), r.randint(0, 100)))
        r.shuffle(edges); return _fmt(k, n, edges[:10000])
    if seed <= 31:  # 满规模随机
        n = r.randint(90, 100); k = r.choice([0, r.randint(0, 200), r.randint(0, 10000), 10000])
        edges = [(r.randint(1, n), r.randint(1, n), r.randint(1, 100), r.randint(0, 100)) for _ in range(10000)]
        return _fmt(k, n, edges)
    if seed <= 35:  # 稀疏长链 + 干扰边：路径长、需要跨越很多城市
        n = 100; k = r.randint(100, 3000); edges = []
        for i in range(1, n):
            edges.append((i, i + 1, r.randint(50, 100), r.randint(0, 30)))
            edges.append((i, i + 1, r.randint(1, 30), r.randint(30, 100)))
        for _ in range(r.randint(100, 3000)):
            u = r.randint(1, n - 1); v = r.randint(1, n)
            edges.append((u, v, r.randint(1, 100), r.randint(0, 100)))
        r.shuffle(edges); return _fmt(k, n, edges)
    # 满规模但 N 不可达或钱刚好不够的 -1
    n = 100; edges = []
    if seed % 2:
        for _ in range(9999):
            u, v = r.randint(1, n - 1), r.randint(1, n - 1)
            edges.append((u, v, r.randint(1, 100), r.randint(0, 100)))
        edges.append((n, r.randint(1, n - 1), 1, 0))
        return _fmt(10000, n, edges)
    for _ in range(10000):
        u, v = r.randint(1, n), r.randint(1, n)
        t = r.randint(0, 100)
        if v == n and u != n: t = r.randint(60, 100)
        edges.append((u, v, r.randint(1, 100), t))
    return _fmt(59, n, edges)

REFERENCE='# 参考解（审计时重写）：按长度做 Dijkstra，状态 (城市, 已花费)；\n# 同一城市后弹出的状态若花费不低于先前弹出者即被支配，直接丢弃。\nimport sys, heapq\ndef main():\n    data = sys.stdin.buffer.read().split()\n    k, n, r = int(data[0]), int(data[1]), int(data[2])\n    adj = [[] for _ in range(n + 1)]\n    p = 3\n    for _ in range(r):\n        s, d, l, t = int(data[p]), int(data[p + 1]), int(data[p + 2]), int(data[p + 3]); p += 4\n        if s != d and t <= k:\n            adj[s].append((d, l, t))\n    best_cost = [k + 1] * (n + 1)\n    pq = [(0, 0, 1)]\n    while pq:\n        length, cost, u = heapq.heappop(pq)\n        if cost >= best_cost[u]:\n            continue\n        best_cost[u] = cost\n        if u == n:\n            print(length); return\n        for v, l, t in adj[u]:\n            c = cost + t\n            if c < best_cost[v]:\n                heapq.heappush(pq, (length + l, c, v))\n    print(-1)\nmain()\n'
NUMBER=1724
SAMPLE='5\n6\n7\n1 2 2 3\n2 4 3 3\n3 4 2 4\n1 3 4 1\n4 6 2 1\n3 5 2 0\n5 4 3 2\n'
def run(x):
 with tempfile.TemporaryDirectory() as d:
  p=Path(d)/'m.py';p.write_text(REFERENCE);q=subprocess.run([sys.executable,'-I',str(p)],input=x,text=True,capture_output=True,timeout=120)
  if q.returncode:raise SystemExit(q.stderr)
  return q.stdout
def main():
 d=Path('data');d.mkdir(exist_ok=True)
 for p in d.glob('*'):p.unlink()
 for i,x in enumerate([SAMPLE]+[gen_file(s) for s in range(1, 40)]):
  (d/f'{i}.in').write_text(x);(d/f'{i}.out').write_text(run(x))
if __name__=='__main__':main()

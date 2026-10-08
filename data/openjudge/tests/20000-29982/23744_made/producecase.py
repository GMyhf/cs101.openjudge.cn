import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE='# 参考解（审计时重写）：原 AC 提交 52178544 只用 min(a,b+c)/min(b,a+c)/min(c,a+b) 的闭式，\n# 漏掉了「两步对角线 (1,1)+(1,-1) 合成一步 x」等组合，c 小于 a 或 b 时会偏大。\n# 这里在位移网格上跑 Dijkstra 求任意两点间最小成本（成本只与位移有关），再枚举 6 种拾取顺序。\nimport heapq\nfrom itertools import permutations\na, b, c = map(float, input().split())\nparts = []\nfor _ in range(3):\n    s, x, y = input().split()\n    parts.append((s, int(x), int(y)))\nR = 205  # 任意两点位移的分量绝对值不超过 199，最优路径可重排到不越出位移框外一格\nW = 2 * R + 1\nINF = float("inf")\ndist = [INF] * (W * W)\nstart = R * W + R\ndist[start] = 0.0\nheap = [(0.0, start)]\nmoves = [(1, 0, a), (-1, 0, a), (0, 1, b), (0, -1, b), (1, 1, c), (1, -1, c), (-1, 1, c), (-1, -1, c)]\nwhile heap:\n    d, u = heapq.heappop(heap)\n    if d > dist[u]:\n        continue\n    x, y = divmod(u, W)\n    for dx, dy, w in moves:\n        nx, ny = x + dx, y + dy\n        if 0 <= nx < W and 0 <= ny < W:\n            v = nx * W + ny\n            nd = d + w\n            if nd < dist[v]:\n                dist[v] = nd\n                heapq.heappush(heap, (nd, v))\ndef cost(p, q):\n    return dist[(q[0] - p[0] + R) * W + (q[1] - p[1] + R)]\nbest = None\nfor order in permutations(range(3)):\n    pts = [(0, 0)] + [(parts[i][1], parts[i][2]) for i in order] + [(100, 100)]\n    total = sum(cost(pts[i], pts[i + 1]) for i in range(4))\n    if best is None or total < best[0]:\n        best = (total, order)\nprint(" ".join(parts[i][0] for i in best[1]))\nprint(f"{best[0]:.2f}")\n'
SAMPLE='1.0 1.0 1.4\nAdamantium 92 40\ninfinity_gauntlet -74 -25\ndecade_armor 95 72\n'
GENERATOR_NAME='g23744'
def _num(cents):
    return f"{cents/100:.1f}" if cents%10==0 else f"{cents/100:.2f}"

def _dist_table(a,b,c,R=200):
    # 生成器内部用整数（分）跑 Dijkstra，用来精确判定最优顺序是否唯一
    import heapq
    W=2*R+1; INF=1<<60; dist=[INF]*(W*W); st=R*W+R; dist[st]=0; h=[(0,st)]
    mv=[(1,0,a),(-1,0,a),(0,1,b),(0,-1,b),(1,1,c),(1,-1,c),(-1,1,c),(-1,-1,c)]
    while h:
        d,u=heapq.heappop(h)
        if d>dist[u]: continue
        x,y=divmod(u,W)
        for dx,dy,w in mv:
            nx,ny=x+dx,y+dy
            if 0<=nx<W and 0<=ny<W and d+w<dist[nx*W+ny]:
                dist[nx*W+ny]=d+w; heapq.heappush(h,(d+w,nx*W+ny))
    return lambda p,q: dist[(q[0]-p[0]+R)*W+(q[1]-p[1]+R)]

_NAME_CHARS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-"

def _costs(r,kind):
    if kind=='natural':      # max(a,b) <= c <= a+b，与样例同类
        a=r.randint(50,500); b=r.randint(50,500); c=r.randint(max(a,b),a+b)
    elif kind=='unit':       # a=b=1
        a=b=100; c=r.choice([100,140,141,150,170,200])
    elif kind=='cheapdiag':  # 对角线比轴向便宜，两步对角线可合成一步轴向
        a=r.randint(150,600); b=r.randint(150,600); c=r.randint(10,min(a,b)-20)
    elif kind=='zero':       # 某一成本为 0
        a,b,c=r.randint(0,400),r.randint(0,400),r.randint(50,400)
        z=r.randrange(3); a,b,c=[0 if i==z else v for i,v in enumerate((a,b,c))]
    else:                    # 任意非负
        a,b,c=r.randint(0,500),r.randint(0,500),r.randint(0,500)
    return a,b,c

def g23744(r,kind='general',edge=False):
    while True:
        a,b,c=_costs(r,kind)
        names=set()
        while len(names)<3:
            k=20 if edge else r.randint(1,20)
            names.add("".join(r.choice(_NAME_CHARS) for _ in range(k)))
        names=sorted(names); r.shuffle(names)
        lo,hi=(-99,99)
        if edge: pts=[(r.choice([-99,99]),r.randint(lo,hi)) if r.random()<.5 else (r.randint(lo,hi),r.choice([-99,99])) for _ in range(3)]
        else: pts=[(r.randint(lo,hi),r.randint(lo,hi)) for _ in range(3)]
        D=_dist_table(a,b,c)
        from itertools import permutations
        tot=sorted(sum(D(q[i],q[i+1]) for i in range(4)) for q in
                   ([(0,0)]+[pts[i] for i in o]+[(100,100)] for o in permutations(range(3))))
        if tot[1]-tot[0]>=1:  # 最优顺序唯一（至少差 0.01），避免输出不唯一
            text=f"{_num(a)} {_num(b)} {_num(c)}\n"+"\n".join(f"{s} {x} {y}" for s,(x,y) in zip(names,pts))+"\n"
            assert valid(text)
            return text

def valid(text):
    """题面：4 行；第一行 a b c 三个非负实数；其后 3 行 s x y，s 为不超过 20 个非空字符，x、y 为整数且 -100<x,y<100。"""
    import re
    lines=text.split('\n')
    if lines and lines[-1]=='': lines.pop()
    if len(lines)!=4: return False
    t=lines[0].split()
    if len(t)!=3 or not all(re.fullmatch(r'[0-9]+(\.[0-9]+)?',v) for v in t): return False
    for l in lines[1:]:
        t=l.split()
        if len(t)!=3 or not 1<=len(t[0])<=20: return False
        if not all(re.fullmatch(r'-?[0-9]+',v) for v in t[1:]): return False
        if not all(-100<int(v)<100 for v in t[1:]): return False
    return True

def build_cases():
    plan=(['natural']*10+['unit']*5+['cheapdiag']*8+['zero']*4+['general']*10)
    cases=[SAMPLE]+[g23744(random.Random(s),k) for s,k in enumerate(plan,1)]
    cases+=[g23744(random.Random(1000+s),k,edge=True) for s,k in enumerate(['natural','cheapdiag'])]
    return cases

def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    d=Path('data'); d.mkdir(exist_ok=True)
    cases=build_cases()
    assert len(cases)==40 and len(set(cases))==40 and all(valid(c) for c in cases)
    for i,c in enumerate(cases): (d/f'{i}.in').write_text(c); (d/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()

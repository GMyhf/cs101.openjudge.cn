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
        return gen_2802(r, seed)
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

REFERENCE='# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md\n# Heading: 2802: 小游戏\n# Fenced code block index: 6\n# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md\n# Upstream problem: http://cs101.openjudge.cn/2024fallroutine/02802/\n# License: not declared in source collection; no license is inferred.\nimport sys\nfrom collections import deque\nfrom collections import defaultdict\n\ndef bfs(start, end, grid, h, w):\n    queue = deque([start])\n    in_queue = defaultdict(lambda: float(\'inf\'))\n    dirs = [(0, -1), (-1, 0), (0, 1), (1, 0)]\n    min_x = float(\'inf\')\n    while queue:\n        x, y, d, seg = queue.popleft()\n\n        for i, (dx, dy) in enumerate(dirs):\n            nx, ny = x + dx, y + dy\n\n            new_seg = seg if i == d else seg + 1\n            if (nx, ny) == end:\n                min_x = min(min_x, new_seg)\n                continue\n\n            if (0 <= nx < h + 2 and 0 <= ny < w + 2 and new_seg<in_queue[(nx,ny,i)]\n                    and grid[nx][ny] != \'X\'):\n                    in_queue[(nx, ny, i)] = new_seg\n                    queue.append((nx, ny, i, new_seg))\n\n    return min_x\n\n\nboard_num = 1\nwhile True:\n    w, h = map(int, input().split())\n    if w == h == 0:\n        break\n\n    grid = [\' \' * (w + 2)] + [\' \' + input() + \' \' for _ in range(h)] + [\' \' * (w + 2)]\n    print(f"Board #{board_num}:")\n    pair_num = 1\n    while True:\n        y1, x1, y2, x2 = map(int, input().split())\n        if x1 == y1 == x2 == y2 == 0:\n            break\n\n        start = (x1, y1, -1, 0)\n        end = (x2, y2)\n\n        seg = bfs(start, end, grid, h, w)\n        if seg == float(\'inf\'):\n            print(f"Pair {pair_num}: impossible.")\n        else:\n            print(f"Pair {pair_num}: {seg} segments.")\n        pair_num += 1\n\n    print()\n    board_num += 1\n'
NUMBER=2802
SAMPLE='5 4\nXXXXX\nX   X\nXXX X\n XXX \n2 3 5 3\n1 3 4 4\n2 3 3 4\n0 0 0 0\n0 0\n'
import re as _re
def valid(text):
    """题面：不多于 10 组；每组 w h (1..75)，h 行每行恰 w 个 'X' 或空格；
    之后若干行 x1 y1 x2 y2（1<=x<=w, 1<=y<=h，两位置不同且都是卡片），以 0 0 0 0 结束；最后 0 0。"""
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    i = 0; boards = 0
    num = r'(0|[1-9][0-9]*)'
    while True:
        if i >= len(lines):
            return False
        m = _re.fullmatch(num + ' ' + num, lines[i]); i += 1
        if not m:
            return False
        w, h = int(m.group(1)), int(m.group(2))
        if w == 0 and h == 0:
            break
        if not (1 <= w <= 75 and 1 <= h <= 75):
            return False
        boards += 1
        if boards > 10 or i + h > len(lines):
            return False
        grid = lines[i:i + h]; i += h
        if any(len(row) != w or set(row) - {'X', ' '} for row in grid):
            return False
        while True:
            if i >= len(lines):
                return False
            m = _re.fullmatch(' '.join([num] * 4), lines[i]); i += 1
            if not m:
                return False
            x1, y1, x2, y2 = map(int, m.groups())
            if x1 == y1 == x2 == y2 == 0:
                break
            if not (1 <= x1 <= w and 1 <= x2 <= w and 1 <= y1 <= h and 1 <= y2 <= h):
                return False
            if (x1, y1) == (x2, y2):
                return False
            if grid[y1 - 1][x1 - 1] != 'X' or grid[y2 - 1][x2 - 1] != 'X':
                return False
    return i == len(lines) and boards >= 1


def gen_2802(r, seed):
    """查询的两个位置都必须是卡片（题面：给出两个卡片的位置）。
    覆盖：75x75 满规模、10 组、全满板、边框板（只能绕到板外）、迷宫条纹、相邻卡片、无查询的板、impossible。"""
    nb = 10 if seed % 4 == 0 else r.randint(1, 4)
    parts = []
    for b in range(nb):
        if (seed % 5 == 0 and b < 3) or (seed % 4 == 0 and b < 2):
            w, h = 75, 75
        elif seed % 3 == 0:
            w, h = r.randint(1, 75), r.randint(1, 75)
        else:
            w, h = r.randint(1, 12), r.randint(1, 12)
        style = (seed + b) % 5
        g = [[' '] * w for _ in range(h)]
        if style == 0:
            p = r.uniform(.15, .7)
            for y in range(h):
                for x in range(w):
                    if r.random() < p: g[y][x] = 'X'
        elif style == 1:
            g = [['X'] * w for _ in range(h)]
            for _ in range(r.randint(0, w * h // 6)):
                g[r.randrange(h)][r.randrange(w)] = ' '
        elif style == 2:
            for y in range(h):
                for x in range(w):
                    if y in (0, h - 1) or x in (0, w - 1) or r.random() < .25: g[y][x] = 'X'
        elif style == 3:
            for y in range(0, h, 2):
                gap = r.randrange(w)
                for x in range(w):
                    if x != gap: g[y][x] = 'X'
            for _ in range(r.randint(1, 1 + w * h // 20)):
                g[r.randrange(h)][r.randrange(w)] = 'X'
        else:
            for y in range(h):
                for x in range(w):
                    if r.random() < .08: g[y][x] = 'X'
        cards = [(x + 1, y + 1) for y in range(h) for x in range(w) if g[y][x] == 'X']
        while len(cards) < 2 and w * h >= 2:
            x, y = r.randrange(w), r.randrange(h)
            if g[y][x] != 'X':
                g[y][x] = 'X'; cards.append((x + 1, y + 1))
        qs = []
        cardset = set(cards)
        if len(cards) >= 2 and not (seed % 7 == 0 and b == nb - 1):
            big = w * h > 1500
            q = r.randint(1, 6 if big and nb > 4 else 12 if big else 25)
            for _ in range(q):
                if r.random() < .1:
                    x, y = r.choice(cards)
                    nbr = [(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if (x + dx, y + dy) in cardset]
                    if nbr:
                        qs.append((x, y) + r.choice(nbr)); continue
                a, c = r.sample(cards, 2)
                qs.append(a + c)
        parts.append(f'{w} {h}\n' + '\n'.join(''.join(row) for row in g) + '\n' +
                     ''.join('%d %d %d %d\n' % t for t in qs) + '0 0 0 0\n')
    return ''.join(parts) + '0 0\n'


def run(x):
 with tempfile.TemporaryDirectory() as d:
  p=Path(d)/'m.py';p.write_text(REFERENCE);q=subprocess.run([sys.executable,'-I',str(p)],input=x,text=True,capture_output=True,timeout=120)
  if q.returncode:raise SystemExit(q.stderr)
  return q.stdout
def main():
 d=Path('data');d.mkdir(exist_ok=True)
 for p in d.glob('*'):p.unlink()
 for i,x in enumerate([SAMPLE]+[generate(NUMBER,s) for s in range(1, 40)]):
  (d/f'{i}.in').write_text(x);(d/f'{i}.out').write_text(run(x))
if __name__=='__main__':main()

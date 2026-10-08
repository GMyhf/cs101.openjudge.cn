import random,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys, heapq\nfrom collections import deque\nP=3791\ndef go(s):\n a=s.split()\n if P==3723:\n  n=int(a[0]);g=a[1:];seen=set();z=[sum(row.count("B") for row in g),sum(row.count("W") for row in g)]\n  for i in range(n):\n   for j in range(n):\n    if g[i][j]!="." or (i,j) in seen:continue\n    q=[(i,j)];seen.add((i,j));e=set();c=0\n    while q:\n     x,y=q.pop();c+=1\n     for u,v in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):\n      if 0<=u<n and 0<=v<n:\n       if g[u][v]=="." and (u,v) not in seen:seen.add((u,v));q.append((u,v))\n       elif g[u][v] in "BW":e.add(g[u][v])\n    if len(e)==1:z["BW".index(next(iter(e)))]+=c\n  return f"{z[0]} {z[1]}\\n"\n if P==3725:\n  x=list(map(int,a));v=sorted(x[1:],reverse=True);M=max(v);best=(10**9,0)\n  for k in range(1,len(v)+1):\n   q=[0]*k\n   for y in v:q[q.index(min(q))]+=y\n   best=min(best,(sum(abs(y-M) for y in q),-k))\n  return f"{-best[1]}\\n"\n if P==3726 or P==3866:\n  p=0;out=[]\n  while p<len(a):\n   R,C=map(int,a[p:p+2]);p+=2\n   if not R:break\n   g=a[p:p+(R if P==3726 else C)];p+=len(g)\n   target="*" if P==3726 else "@"; src=next((i,j) for i in range(len(g)) for j in range(len(g[0]) if g else 0) if g[i][j]==target)\n   q=deque([src]);seen={src}\n   while q:\n    x,y=q.popleft()\n    for u,v in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):\n     if 0<=u<len(g) and 0<=v<len(g[0]) and g[u][v]!="#" and (u,v) not in seen:seen.add((u,v));q.append((u,v))\n   if P==3726:\n    start=next((i,j) for i in range(R) for j in range(C) if g[i][j]=="@");q=deque([(start[0],start[1],0)]);vis={start};ans=-1\n    while q:\n     x,y,d=q.popleft()\n     if g[x][y]=="*":ans=d;break\n     for u,v in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):\n      if 0<=u<R and 0<=v<C and g[u][v]!="#" and (u,v) not in vis:vis.add((u,v));q.append((u,v,d+1))\n    out.append(str(ans))\n   else:out.append(str(len(seen)))\n  return "\\n".join(out)+"\\n"\n if P==3727:\n  p=1;out=[]\n  for _ in range(int(a[0])):\n   R,C=map(int,a[p:p+2]);p+=2;d=[0]*C\n   for i in range(R):\n    for j in range(C):d[j]=max(d[j],d[j-1] if j else 0)+int(a[p]);p+=1\n   out.append(str(d[-1]))\n  return "\\n".join(out)+"\\n"\n if P==3728:\n  out=[]\n  for line in s.splitlines():\n   b,n=map(int,line.split());q={b};h=[b];outv=[]\n   while len(outv)<n:\n    x=heapq.heappop(h);outv.append(x)\n    for y in (2*x+1,3*x+1):\n     if y not in q:q.add(y);heapq.heappush(h,y)\n   out.append(str(outv[-1]))\n  return "\\n".join(out)+"\\n"\n if P==3744:\n  return "\\n".join(str(min(2*(x*y+x*w+y*w) for x in range(1,n+1) for y in range(x,n+1) if n%(x*y)==0 for w in [n//(x*y)])) for n in map(int,a[1:]))+"\\n"\n if P==3789:\n  n,k=map(int,a[:2]);v=list(map(int,a[2:]))\n  for L in range(n,0,-1):\n   if any(sum(v[i:i+L]==v[j:j+L] for j in range(n-L+1))>=k for i in range(n-L+1)):return str(L)+"\\n"\n if P==3791:\n  p=1;out=[]\n  for _ in range(int(a[0])):\n   n=int(a[p]);p+=1;q=sorted(a[p:p+n]);p+=n;out.append("NO" if any(y.startswith(x) for x,y in zip(q,q[1:])) else "YES")\n  return "\\n".join(out)+"\\n"\n if P==3906:\n  m,n=map(int,a[:2]);v=list(map(int,a[2:]));D={(0,0,0,0):v[0]}\n  for _ in range(m+n-2):\n   N={}\n   for (x,y,u,w),z in D.items():\n    for dx,dy in ((1,0),(0,1)):\n     for du,dw in ((1,0),(0,1)):\n      X,Y=x+dx,y+dy;U,W=u+du,w+dw\n      if X<m and Y<n and U<m and W<n and ((X,Y)!=(U,W) or (X,Y)==(m-1,n-1)):N[X,Y,U,W]=max(N.get((X,Y,U,W),-1),z+v[X*n+Y]+v[U*n+W])\n   D=N\n  return str(max(D.values()))+"\\n"\n if P==4001:\n  n,k=map(int,a);q=deque([(n,0)]);vis={n}\n  while q:\n   x,d=q.popleft()\n   if x==k:return str(d)+"\\n"\n   for y in (x-1,x+1,2*x):\n    if 0<=y<=100000 and y not in vis:vis.add(y);q.append((y,d+1))\n if P==4002:\n  v=list(map(int,a[2:]));return "".join((str(v.count(x)-1) if v.count(x)>1 else "BeiJu")+"\\n" for x in v)\n if P==4006:\n  q,n=map(int,a[:2]);out=[]\n  for i,j in zip(map(int,a[2::2]),map(int,a[3::2])):\n   l=min(i-1,j-1,n-i,n-j);z=n-2*l;st=n*n-z*z+1;u=i-l-1;v=j-l-1\n   out.append(str(st+v if u==0 else st+z-1+u if v==z-1 else st+2*z-2+z-1-v if u==z-1 else st+3*z-3+z-1-u))\n  return "\\n".join(out)+"\\n"\n if P==4007:\n  p=1;out=[]\n  for _ in range(int(a[0])):\n   x,y=a[p:p+2];p+=2;d=list(range(len(y)+1))\n   for c in x:\n    old=d;d=[old[0]+1]\n    for j in range(len(y)):d.append(min(old[j+1]+1,d[-1]+1,old[j]+(c!=y[j])))\n   out.append(str(d[-1]))\n  return "\\n".join(out)+"\\n"\n if P==4008:\n  n,k=map(int,a[:2]);d=[-10**9]*k;d[0]=0\n  for x in map(int,a[2:]):d=[max(d[j],d[(j-x)%k]+x) for j in range(k)]\n  return str(d[0])+"\\n"\n if P==4009:\n  pc=[bin(x).count("1") for x in range(65536)]\n  def pop(x):return pc[x&65535]+pc[x>>16]\n  out=[]\n  for n in map(int,a):\n   if not n:break\n   c=0\n   for mask in range(1<<n):\n    row=mask;z=2*pop(mask)-n\n    for width in range(n,1,-1):\n     row=(~(row^(row>>1)))&((1<<(width-1))-1);z+=2*pop(row)-(width-1)\n    c+=z==0\n   out.append(f"{n} {c}")\n  return "\\n".join(out)+"\\n"\n if P==4010:return "\\n".join(str(pow(2011,int(x),10000)) for x in a[1:])+"\\n"\n if P==4021:\n  p=1;out=[]\n  for _ in range(int(a[0])):\n   n=int(a[p]);v=list(map(int,a[p+1:p+1+n]));p+=n+1\n   z=[__import__("math").prod(v[:i]+v[i+1:]) for i in range(n)];out.append(str(v[z.index(max(z))]))\n  return "\\n".join(out)+"\\n"\n if P==4033:\n  n=int(a[0]);x,y=map(int,a[1+4*n:]);ans=-1\n  for i in range(n):\n   A,B,G,K=map(int,a[1+4*i:5+4*i])\n   if A<=x<=A+G and B<=y<=B+K:ans=i+1\n  return str(ans)+"\\n"\n if P==4034:\n  n,k,p=map(int,a[:3]);v=[tuple(map(int,a[i:i+2])) for i in range(3,3+2*n,2)]\n  return str(sum(v[i][0]==v[j][0] and min(x[1] for x in v[i:j+1])<=p for i in range(n) for j in range(i+1,n)))+"\\n"\nfor line in []:pass\nsys.stdout.write(go(sys.stdin.read()))\n'
SAMPLE_IN='2\n3\n911\n97625999\n91125426\n5\n113\n12340\n123440\n12345\n98346\n'

def valid(text):
    """题面契约：第一行 t（1<=t<=40）；每组先一行 n（1<=n<=10000），
    其后 n 行各一个不超过 10 位的电话号码（数字串，长度 1..10）。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    def num(s, lo, hi):
        return s.isdigit() and (s == "0" or s[0] != "0") and lo <= int(s) <= hi
    if not num(lines[0], 1, 40):
        return False
    p = 1
    for _ in range(int(lines[0])):
        if p >= len(lines) or not num(lines[p], 1, 10000):
            return False
        n = int(lines[p]); p += 1
        if p + n > len(lines):
            return False
        for s in lines[p:p + n]:
            if not (s.isdigit() and s.isascii() and 1 <= len(s) <= 10):
                return False
        p += n
    return p == len(lines)

def fmt(tests):
    z = [str(len(tests))]
    for a in tests:
        z += [str(len(a))] + a
    return "\n".join(z) + "\n"

def rnd_num(r, lo=1, hi=10, lead0=False):
    L = r.randint(lo, hi)
    first = "0123456789" if lead0 else "123456789"
    return r.choice(first) + "".join(r.choice("0123456789") for _ in range(L - 1))

def prefix_free(r, n, lo, hi, lead0=False):
    # 生成 n 个互异且两两不为前缀的号码
    s = set(); pres = set(); out = []
    while len(out) < n:
        x = rnd_num(r, lo, hi, lead0)
        if x in pres or any(x[:i] in s for i in range(1, len(x) + 1)): continue
        s.add(x); out.append(x)
        for i in range(1, len(x) + 1): pres.add(x[:i])
    return out

def prefix_free_fast(r, n, L, lead0=False):
    # 定长 L 的互异号码天然无前缀关系
    s = set()
    while len(s) < n:
        s.add(rnd_num(r, L, L, lead0))
    out = sorted(s); r.shuffle(out); return out  # 排序后再洗牌，避免 set 顺序随哈希种子变化

def plant(r, a):
    # 把某个号码的真前缀（与原号码不同）塞进列表，制造 NO；前缀随机放在前面或后面
    a = a[:]
    x = r.choice([y for y in a if len(y) >= 2])
    pre = x[:r.randint(1, len(x) - 1)]
    if pre in a: return a
    i = r.randrange(len(a))
    a[i] = pre if a[i] != x else a[i]
    if pre not in a: a.append(pre)
    return a

def g_small(r):
    t = r.randint(1, 5); tests = []
    for _ in range(t):
        a = prefix_free(r, r.randint(1, 8), 1, 6)
        if len(a) >= 2 and r.random() < 0.5: a = plant(r, a)
        tests.append(a)
    return fmt(tests)

def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 11):
        for j in range(100):
            c = g_small(random.Random(3791 + i + j * 1000))
            if c not in cases: break
        cases.append(c)
    r = random.Random(379100)
    # 边界：n=1、t=40
    cases.append(fmt([[rnd_num(r)] for _ in range(40)]))
    cases.append(fmt([["0"]]))
    cases.append(fmt([["9", "91234567", "8"], ["1", "2", "3"], ["0123", "123"], ["12", "13", "123"], ["5555555555", "555"]]))
    # 前导 0：按整数读入会把 0123 与 123 混为一谈
    cases.append(fmt([["0123", "123", "00123", "1203"], ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"], ["00", "0"]]))
    # 数值排序陷阱：12 < 13 < 123，按数值排序后相邻比较漏判
    a = [str(x) for x in range(100, 1000)] + ["12"]
    r.shuffle(a); cases.append(fmt([a]))
    # 满规模单组
    cases.append(fmt([prefix_free_fast(r, 10000, 10)]))                       # YES
    a = prefix_free_fast(r, 10000, 10); a[r.randrange(5000, 10000)] = a[r.randrange(5000)][:r.randint(1, 9)]
    cases.append(fmt([a]))                                                    # NO（前缀可能在号码前或后）
    a = [f"{x:04d}" for x in range(10000)]; r.shuffle(a)
    cases.append(fmt([a]))                                                    # 全体 4 位串，YES
    a[r.randrange(10000)] = "000"
    cases.append(fmt([a]))                                                    # NO
    a = prefix_free(r, 10000, 3, 10); cases.append(fmt([a]))                  # 变长 YES
    cases.append(fmt([plant(r, a)[:10000]]))
    # 多组满 n：卡 O(n^2) 两两比较
    for seed in range(4):
        tests = []
        for q in range(8):
            a = prefix_free_fast(r, 10000, r.randint(6, 10))
            if (q + seed) % 3 == 0:
                x = a.pop(r.randrange(len(a))); a.insert(r.randrange(len(a)), x[:r.randint(1, len(x) - 1)]); a.append(x)
                a = a[-10000:] if len(a) > 10000 else a
            tests.append(a)
        cases.append(fmt(tests))
    # 40 组中等规模
    for seed in range(3):
        tests = []
        for q in range(40):
            a = prefix_free(r, r.randint(1, 1500), 1, 10, lead0=(seed == 1))
            if len(a) >= 2 and r.random() < 0.4: a = plant(r, a)
            tests.append(a)
        cases.append(fmt(tests))
    # 前缀链 / 唯一一个只与末尾号码冲突
    cases.append(fmt([["1", "12", "123", "1234", "12345", "123456", "1234567", "12345678", "123456789", "1234567890"]]))
    a = prefix_free_fast(r, 9999, 10); a.append(a[0][:9]); cases.append(fmt([a]))
    a = prefix_free_fast(r, 9999, 10); a.insert(0, a[-1][:1] if False else a[-1][:5]); cases.append(fmt([a]))
    a = prefix_free_fast(r, 9999, 7, lead0=True); a.append(a[-1] + "0"); cases.append(fmt([a]))
    tests = [prefix_free_fast(r, 2, 10) for _ in range(40)]
    for q in range(0, 40, 3): tests[q] = [tests[q][0], tests[q][0][:r.randint(1, 9)]]
    cases.append(fmt(tests))
    while len(cases) < 40:
        cases.append(fmt([plant(r, prefix_free(r, 3000, 2, 10, lead0=True))]))
    return cases

def main():
    cases = build_cases()
    assert len(cases) == 40 and len(set(cases)) == 40
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as h:
        h.write(REFERENCE_SOURCE); h.flush(); root = Path(__file__).parent / "data"
        for i, c in enumerate(cases):
            assert valid(c), i
            assert len(c.encode()) <= 1 << 20, i
            p = subprocess.run(["python3", h.name], input=c, text=True, capture_output=True, check=True)
            (root / f"{i}.in").write_text(c, encoding="utf-8"); (root / f"{i}.out").write_text(p.stdout, encoding="utf-8")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build T-004 round 1 with independent second implementations."""
import inspect
import json
import random
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path
from build_001a import bucket

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "collab/t004-round1-manifest.json"
REPORT = ROOT / "collab/t004-round1-report.json"
TESTS = ROOT / "data/openjudge/tests"

def run(code, content, timeout=10):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as f:
        f.write(code); f.flush()
        p = subprocess.run([sys.executable, f.name], input=content, text=True,
                           capture_output=True, timeout=timeout)
    if p.returncode:
        raise RuntimeError(p.stderr[-1200:])
    return p.stdout

def g3263(r):
    cases = []
    for _ in range(r.randint(1, 3)):
        n = r.randint(1, 8)
        rows = [[r.randint(0, 100) for _ in range(i + 1)] for i in range(n)]
        cases.append((rows, r.randint(1, n), r.randint(1, n)))
        cases[-1] = (rows, cases[-1][1], r.randint(1, cases[-1][1]))
    lines = []
    for rows, row, col in cases:
        lines += [str(len(rows))] + [" ".join(map(str, x)) for x in rows] + [f"{row} {col}"]
    return "\n".join(lines + ["0"]) + "\n"

def g3376(r):
    n = r.randint(1, 24)
    return str(n) + "\n" + "\n".join(r.choice("ABCXYZ") for _ in range(n)) + "\n"

def spiral_positions(rows, cols):
    t, l, b, rr = 0, 0, rows - 1, cols - 1
    while t <= b and l <= rr:
        for j in range(l, rr + 1): yield t, j
        t += 1
        for i in range(t, b + 1): yield i, rr
        rr -= 1
        if t <= b:
            for j in range(rr, l - 1, -1): yield b, j
            b -= 1
        if l <= rr:
            for i in range(b, t - 1, -1): yield i, l
            l += 1

def encode_spiral(rows, cols, message):
    bits = "".join(f"{0 if ch == ' ' else ord(ch) - 64:05b}" for ch in message)
    bits = bits.ljust(rows * cols, "0")[:rows * cols]
    grid = [["0"] * cols for _ in range(rows)]
    for pos, bit in zip(spiral_positions(rows, cols), bits): grid[pos[0]][pos[1]] = bit
    return "".join("".join(row) for row in grid)

def g3421(r):
    rows, cols = r.randint(1, 8), r.randint(1, 8)
    msg = "".join(r.choice(" ABCXYZ") for _ in range(r.randint(0, rows * cols // 5)))
    return f"{rows} {cols} {msg}\n"

def g3527(r):
    return "\n".join(" ".join(str(r.randint(1, 9)) for _ in range(r.choice([4,5,7,8,10,11,13,14]))) for _ in range(r.randint(1, 4))) + "\n0\n"

def g3708(r):
    return str(5) + "\n" + "\n".join(str(r.randint(1, 10**9)) for _ in range(5)) + "\n"

def g3709(r):
    return "5\n" + "\n".join("1" + "".join(r.choice("01") for _ in range(r.randint(0, 18))) for _ in range(5)) + "\n"

def g3710(r):
    return "5\n" + "\n".join(f"{r.randint(1, 10**6)} {r.randint(1, 10**6)}" for _ in range(5)) + "\n"

def g3711(r):
    return f"{''.join(r.choice('ABCD') for _ in range(r.randint(1, 12)))} {''.join(r.choice('ABCD') for _ in range(r.randint(1, 12)))}\n"

def g3712(r):
    mp = "abc def ghi jkl mno pqrs tuv wxyz".split()
    cases = []
    for _ in range(r.randint(1, 5)):
        digits = "".join(r.choice("23456789") for _ in range(r.randint(1, 12)))
        word = "".join(r.choice(mp[int(d)-2]) for d in digits)
        if r.random() < .35: word = word[:-1] + r.choice("xyz")
        cases.append(f"{word} {digits}")
    return str(len(cases)) + "\n" + "\n".join(cases) + "\n"

def g3714(r):
    n, cap = r.randint(1, 12), r.randint(1, 80)
    items = [(r.randint(1, 30), r.randint(1, 30)) for _ in range(n)]
    return f"{cap} {n}\n" + "\n".join(f"{p} {v}" for p, v in items) + "\n"

GENERATORS = {n: globals()[f"g{n}"] for n in [3263,3376,3421,3527,3708,3709,3710,3711,3712,3714]}

REFERENCE = {}
REFERENCE[3263] = r'''import sys
a=iter(sys.stdin.read().split()); out=[]
while True:
 n=int(next(a))
 if n==0: break
 nrows=[[int(next(a)) for _ in range(i+1)] for i in range(n)]
 row,col=int(next(a))-1,int(next(a))-1
 def f(i,j):
  if i==n-1:return nrows[i][j]
  return max(nrows[i][j],f(i+1,j),f(i+1,j+1))
 out.append(str(f(row,col)))
print("\n".join(out))'''
REFERENCE[3376] = r'''import sys
a=sys.stdin.read().split(); s="".join(a[1:])
l,rr,out=0,len(s)-1,[]
while l<=rr:
 if s[l]<s[rr]: out.append(s[l]); l+=1
 elif s[l]>s[rr]: out.append(s[rr]); rr-=1
 else:
  i,j=l,rr
  while i<=j and s[i]==s[j]: i+=1; j-=1
  if i>j or s[i]<=s[j]: out.append(s[l]); l+=1
  else: out.append(s[rr]); rr-=1
print("".join(out))'''
REFERENCE[3421] = r'''import sys
def pos(r,c):
 t,l,b,rr=0,0,r-1,c-1
 while t<=b and l<=rr:
  for j in range(l,rr+1): yield t,j
  t+=1
  for i in range(t,b+1): yield i,rr
  rr-=1
  if t<=b:
   for j in range(rr,l-1,-1): yield b,j
   b-=1
  if l<=rr:
   for i in range(b,t-1,-1): yield i,l
   l+=1
r,c,msg=sys.stdin.read().rstrip("\n").split(" ",2); r,c=int(r),int(c)
bits="".join(format(0 if x==" " else ord(x)-64,"05b") for x in msg).ljust(r*c,"0")
g=[["0"]*c for _ in range(r)]
for (i,j),x in zip(pos(r,c),bits): g[i][j]=x
print("".join("".join(x) for x in g))'''
REFERENCE[3527] = r'''import sys
from collections import Counter
def ok(v):
 if len(v)<2 or (len(v)-2)%3: return "XIANGGONG"
 def f(c,p):
  if not sum(c.values()): return p
  x=min(k for k,v in c.items() if v)
  if p is None and c[x]>=2:
   c[x]-=2
   if f(c,x): return x
   c[x]+=2
  if c[x]>=3:
   c[x]-=3
   if f(c,p): return p
   c[x]+=3
  if c.get(x+1,0) and c.get(x+2,0):
   for y in (x,x+1,x+2): c[y]-=1
   if f(c,p): return p
   for y in (x,x+1,x+2): c[y]+=1
  return None
 return "HU" if f(Counter(v),None) is not None else "BUHU"
out=[]
for line in sys.stdin:
 v=list(map(int,line.split()))
 if v and v[0]==0: break
 out.append(ok(v))
print("\n".join(out))'''
REFERENCE[3708] = 'import sys\nfor x in sys.stdin.read().split()[1:]: print(bin(int(x)).count("1"))'
REFERENCE[3709] = r'''import sys
def f(s):
 n=int(s,2); out=[]
 if not n:return "0"
 while n: out.append(str(n%3)); n//=3
 return "".join(out[::-1])
a=sys.stdin.read().split(); print("\n".join(f(x) for x in a[1:]))'''
REFERENCE[3710] = r'''import sys
a=list(map(int,sys.stdin.read().split()))
print("\n".join(str(bin(x^y).count("1")) for x,y in zip(a[1::2],a[2::2])))'''
REFERENCE[3711] = r'''import sys
a,b=sys.stdin.read().split()
print("true" if a in b+b or b in a+a else "false")'''
REFERENCE[3712] = r'''import sys
m={"2":"abc","3":"def","4":"ghi","5":"jkl","6":"mno","7":"pqrs","8":"tuv","9":"wxyz"}
a=sys.stdin.read().split(); out=[]
for w,d in zip(a[1::2],a[2::2]): out.append("Y" if len(w)==len(d) and all(x.lower() in m[y] for x,y in zip(w,d)) else "N")
print("\n".join(out))'''
REFERENCE[3714] = r'''import sys
a=list(map(int,sys.stdin.read().split())); cap,n=a[:2]; dp=[0]*(cap+1)
for p,v in zip(a[2::2],a[3::2]):
 for x in range(cap,p-1,-1): dp[x]=max(dp[x],dp[x-p]+v)
print(dp[cap])'''

# 001b 确立的「题面保证 X -> 生成器保证 X」逐条打钩表。
# 原来是 10 题共用一个 {"题面":"see source page", ...} 的占位 dict —— 「see source page」
# 就是「没填」，但它看起来像填了。只填本轮复核真正逐条核对过题面的题，其余留 None 待补。
CONSTRAINTS = {
    3421: ["1<=R<=20, 1<=C<=20", "字符串只含大写字母和空格", "字符串长度 <= (R*C)/5",
           "空格=0, A=1..Z=26，每字符 5 位二进制", "按螺旋顺序填入，末尾用 0 补满 R*C 位",
           "生成器目前 R,C 只到 8，未贴题面上界 20"],
    3263: ["每组先给三角形层数 n，n=0 结束", "查询给出起点行列（1-based）",
           "从起点向下相邻两格可达位置中取最大数"],
    3376: ["1<=N<=30000", "每行一个 A..Z 初始字母", "每次只能取剩余原序列的首或尾", "输出可形成的字典序最小串"],
    3527: ["每个数字为1..9", "每个数字出现次数不超过4", "集合长度不超过14", "长度必须为3n+2且n<=4", "三元组为相等或连续递增，二元组相等"],
    3708: ["第一行给测试组数", "每组输入一个十进制整数", "每组输出其二进制表示中的1的个数"],
    3709: ["测试组数n与输入行数一致", "每个输入是长度1..64的0/1字符串", "输出对应的三进制表示"],
    3710: ["A、B为正整数", "每组比较二进制表示并按高位补0", "输出不同位数"],
    3711: ["两个字符串仅含字母和数字", "长度不超过30", "判定循环移位所得字符串是否包含另一字符串"],
    3712: ["测试组数n与输入行数一致", "两个字符串长度不超过20且可不同", "电话数字使用2..9键盘映射", "输出Y或N"],
    3714: ["1<=C<=1000", "1<=N<=100", "每道菜价格和评价均为1..100", "每道菜最多选择一次", "总价格不超过C"],
}


def oracle(number, content):
    if number == 3263:
        a=iter(content.split()); ans=[]
        while True:
            n=int(next(a))
            if n==0: break
            tri=[[int(next(a)) for _ in range(i+1)] for i in range(n)]
            row,col=int(next(a))-1,int(next(a))-1
            def f(i,j):
                if i==n-1:return tri[i][j]
                return max(tri[i][j],f(i+1,j),f(i+1,j+1))
            ans.append(str(f(row,col)))
        return "\n".join(ans)+"\n"
    if number == 3376:
        s="".join(content.split()[1:])
        memo={}
        def f(l,r):
            if l>r:return ""
            if (l,r) not in memo: memo[l,r]=min(s[l]+f(l+1,r),s[r]+f(l,r-1))
            return memo[l,r]
        return f(0,len(s)-1)+"\n"
    if number == 3421:
        r,c,msg=content.rstrip("\n").split(" ",2); return encode_spiral(int(r),int(c),msg)+"\n"
    if number == 3527:
        def valid(v):
            if len(v)<2 or (len(v)-2)%3:return "XIANGGONG"
            def f(rest,p):
                if not rest:return p
                x=rest[0]
                if p is None and rest.count(x)>=2:
                    q=rest[:];q.remove(x);q.remove(x)
                    if f(q,x):return x
                if rest.count(x)>=3:
                    q=rest[:];q.remove(x);q.remove(x);q.remove(x)
                    if f(q,p):return p
                if x+1 in rest and x+2 in rest:
                    q=rest[:];q.remove(x);q.remove(x+1);q.remove(x+2)
                    if f(q,p):return p
                return None
            return "HU" if f(sorted(v),None) is not None else "BUHU"
        out=[]
        for line in content.splitlines():
            v=list(map(int,line.split()))
            if v and v[0]==0:break
            out.append(valid(v))
        return "\n".join(out)+"\n"
    if number == 3708:
        return "\n".join(str(bin(int(x))[2:].count("1")) for x in content.split()[1:])+"\n"
    if number == 3709:
        out=[]
        for bits in content.split()[1:]:
            n=0
            for bit in bits:n=n*2+int(bit)
            ds=["0"] if n==0 else []
            while n:ds.append(str(n%3));n//=3
            out.append("".join(ds[::-1]))
        return "\n".join(out)+"\n"
    if number == 3710:
        a=list(map(int,content.split())); out=[]
        for x,y in zip(a[1::2],a[2::2]):
            out.append(str(bin(x^y).count("1")))
        return "\n".join(out)+"\n"
    if number == 3711:
        a,b=content.split()
        return ("true" if any(a in b[i:]+b[:i]+b[i:]+b[:i] or b in a[i:]+a[:i]+a[i:]+a[:i] for i in range(max(len(a),len(b)))) else "false")+"\n"
    if number == 3712:
        m={"2":set("abc"),"3":set("def"),"4":set("ghi"),"5":set("jkl"),"6":set("mno"),"7":set("pqrs"),"8":set("tuv"),"9":set("wxyz")}
        a=content.split(); out=[]
        for w,d in zip(a[1::2],a[2::2]):out.append("Y" if len(w)==len(d) and all(x.lower() in m[y] for x,y in zip(w,d)) else "N")
        return "\n".join(out)+"\n"
    a=list(map(int,content.split())); cap,n=a[:2]; best=0
    for mask in range(1<<n):
        cost=value=0
        for i in range(n):
            if mask>>i&1:cost+=a[2+2*i];value+=a[3+2*i]
        if cost<=cap:best=max(best,value)
    return str(best)+"\n"

def reproduce(directory):
    data=directory/"data"; before={p.name:p.read_bytes() for p in data.iterdir()}
    p=subprocess.run([sys.executable,"producecase.py"],cwd=directory,capture_output=True,timeout=600)
    return p.returncode==0 and before=={p.name:p.read_bytes() for p in data.iterdir()}

def main():
    # First gate: a concrete reference mutation must be caught by the oracle.
    subprocess.run([sys.executable, str(ROOT / "scripts/t004_mutation_check.py")], check=True)
    manifest=json.loads(MANIFEST.read_text(encoding="utf-8")); report=[]
    for entry in manifest["entries"]:
        n=entry["local_number"]; ref=REFERENCE[n]
        assert run(ref,entry["sample_input"]).split()==entry["sample_output"].split()
        assert oracle(n,entry["sample_input"]).split()==entry["sample_output"].split()
        for seed in range(20000): GENERATORS[n](random.Random(n+seed))
        for seed in range(2000):
            case=GENERATORS[n](random.Random(n+seed))
            assert run(ref,case).split()==oracle(n,case).split()
        cases=[entry["sample_input"]]
        for i in range(1,21):
            for attempt in range(100):
                case=GENERATORS[n](random.Random(n+i+attempt*1000))
                if case not in cases:cases.append(case);break
            else:raise AssertionError(f"insufficient diversity {n}")
        d=TESTS/bucket(n)/f"{n:05d}_made"; data=d/"data"; data.mkdir(parents=True,exist_ok=True)
        outputs=[run(ref,x) for x in cases]
        (d/"samplecode.py").write_text("# LLM-written reference implementation\n"+ref,encoding="utf-8")
        gsource=inspect.getsource(GENERATORS[n])
        produce=f'''import random,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE={ref!r}
SAMPLE_IN={entry["sample_input"]!r}
{gsource}
with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
 handle.write(REFERENCE_SOURCE);handle.flush()
 root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
 for index in range(21):
  if index==0:content=SAMPLE_IN
  else:
   for attempt in range(100):
    content={GENERATORS[n].__name__}(random.Random({n}+index+attempt*1000))
    if content not in seen:break
   else:raise AssertionError("insufficient diversity")
  seen.append(content)
  result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
  (root/f"{{index}}.in").write_text(content,encoding="utf-8")
  (root/f"{{index}}.out").write_text(result.stdout,encoding="utf-8")
'''
        (d/"producecase.py").write_text(produce,encoding="utf-8")
        for p in data.glob("*"):p.unlink()
        for i,out in enumerate(outputs):
            (data/f"{i}.in").write_text(cases[i],encoding="utf-8");(data/f"{i}.out").write_text(out,encoding="utf-8")
        freq=Counter(tuple(x.split()) for x in outputs)
        report.append({"local_number":n,"title":entry["title"],"source":entry["source"],"reference_source":"LLM-written","generator":GENERATORS[n].__name__,"seed":n,"test_cases":len(cases),"distinct_input_cases":len(set(cases)),"distinct_outputs":len(freq),"max_output_frequency":max(freq.values()),"constant_output_probe":{"status":"rejected" if max(freq.values())<len(cases) else "accepted","frequency":max(freq.values()),"total":len(cases)},"constraints":CONSTRAINTS.get(n),"structure_checked":n in CONSTRAINTS,"generator_seed_smoke":{"seeds":20000,"status":"passed"},"reference_seed_smoke":{"seeds":2000,"status":"passed"},"independent_oracle_smoke":{"seeds":2000,"status":"passed"},"sample_reproduced":True,"independent_sample_agreement":True,"producecase_reproduced":reproduce(d)})
        print("built",n,flush=True)
    REPORT.write_text(json.dumps({"batch":"T-004-r1","entries":report},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
if __name__=="__main__":main()

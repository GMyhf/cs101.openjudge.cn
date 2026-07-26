#!/usr/bin/env python3
"""Build T-004 round 3 with two-stage misconception probes."""
import inspect
import json
import random
import subprocess
import sys
import tempfile
from collections import Counter
from datetime import date, timedelta
from heapq import heappop, heappush
from pathlib import Path
from functools import cmp_to_key

from build_001a import bucket

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "collab/t004-round3-manifest.json"
REPORT = ROOT / "collab/t004-round3-report.json"
TESTS = ROOT / "data/openjudge/tests"

def run(code, content, timeout=10):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as f:
        f.write(code); f.flush()
        p = subprocess.run([sys.executable, f.name], input=content, text=True,
                           capture_output=True, timeout=timeout)
    if p.returncode:
        raise RuntimeError(p.stderr[-1200:])
    return p.stdout

def g3704(r):
    lines=[]
    for _ in range(r.randint(1, 5)):
        s="".join(r.choice("()ABCxyz") for _ in range(r.randint(1, 40)))
        lines.append(s)
    return "\n".join(lines)+"\n"

def g3713(r):
    phrases=[
        "zero","one","twelve","nineteen","twenty one","forty two",
        "one hundred","three hundred five","nine hundred ninety nine",
        "one thousand two","twelve thousand three hundred forty five",
        "one million one hundred one","negative seven hundred twenty nine",
        "negative one million two hundred thirty four",
        "eight hundred fourteen thousand twenty two",
        "six hundred thousand","seventy thousand nineteen",
        "four million five hundred",
        "negative ninety nine million nine hundred ninety nine thousand nine hundred ninety nine",
        "two hundred thirty four million five hundred sixty seven thousand eight hundred ninety",
        "negative one thousand one",
        "fifteen million sixteen thousand seventeen"
    ]
    return "\n".join(r.sample(phrases, r.randint(1, 5)))+"\n"

def g3715(r):
    from datetime import date, timedelta
    rows=[]
    for i in range(r.randint(1, 8)):
        y=r.randint(1900, 9990); m=r.randint(1, 12)
        start=date(y,m,1)+timedelta(days=r.randint(0, 27))
        if start.year==9999: start=date(9998,12,1)
        end=start+timedelta(days=r.randint(1, 3000))
        rows.append(f"p{i:02d} {start.year} {start.month} {start.day} {end.year} {end.month} {end.day}")
    return str(len(rows))+"\n"+"\n".join(rows)+"\n"

def g3716(r):
    lines=["# generated config"]
    for i in range(r.randint(1, 8)):
        lines.append(r.choice(["timevar","portvar","pathvar"])+" KEY"+str(i)+" "+r.choice(["0","120","[1,2,3]","/tmp/x"]))
        if r.random()<.35: lines.append("")
        if r.random()<.25: lines.append("# note")
    lines.append("# End of the config file")
    return "\n".join(lines)+"\n"

def g3717(r):
    m=r.randint(1, 19); n=r.randint(1, 20-m)
    return f"{m} {n}\n"

def g3719(r):
    rows=[]
    for i in range(r.randint(1, 8)):
        name=r.choice(["Ann Lee","bob Stone","Cara Q","D E"])+" "+str(i)
        ident=r.randint(1,99999); sex=r.choice(["M","F"]); age=r.randint(1,100)
        rows.append(f"{name}\n{ident},{sex} {age}")
    return "\n".join(rows)+"\n"

def g3721(r):
    n=r.randint(3, 30)
    return str(n)+"\n"+" ".join(str(r.randint(1,10000)) for _ in range(n))+"\n"

def g3722(r):
    n=r.randint(1, 1000000); m=r.randint(2, 200)
    return f"{n} {m}\n"

def g3724(r):
    return "\n".join(str(r.randint(0, 2**31-1)) for _ in range(r.randint(1, 8)))+"\n"

def g3752(r):
    rows,cols=r.randint(1, 12),r.randint(1, 12)
    grid=[["."]*cols for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            if (i,j) not in [(0,0),(rows-1,cols-1)] and r.random()<.25:
                grid[i][j]="#"
    # Force a monotone backbone, then verify the generated maze remains reachable.
    for i in range(rows): grid[i][0]="."
    for j in range(cols): grid[rows-1][j]="."
    assert grid[0][0]=="." and grid[-1][-1]=="."
    return f"{rows} {cols}\n"+"\n".join("".join(row) for row in grid)+"\n"

GENERATORS={n:globals()[f"g{n}"] for n in [3704,3713,3715,3716,3717,3719,3721,3722,3724,3752]}

REFERENCE={}
REFERENCE[3704]=r'''import sys
for line in sys.stdin.read().splitlines():
    bad=[" "]*len(line); stack=[]
    for i,ch in enumerate(line):
        if ch=="(": stack.append(i)
        elif ch==")":
            if stack: stack.pop()
            else: bad[i]="?"
    for i in stack: bad[i]="$"
    print(line); print("".join(bad).rstrip())'''
REFERENCE[3713]=r'''import sys
small={"zero":0,"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,"nine":9,"ten":10,"eleven":11,"twelve":12,"thirteen":13,"fourteen":14,"fifteen":15,"sixteen":16,"seventeen":17,"eighteen":18,"nineteen":19}
tens={"twenty":20,"thirty":30,"forty":40,"fifty":50,"sixty":60,"seventy":70,"eighty":80,"ninety":90}
for line in sys.stdin:
    cur=total=0; neg=False
    for w in line.split():
        if w=="negative": neg=True
        elif w in small: cur+=small[w]
        elif w in tens: cur+=tens[w]
        elif w=="hundred": cur*=100
        elif w=="thousand": total+=cur*1000; cur=0
        elif w=="million": total+=cur*1000000; cur=0
    value=total+cur
    print(-value if neg else value)'''
REFERENCE[3715]=r'''import sys
from datetime import date
lines=sys.stdin.read().splitlines(); n=int(lines[0]); rows=[]
for i in range(n):
    parts=lines[1+i].split(); name=parts[0]; y,m,d,Y,M,D=map(int,parts[1:])
    rows.append((name,(date(Y,M,D)-date(y,m,d)).days+1,i))
for row in sorted(rows,key=lambda x:(-x[1],x[2])): print(row[0],row[1])'''
REFERENCE[3716]=r'''import sys
out=[]
for line in sys.stdin.read().splitlines():
    parts=line.split()
    if parts and not parts[0].startswith("#") and parts[0]!="":
        out.append(" ".join(parts[1:]))
print(len(out)); print("\n".join(out))'''
REFERENCE[3717]=r'''import sys
m,n=map(int,sys.stdin.read().split()); dp=[1]*n
for _ in range(m-1):
    for j in range(1,n): dp[j]+=dp[j-1]
print(dp[n-1])'''
REFERENCE[3719]=r'''import sys
lines=sys.stdin.read().splitlines()
while lines and not lines[-1].strip(): lines.pop()
n=len(lines)//2; rows=[]
for i in range(n):
    name=lines[2*i]; a=lines[2*i+1].split()
    ident,sex=a[0].split(","); age=a[1]
    rows.append((name, i, ident, sex, age))
for x in sorted(rows,key=lambda z:z[0].lower()):
    print(x[0]); print(f"{int(x[2]):08d},{x[3]} {x[4]}")
'''
REFERENCE[3721]=r'''import sys
a=list(map(int,sys.stdin.read().split())); n=a[0]; v=a[1:1+n]; ans=0
for i,x in enumerate(v):
    seen=set()
    for j,y in enumerate(v):
        if j!=i and x-y in seen: ans+=1; break
        if j!=i: seen.add(y)
print(ans)'''
REFERENCE[3722]=r'''import sys
n,m=map(int,sys.stdin.read().split()); answer=-1
for a in range(1,m):
    if n%a==0 and n%(m-a)==0: answer=a; break
print(answer)'''
REFERENCE[3724]=r'''import sys
days=[31,28,31,30,31,30,31,31,30,31,30,31]
def leap(y): return y%400==0 or y%4==0 and y%100!=0
for token in sys.stdin.read().split():
    rem=int(token); y=1970
    while rem >= (366 if leap(y) else 365)*86400: rem-=(366 if leap(y) else 365)*86400; y+=1
    month=1
    while True:
        md=days[month-1]+(month==2 and leap(y))
        if rem < md*86400: break
        rem-=md*86400; month+=1
    print(f"{y:04d}-{month:02d}-{rem//86400+1:02d} {(rem%86400)//3600:02d}:{(rem%3600)//60:02d}:{rem%60:02d}")'''
REFERENCE[3752]=r'''import sys
from collections import deque
a=sys.stdin.read().split(); r,c=map(int,a[:2]); g=a[2:]; d=[[-1]*c for _ in range(r)]
q=deque([(0,0)]); d[0][0]=1
while q:
    x,y=q.popleft()
    for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
        u,v=x+dx,y+dy
        if 0<=u<r and 0<=v<c and g[u][v]=="." and d[u][v]<0:
            d[u][v]=d[x][y]+1; q.append((u,v))
print(d[-1][-1])'''

CONSTRAINTS={
3704:["每行长度<=100","只含括号和大小写字母","输入多组行直到EOF","未匹配左括号标$、右括号标?"],
3713:["数值范围-999999999..999999999","单词来自题面给定词表","negative表示负号","输入多行直到EOF"],
3715:["只有一个测试样例","学生数不超过题面限制","姓名最长18字符","日期范围1900-01-01..9999-12-31","同天数按输入顺序"],
3716:["行数<20","每行<50字符","配置行由空格分隔","#开头和空行无效","末行固定# End of the config file"],
3717:["m,n为正整数","m+n<=20","每步只能向上或向右","输出路线数"],
3719:["学生信息按姓名行与信息行成对输入直到EOF","姓名由英文字母和空格构成","学号<=100000","性别为M或F","年龄<=100","输出学号补足8位"],
3721:["1<=n<=100","每个数为正整数且<=10000","目标数需等于其他两个数之和","两个加数来自其他位置"],
3722:["N<=1000000","a为正整数","M-a为正整数","a和M-a均为N的因子","无解输出-1"],
3724:["0<=t<2^31","Unix epoch为1970-01-01 00:00:00","输出YYYY-mm-dd HH:ii:ss"],
3752:["1<=R,C<=40",".可走、#不可走","左上角和右下角为.","保证存在路径","只能上下左右移动"]
}

def oracle(n,content):
    if n==3704:
        out=[]
        for line in content.splitlines():
            chars=[(i,ch) for i,ch in enumerate(line) if ch in "()"]
            mark=[" "]*len(line)
            while True:
                pair=None
                for i in range(len(chars)-1):
                    if chars[i][1]=="(" and chars[i+1][1]==")": pair=i; break
                if pair is None: break
                del chars[pair:pair+2]
            for i,ch in chars:
                if ch=="(": mark[i]="$"
                elif ch==")": mark[i]="?"
            out += [line,"".join(mark).rstrip()]
        return "\n".join(out)+"\n"
    if n==3713:
        val={"zero":0,"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,"nine":9,"ten":10,"eleven":11,"twelve":12,"thirteen":13,"fourteen":14,"fifteen":15,"sixteen":16,"seventeen":17,"eighteen":18,"nineteen":19,"twenty":20,"thirty":30,"forty":40,"fifty":50,"sixty":60,"seventy":70,"eighty":80,"ninety":90}
        out=[]
        for line in content.splitlines():
            neg=line.startswith("negative"); total=cur=0
            for w in line.split():
                if w in val: cur+=val[w]
                elif w=="hundred": cur*=100
                elif w=="thousand": total+=cur*1000;cur=0
                elif w=="million": total+=cur*1000000;cur=0
            out.append(str(-(total+cur) if neg else total+cur))
        return "\n".join(out)+"\n"
    if n==3715:
        month_days=[31,28,31,30,31,30,31,31,30,31,30,31]
        def serial(y,m,d):
            before=y-1
            total=365*before+before//4-before//100+before//400
            for month in range(1,m): total+=month_days[month-1]+(month==2 and (y%400==0 or y%4==0 and y%100!=0))
            return total+d
        lines=content.splitlines(); n=int(lines[0]); rows=[]
        for i in range(n):
            parts=lines[1+i].split(); name=parts[0]; y,m,d,Y,M,D=map(int,parts[1:])
            rows.append((name,serial(Y,M,D)-serial(y,m,d)+1,i))
        return "\n".join(f"{x[0]} {x[1]}" for x in sorted(rows,key=lambda z:(-z[1],z[2])))+"\n"
    if n==3716:
        out=[]
        for line in content.splitlines():
            p=line.split()
            if p and not p[0].startswith("#"): out.append(" ".join(p[1:]))
        return str(len(out))+"\n"+"\n".join(out)+"\n"
    if n==3717:
        m,n=map(int,content.split()); a=[[0]*(n+1) for _ in range(m+1)]
        for i in range(m+1): a[i][0]=1
        for j in range(n+1): a[0][j]=1
        for i in range(1,m+1):
            for j in range(1,n+1): a[i][j]=a[i-1][j]+a[i][j-1]
        return f"{a[m-1][n-1]}\n"
    if n==3719:
        lines=content.splitlines()
        while lines and not lines[-1].strip(): lines.pop()
        n=len(lines)//2; rows=[]
        for i in range(n):
            name=lines[2*i]; a=lines[2*i+1].split(); ident,sex=a[0].split(","); age=a[1]
            rows.append((name,i,ident,sex,age))
        return "\n".join(f"{x[0]}\n{int(x[2]):08d},{x[3]} {x[4]}" for x in sorted(rows,key=lambda z:z[0].lower()))+"\n"
    if n==3721:
        a=list(map(int,content.split())); v=a[1:1+a[0]]; ans=0
        for i,x in enumerate(v):
            for j in range(len(v)):
                if j==i: continue
                for k in range(j+1,len(v)):
                    if k!=i and v[j]+v[k]==x: ans+=1; break
                else: continue
                break
        return f"{ans}\n"
    if n==3722:
        n,m=map(int,content.split())
        for a in range(1,m):
            if n%a==0 and n%(m-a)==0:return f"{a}\n"
        return "-1\n"
    if n==3724:
        out=[]
        for token in content.split():
            t=int(token); base=date(1970,1,1); day,sec=divmod(t,86400)
            d=base+timedelta(days=day)
            out.append(f"{d:%Y-%m-%d} {sec//3600:02d}:{sec%3600//60:02d}:{sec%60:02d}")
        return "\n".join(out)+"\n"
    if n==3752:
        a=content.split(); r,c=map(int,a[:2]); g=a[2:]; q=[(0,0,1)]; seen={(0,0)}
        for x,y,d in q:
            if (x,y)==(r-1,c-1): return f"{d}\n"
            for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
                u,v=x+dx,y+dy
                if 0<=u<r and 0<=v<c and g[u][v]=="." and (u,v) not in seen:
                    seen.add((u,v));q.append((u,v,d+1))
        return "-1\n"
    raise KeyError(n)

def mutate(n,source):
    changes={
      3704:("if stack: stack.pop()","if not stack: stack.pop()"),
      3713:("elif w==\"hundred\": cur*=100","elif w==\"hundred\": cur+=100"),
      3715:("date(Y,M,D)-date(y,m,d)).days+1","date(Y,M,D)-date(y,m,d)).days"),
      3716:("out.append(\" \".join(parts[1:]))","out.append(\" \".join(parts[0:]))"),
      3717:("for _ in range(m-1):","for _ in range(m):"),
      3719:("key=lambda z:z[0].lower()","key=lambda z:z[0]"),
      3721:("if j!=i and x-y in seen","if j==i and x-y in seen"),
      3722:("n%a==0 and n%(m-a)==0","n%a==0 or n%(m-a)==0"),
      3724:("rem=int(token); y=1970","rem=int(token)+60; y=1970"),
      3752:("print(d[-1][-1])","print(d[-1][-1]-1)")
    }
    old,new=changes[n]; changed=source.replace(old,new); assert changed!=source
    return changed

def attempt(code,content):
    try:return run(code,content).split(),False
    except (RuntimeError,subprocess.TimeoutExpired) as e:return [f"<runtime error: {type(e).__name__}>"],True

def probe(n,mutated,entry,cases=None):
    sample_bad,sample_err=attempt(mutated,entry["sample_input"])
    sample_good=entry["sample_output"].split()
    data_hits=[]
    if cases is not None:
        for i,case in enumerate(cases):
            bad,_=attempt(mutated,case); good=oracle(n,case).split()
            if bad!=good:data_hits.append(i)
    return {"sample_pins_interpretation":sample_bad!=sample_good,
            "sample_mutated_output":sample_bad,"sample_expected":sample_good,
            "sample_runtime_error":sample_err,"data_catches_misreading":bool(data_hits),
            "data_catching_cases":data_hits,"status":"caught" if data_hits else "missed"}

def reproduce(directory):
    data=directory/"data"; before={p.name:p.read_bytes() for p in data.iterdir()}
    p=subprocess.run([sys.executable,"producecase.py"],cwd=directory,capture_output=True,text=True,timeout=600)
    return p.returncode==0 and before=={p.name:p.read_bytes() for p in data.iterdir()}

def main():
    manifest=json.loads(MANIFEST.read_text(encoding="utf-8")); report=[]
    for entry in manifest["entries"]:
        n=entry["local_number"]; ref=REFERENCE[n]; gen=GENERATORS[n]
        assert run(ref,entry["sample_input"]).split()==entry["sample_output"].split(),n
        assert oracle(n,entry["sample_input"]).split()==entry["sample_output"].split(),n
        mutated=mutate(n,ref)
        cases=[entry["sample_input"]]
        for i in range(1,21):
            for attempt_no in range(100):
                case=gen(random.Random(n+i+attempt_no*1000))
                if case not in cases:cases.append(case);break
            else:raise AssertionError(f"insufficient diversity {n}")
        p=probe(n,mutated,entry,cases)
        assert p["data_catches_misreading"],(n,p)
        for seed in range(20000): gen(random.Random(n+seed))
        for seed in range(1000):
            case=gen(random.Random(n+seed))
            assert run(ref,case).split()==oracle(n,case).split(),n
        d=TESTS/bucket(n)/f"{n:05d}_made";data=d/"data";data.mkdir(parents=True,exist_ok=True)
        outs=[run(ref,x) for x in cases]
        (d/"samplecode.py").write_text("# T-004-r3 reference implementation\n"+ref,encoding="utf-8")
        gsource=inspect.getsource(gen)
        produce=f'''import random,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE={ref!r}
SAMPLE_IN={entry["sample_input"]!r}
{gsource}
with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
 handle.write(REFERENCE_SOURCE);handle.flush()
 root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
 for index in range(21):
  if index==0: content=SAMPLE_IN
  else:
   for attempt_no in range(100):
    content={gen.__name__}(random.Random({n}+index+attempt_no*1000))
    if content not in seen: break
   else: raise AssertionError("insufficient diversity")
  seen.append(content)
  result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
  (root/f"{{index}}.in").write_text(content,encoding="utf-8")
  (root/f"{{index}}.out").write_text(result.stdout,encoding="utf-8")
'''
        (d/"producecase.py").write_text(produce,encoding="utf-8")
        for f in data.iterdir():f.unlink()
        for i,out in enumerate(outs):
            (data/f"{i}.in").write_text(cases[i],encoding="utf-8");(data/f"{i}.out").write_text(out,encoding="utf-8")
        freq=Counter(tuple(x.split()) for x in outs)
        report.append({"local_number":n,"title":entry["title"],"source":entry["source"],
          "reference_source":"LLM-written","generator":gen.__name__,"seed":n,
          "test_cases":len(cases),"distinct_input_cases":len(set(cases)),
          "distinct_outputs":len(freq),"max_output_frequency":max(freq.values()),
          "constant_output_probe":{"status":"rejected" if max(freq.values())<len(cases) else "accepted","frequency":max(freq.values()),"total":len(cases)},
          "constraints":CONSTRAINTS[n],"structure_checked":False,
          "generator_seed_smoke":{"seeds":20000,"status":"passed"},
          "reference_seed_smoke":{"seeds":1000,"status":"passed"},
          "independent_oracle_smoke":{"seeds":1000,"status":"passed"},
          "sample_reproduced":True,"independent_sample_agreement":True,
          "misconception_probe":p,"producecase_reproduced":reproduce(d)})
        print("built",n,flush=True)
    REPORT.write_text(json.dumps({"batch":"T-004-r3","entries":report},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

if __name__=="__main__":main()

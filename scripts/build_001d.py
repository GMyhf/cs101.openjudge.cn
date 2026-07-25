#!/usr/bin/env python3
"""Build the T-002-001d data batch."""
import json, random, re, subprocess, sys, tempfile
from pathlib import Path
from build_001a import bucket, fence_blocks, locate_source
from build_001b import first_sample

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "collab/t002-batch-001-manifest.json"
REPORT = ROOT / "collab/t002-001d-report.json"
TESTS = ROOT / "data/openjudge/tests"
IDS = [16926,17968,17975,19942,20018,20027,20123,20352,20449,20453,20456,20472,20555,20576,20625,20626,20644,20650,20742,20743]
PREV = {x["local_number"]: x for x in json.loads(REPORT.read_text())["entries"]} if REPORT.is_file() else {}

# 001b 复核确立的「题面保证 X → 生成器保证 X」逐条打钩表。
# 只填本轮复核真正逐条核对过题面的题；未核对的留 None（待补），不写 True 充数。
CONSTRAINTS = {
    16926: ["1<=M<=100000", "1<=N<=20", "0<=K<=100", "0<=T<=6000", "五种initial生命值 (0,200]", "五种攻击力 (0,200]"],
    17968: ["N<=1000", "M 为 >=N 的最小素数", "线性探查法", "H(key)=key%M"],
    17975: ["N<=1000", "M 为素数且 M>=2N（题面硬保证「表长不小于关键字总数的2倍」；「>=2N的最小素数」措辞为『一般为』，非硬约束）", "二次探查法 ±i²"],
    19942: ["1<=p<=m", "1<=q<=n", "卷积输出 m+1-p 行、每行 n+1-q 个整数"],
    20018: ["2<=N<=100000（50% 数据 2<=N<=1000）", "速度为非负整数"],
    20123: ["位数<=10^5", "首位不为 0", "不能擦掉所有数字", "允许只剩一个数字 0"],
    20352: ["第一行 n", "接下来 n 行、每行两个不含空格的字符串 s1 s2", "s2 未出现时输出 no"],
    20456: ["恰好 10 行", "每行 10 个 0/1"],
    20472: ["字符串仅由 G L R 组成"],
    20626: ["第一行为正整数数列 V", "第 2-10001 行共 10000 条查询", "L<=R", "下标从 0 开始"],
}

def body(source, number):
    lines = locate_source(source).read_text(encoding="utf-8", errors="ignore").splitlines()
    starts = [i for i,x in enumerate(lines) if re.match(r"^##\s+", x)]
    for i,s in enumerate(starts):
        if re.match(rf"^##\s+[^\d]*0*{number}[:：]", lines[s]):
            return "\n".join(lines[s:starts[i+1] if i+1 < len(starts) else len(lines)])
    raise ValueError(number)

def samples(text, number):
    if number == 19942: return ("5 5 3 3\n3 3 2 1 0\n0 0 1 3 1\n3 1 2 2 3\n2 0 0 2 2\n2 0 0 0 1\n0 1 2\n2 2 0\n0 1 2\n", "12 12 17\n10 17 19\n9 6 14\n")
    if number == 20018: return ("5\n1\n5\n10\n7\n6\n", "7\n")
    if number == 20027: return ("a\n1\n", "c\n")
    if number == 20123: return ("123364315\n", "YES\n")
    if number == 20626:
        q="0 1\n1 2\n0 3\n3 3\n"+"0 0\n"*9996
        return ("1 3 4 8\n"+q, "2\n7\n14\n8\n"+"1\n"*9996)
    if number == 20650: return ("ABCBDAB\nBDCABA\n", "4\n")
    return first_sample(text, "样例输入"), first_sample(text, "样例输出")

def next_prime(x):
    y=max(2,x)
    while any(y%d==0 for d in range(2,int(y**0.5)+1)): y+=1
    return y

def friendly7(s):
    """存在非空保序子序列构成 7 的倍数？与参考解法的 int(sub)%7 同语义。"""
    seen=set()
    for ch in s:
        d=int(ch); seen=seen|{d%7}|{(r*10+d)%7 for r in seen}
        if 0 in seen: return True
    return False

# 题面上界 M<=100000, N<=20, 0<=K<=100, 0<=T<=6000, 生命/攻击力 (0,200]。
# 原生成器只取 M∈[8,35]、K>=1、T>=50，既不贴上界也不覆盖 K=0/T=0 边界。
def g16926(r):
    kind=r.random()
    if kind<0.14: m,n,k,t=r.randint(1,50),r.randint(1,20),0,0                                  # 下界 + K=0 + T=0
    elif kind<0.24: m,n,k,t=100000,20,100,6000                                                 # 贴上界
    elif kind<0.5: m,n,k,t=r.randint(1,120),r.randint(1,4),r.randint(0,100),r.randint(0,150)
    else: m,n,k,t=r.randint(20,3000),r.randint(1,20),r.randint(0,100),r.randint(0,1200)
    hp=" ".join(str(r.randint(1,200)) for _ in range(5)); atk=" ".join(str(r.randint(1,200)) for _ in range(5))
    return f"1\n{m} {n} {k} {t}\n{hp}\n{atk}\n"

# 题面：N<=1000，M 为 >=N 的最小素数（无「一般为」之类的松动措辞）。
# 原生成器从 {5,7,11,13,17} 里独立抽 M，13/20 组的 M 并非 >=N 的最小素数。
def g17968(r):
    n=r.choice([1,2,3,5,10,50,200,999,1000]) if r.random()<0.5 else r.randint(1,1000)
    lo,hi=(-100,100) if n<=10 else (-10**6,10**6)
    return f"{n} {next_prime(n)}\n"+" ".join(str(r.randint(lo,hi)) for _ in range(n))+"\n"
def g17975(r):
    m=r.choice([11,13,17,19,23]); n=r.randint(2,m//2); return f"{n} {m}\n"+" ".join(str(r.randint(-100,100)) for _ in range(n))+"\n"
def g19942(r):
    m,n=r.randint(2,7),r.randint(2,7); p,q=r.randint(1,m),r.randint(1,n); rows=[" ".join(str(r.randint(-5,5)) for _ in range(n)) for _ in range(m)]; ker=[" ".join(str(r.randint(-5,5)) for _ in range(q)) for _ in range(p)]; return f"{m} {n} {p} {q}\n"+"\n".join(rows+ker)+"\n"
# 题面：50% 数据 2<=N<=1000，100% 数据 2<=N<=100000。原生成器封顶 N=80，
# 连 50% 档都没进。参考解法是归并排序数逆序对（O(N log N)），N=1e5 实测 0.33s。
def g20018(r):
    kind=r.random()
    n=r.randint(2,300) if kind<0.58 else (r.randint(1000,3000) if kind<0.84 else r.randint(99000,100000))
    wide=r.random()<0.5
    hi=1000 if (n>=99000 or not wide) else 10**9      # 小值域保留并列（不算赶超）的覆盖；贴上界那组也用小值域压体积
    return str(n)+"\n"+"\n".join(str(r.randint(0,hi)) for _ in range(n))+"\n"
def g20027(r): return "".join(r.choice("abc") for _ in range(r.randint(1,5)))+"\n"+str(r.randint(1,100))+"\n"
# 题面：位数 <= 10^5，输出 YES / NO。原生成器取 randint(1,10^8)，19/20 组 >=7 位，
# 参考解法直接走「>=7 位必 YES」的抽屉原理捷径 —— NO 分支 0/20，print("YES") 能 AC 20/20。
def g20123(r):
    kind=r.random()
    if kind<0.34:                                                                               # 强制 NO：短数且无任何子序列被 7 整除
        for _ in range(400):
            s="".join(str(r.randint(1,9)) for _ in range(r.randint(1,6)))
            if not friendly7(s): return s+"\n"
        return "11\n"
    if kind<0.6:                                                                                # 短数且必 YES：走 DFS 真算法而非捷径
        for _ in range(400):
            s=str(r.randint(1,9))+"".join(str(r.randint(0,9)) for _ in range(r.randint(0,5)))
            if friendly7(s): return s+"\n"
        return "7\n"
    n=r.randint(7,60) if kind<0.88 else r.randint(99000,100000)                                 # 后者贴题面 10^5 位上界
    return str(r.randint(1,9))+"".join(str(r.randint(0,9)) for _ in range(n-1))+"\n"
def g20352(r):
    x=[]
    for _ in range(r.randint(1,5)): x.append("".join(r.choice("abc") for _ in range(r.randint(4,16)))+" "+"".join(r.choice("abc") for _ in range(r.randint(1,3))))
    return str(len(x))+"\n"+"\n".join(x)+"\n"
def g20449(r): return "".join(r.choice("01") for _ in range(r.randint(1,30)))+"\n"
def g20453(r):
    a=[r.randint(-5,8) for _ in range(r.randint(2,20))]; return " ".join(map(str,a))+"\n"+str(r.randint(-8,15))+"\n"
def g20456(r): return "\n".join(",".join(r.choice("01") for _ in range(10)) for _ in range(10))+"\n"
def g20472(r): return "".join(r.choice("GLR") for _ in range(r.randint(1,20)))+"\n"
def g20555(r):
    a=r.choices(["True","False"],k=4); op1=r.choice(["and","or"]); op2=r.choice(["and","or"]); return f"( {a[0]} {op1} {a[1]} ) {op2} ( not {a[2]} or {a[3]} )\n"
def g20576(r):
    a,b,c,d=r.choices(["True","False"],k=4); return f"( not ( {a} {r.choice(['and','or'])} {b} ) ) {r.choice(['and','or'])} ( {c} {r.choice(['and','or'])} {d} )\n"
def g20625(r): return "".join(r.choice("01") for _ in range(r.randint(2,50)))+"\n"
def g20626(r):
    a=[r.randint(1,1000) for _ in range(r.randint(2,20))]; q=[]
    for _ in range(10000):
        l=r.randrange(len(a)); q.append(f"{l} {r.randint(l,len(a)-1)}")
    return " ".join(map(str,a))+"\n"+"\n".join(q)+"\n"
def g20644(r):
    m,n=r.randint(2,10),r.randint(2,10); return f"{m} {n}\n"+"\n".join("".join(r.choice("01") for _ in range(n)) for _ in range(m))+"\n"
def g20650(r):
    return "".join(r.choice("ABCDE") for _ in range(r.randint(2,20)))+"\n"+"".join(r.choice("ABCDE") for _ in range(r.randint(2,20)))+"\n"
def g20742(r): return str(r.randint(1,30))+"\n"
def g20743(r): return "("+"".join(r.choice("abcd") for _ in range(r.randint(1,20)))+")"+"".join(r.choice("abcd") for _ in range(r.randint(0,5)))+"\n"
G={n:globals()[f"g{n}"] for n in IDS}

# 第四代自检（001c 复核追加）：题面写了「否则输出 X」的，数据里必须真有触发 X 的组。
# 值为该题输出空间里必须各自出现过的 token；None 表示该题输出连续、无离散分支。
SPECIAL_BRANCHES={16926:None,17968:None,17975:None,19942:None,20018:None,20027:None,
                  20123:["YES","NO"],20352:["no"],20449:None,20453:["0"],20456:["0"],
                  20472:["0","1"],20555:["0","1"],20576:None,20625:None,20626:None,
                  20644:None,20650:None,20742:None,20743:None}

def branch_covered(number, outs):
    want=SPECIAL_BRANCHES.get(number)
    if want is None: return None
    seen=set()
    for o in outs: seen|=set(o.split())
    return all(t in seen for t in want)

def refreshed(number):
    """未重建的题：自检字段一律从磁盘实测，不沿用上一版报告里的硬编码常量。"""
    data=TESTS/bucket(number)/f"{number:05d}_made"/"data"
    cases=[(data/f"{i}.in").read_text() for i in range(20)]
    outs=[(data/f"{i}.out").read_text() for i in range(20)]
    old=PREV.get(number,{})
    return {"local_number":number,"status":"generated","source":old.get("source"),
            "source_code":"solution collection (sample-validated)","generator":f"g{number}",
            "seed":number,"test_cases":len(cases),"distinct_input_cases":len(set(cases)),
            "distinct_outputs":len(set(outs)),"max_input_bytes":max(len(v) for v in cases),
            "constraints":CONSTRAINTS.get(number),
            "no_solution_branch_covered":branch_covered(number,outs)}

def run(code, inp):
    with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as f:
        f.write(code); f.flush(); result=subprocess.run(["python3",f.name],input=inp,text=True,capture_output=True,timeout=8)
        if result.returncode: raise RuntimeError((result.stderr, inp))
        return result.stdout

def main():
    only={int(x) for x in sys.argv[1].split(",")} if len(sys.argv)>1 else set(IDS)
    manifest=json.loads(MANIFEST.read_text()); by={x["local_number"]:x for x in manifest["entries"]}; report=[]
    for number in IDS:
        if number not in only:
            report.append(refreshed(number)); continue
        entry=by[number]; text=body(entry["source"],number); sin,sout=samples(text,number)
        codes=[c for c in fence_blocks(text) if "import " in c or "def " in c]
        code=None
        for candidate in codes:
            try:
                if run(candidate,sin).split()==sout.split(): code=candidate; break
            except (RuntimeError, subprocess.SubprocessError):
                continue
        if code is None: raise AssertionError(f"no sample solution {number}")
        d=TESTS/bucket(number)/f"{number:05d}_made"; data=d/"data"; data.mkdir(parents=True,exist_ok=True); cases=[sin]
        for i in range(1,20):
            for attempt in range(100):
                v=G[number](random.Random(number+i+attempt*1000))
                if v not in cases: cases.append(v); break
            else: raise AssertionError(f"insufficient diversity {number}")
        outs=[run(code,v) for v in cases]; (d/"samplecode.py").write_text("# Source: "+entry["source"]+"\n"+code)
        prod="import subprocess, tempfile\nfrom pathlib import Path\nCASES="+repr(cases)+"\nSOURCE="+repr(code)+"\nwith tempfile.NamedTemporaryFile('w',suffix='.py') as f:\n f.write(SOURCE); f.flush()\n root=Path(__file__).parent/'data'\n for i,c in enumerate(CASES):\n  o=subprocess.run(['python3',f.name],input=c,text=True,capture_output=True,check=True).stdout\n  (root/f'{i}.in').write_text(c); (root/f'{i}.out').write_text(o)\n"
        (d/"producecase.py").write_text(prod)
        for p in data.glob("*"): p.unlink()
        for i,(v,o) in enumerate(zip(cases,outs)): (data/f"{i}.in").write_text(v); (data/f"{i}.out").write_text(o)
        report.append({"local_number":number,"status":"generated","source":entry["source"],
                       "source_code":"solution collection (sample-validated)","generator":f"g{number}",
                       "seed":number,"test_cases":20,"distinct_input_cases":len(set(cases)),
                       "distinct_outputs":len(set(outs)),"max_input_bytes":max(len(v) for v in cases),
                       "constraints":CONSTRAINTS.get(number),
                       "no_solution_branch_covered":branch_covered(number,outs)})
        print("built",number,len(set(cases)),flush=True)
    (ROOT/"collab/t002-001d-report.json").write_text(json.dumps({"batch":"001d","entries":report},ensure_ascii=False,indent=2)+"\n")
if __name__=="__main__": main()

#!/usr/bin/env python3
"""Build T-004 round 2: independently implemented references and oracles."""
import inspect
import json
import random
import subprocess
import sys
import tempfile
from collections import Counter
from functools import cmp_to_key
from pathlib import Path

from build_001a import bucket

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "collab/t004-round2-manifest.json"
REPORT = ROOT / "collab/t004-round2-report.json"
TESTS = ROOT / "data/openjudge/tests"

def run(code, content, timeout=10):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as f:
        f.write(code)
        f.flush()
        p = subprocess.run([sys.executable, f.name], input=content, text=True,
                           capture_output=True, timeout=timeout)
    if p.returncode:
        raise RuntimeError(p.stderr[-1200:])
    return p.stdout

def g4003(r):
    digits = "0123456789ABCDEF"
    t = r.randint(1, 8)
    return str(t) + "\n" + "\n".join(
        "".join(r.choice(digits) for _ in range(r.randint(1, 8))).lstrip("0") or "0"
        for _ in range(t)
    ) + "\n"

def g4004(r):
    n = r.randint(1, 20)
    values = [r.randint(1, 80) for _ in range(n)]
    return f"{n} {r.randint(1, 1000)}\n" + " ".join(map(str, values)) + "\n"

def g4029(r):
    value = r.randint(-1_000_000_000, 1_000_000_000)
    return f"{value}\n"

def g4085(r):
    n = r.randint(1, 80)
    return f"{n}\n" + " ".join(str(r.randint(0, 10_000)) for _ in range(n)) + "\n"

def g3718(r):
    n = r.randint(1, 50)
    pairs = []
    for _ in range(n):
        a = r.randint(0, 65535)
        if r.random() < .5:
            k = r.randint(0, 15)
            b = ((a << k) | (a >> (16 - k))) & 65535
        else:
            b = r.randint(0, 65535)
        pairs.append(f"{a} {b}")
    return str(n) + "\n" + "\n".join(pairs) + "\n"

def g6645(r):
    if r.random() < .15:
        value = 0
    else:
        value = r.randrange(1, 10**40)
    return f"{value}\n"

def g7745(r):
    return " ".join(str(r.randint(0, 100)) for _ in range(10)) + "\n"

def g23007(r):
    versions = []
    for _ in range(r.randint(1, 20)):
        versions.append(".".join(str(r.randint(0, 100)) for _ in range(r.randint(1, 6))))
    return str(len(versions)) + "\n" + "\n".join(versions) + "\n"

def g27706(r):
    words = [r.choice(["alpha", "B2", "x!", "can't", "42", "node"]) for _ in range(r.randint(1, 20))]
    return " ".join(words) + "\n"

def g28557(r):
    n = r.randint(1, 10)
    return str(n) + "\n" + "\n".join(
        f"{r.randint(1, 1_000_000_000)} {r.randint(1, 1_000_000_000)}"
        for _ in range(n)
    ) + "\n"

GENERATORS = {n: globals()[f"g{n}"] for n in
              [4003, 4004, 4029, 4085, 3718, 6645, 7745, 23007, 27706, 28557]}

REFERENCE = {}
REFERENCE[4003] = r'''import sys
a=sys.stdin.read().split(); t=int(a[0])
print("\n".join(str(int(x,16)) for x in a[1:t+1]))'''
REFERENCE[4004] = r'''import sys
a=list(map(int,sys.stdin.read().split())); n,t=a[:2]; dp=[0]*(t+1); dp[0]=1
for x in a[2:2+n]:
    for s in range(t,x-1,-1): dp[s]+=dp[s-x]
print(dp[t])'''
REFERENCE[4029] = r'''import sys
s=sys.stdin.read().strip()
sign="-" if s.startswith("-") else ""
digits=s[1:] if sign else s
print(sign + digits[::-1].lstrip("0") or "0")'''
REFERENCE[4085] = r'''import sys
a=list(map(int,sys.stdin.read().split())); n=a[0]
print(" ".join(map(str,sorted(set(a[1:n+1])))))'''
REFERENCE[3718] = r'''import sys
a=list(map(int,sys.stdin.read().split())); out=[]
for x,y in zip(a[1::2],a[2::2]):
    out.append("YES" if any(((x<<k)|(x>>(16-k)))&65535==y for k in range(16)) else "NO")
print("\n".join(out))'''
REFERENCE[6645] = r'''import sys
s=sys.stdin.read().strip(); bits=[]
while int(s):
    q,rem=[],0
    for ch in s:
        rem=rem*10+ord(ch)-48
        if q or rem>=2: q.append(str(rem//2)); rem%=2
    s="".join(q) or "0"; bits.append(str(rem))
print("".join(bits[::-1]) or "0")'''
REFERENCE[7745] = r'''import sys
a=list(map(int,sys.stdin.read().split()))
odd=sorted((x for x in a if x%2),reverse=True)
even=sorted(x for x in a if not x%2)
print(" ".join(map(str,odd+even)))'''
REFERENCE[23007] = r'''import sys
a=sys.stdin.read().split(); n=int(a[0]); versions=a[1:1+n]
def key(v): return tuple(map(int,v.split(".")))
print("\n".join(sorted(versions,key=key)))'''
REFERENCE[27706] = r'''import sys
print(" ".join(sys.stdin.read().split()[::-1]))'''
REFERENCE[28557] = r'''import sys
out=[]
for line in sys.stdin.read().splitlines()[1:]:
    a,b=map(int,line.split()); carry=0; count=0
    while a or b:
        carry,a,b=(a%10+b%10+carry)//10,a//10,b//10
        count += carry
    out.append(str(count))
print("\n".join(out))'''

CONSTRAINTS = {
    4003: ["T>=1", "每个十六进制无符号整数长度<=8", "a-f使用大写字母", "数前无多余0", "十进制结果<2^31"],
    4004: ["1<=n<=20", "1<=t<=1000", "输入为n个正整数", "每个数至多使用一次", "输出和为t的组合数"],
    4029: ["输入一个整数N", "-1000000000<=N<=1000000000", "反转后除零外最高位不为0", "负号保留在最高位"],
    4085: ["n<=100000", "整数不超过10000", "输入整数之间可能有若干空格", "输出去重后升序序列"],
    3718: ["0<n<300000", "两个数均为0..65535", "按16位二进制表示循环左移判断"],
    6645: ["十进制数长度<100", "输入数可能非常大", "输出对应二进制表示"],
    7745: ["固定输入10个整数", "每个整数为0..100", "奇数在前且降序", "偶数在后且升序"],
    23007: ["1<=N<=100", "版本号总长度<=100", "主版本号和每个子版本号<=100", "版本段由点连接", "NULL小于0，短版本优先"],
    27706: ["单行句子", "单词数<=50", "每个单词长度<=10", "单词可含字母数字标点", "单词之间一个空格"],
    28557: ["1<=t<=10", "1<=a,b<=1000000000", "统计十进制加法产生的进位次数"],
}

def oracle(n, content):
    if n == 4003:
        a=content.split(); return "\n".join(str(sum("0123456789ABCDEF".index(c)*16**i for i,c in enumerate(x[::-1]))) for x in a[1:])+"\n"
    if n == 4004:
        a=list(map(int,content.split())); values=a[2:2+a[0]]; total=a[1]
        middle=len(values)//2
        left=[0]
        for x in values[:middle]: left += [s+x for s in left]
        right=[0]
        for x in values[middle:]: right += [s+x for s in right]
        counts={}
        for s in right: counts[s]=counts.get(s,0)+1
        count=sum(counts.get(total-s,0) for s in left)
        return f"{count}\n"
    if n == 4029:
        s=content.strip(); neg=s.startswith("-"); d=s[1:] if neg else s
        d=d[::-1].lstrip("0") or "0"
        return ("-" if neg and d!="0" else "")+d+"\n"
    if n == 4085:
        a=list(map(int,content.split())); return " ".join(map(str,sorted(set(a[1:1+a[0]]))))+"\n"
    if n == 3718:
        a=list(map(int,content.split())); out=[]
        for x,y in zip(a[1::2],a[2::2]):
            bits=f"{x:016b}"; out.append("YES" if any(bits[k:]+bits[:k] == f"{y:016b}" for k in range(16)) else "NO")
        return "\n".join(out)+"\n"
    if n == 6645:
        s=content.strip(); out=""
        if s == "0":
            return "0\n"
        while s != "0":
            q=[]; rem=0
            for ch in s:
                rem=rem*10+int(ch); q.append(str(rem//2) if q or rem>=2 else "")
                rem%=2
            s="".join(q) or "0"; out=str(rem)+out
        return out+"\n"
    if n == 7745:
        a=list(map(int,content.split())); odd=[]; even=[]
        for x in a:
            (odd if x%2 else even).append(x)
        odd.sort(reverse=True); even.sort()
        return " ".join(map(str,odd+even))+"\n"
    if n == 23007:
        a=content.split(); vs=a[1:1+int(a[0])]
        def cmp(x,y):
            xx=list(map(int,x.split("."))); yy=list(map(int,y.split(".")))
            for i in range(max(len(xx),len(yy))):
                xv=xx[i] if i<len(xx) else 0; yv=yy[i] if i<len(yy) else 0
                if xv!=yv:return -1 if xv<yv else 1
            return -1 if len(xx)<len(yy) else (1 if len(xx)>len(yy) else 0)
        return "\n".join(sorted(vs,key=cmp_to_key(cmp)))+"\n"
    if n == 27706:
        line=content.rstrip("\n"); words=[]; word=""
        for ch in line+" ":
            if ch==" ":
                if word: words.append(word); word=""
            else: word+=ch
        return " ".join(reversed(words))+"\n"
    if n == 28557:
        a=list(map(int,content.split())); out=[]
        for x,y in zip(a[1::2],a[2::2]):
            carry=0; count=0
            while x or y:
                digit=x%10+y%10+carry
                carry=1 if digit>=10 else 0; count+=carry; x//=10; y//=10
            out.append(str(count))
        return "\n".join(out)+"\n"
    raise KeyError(n)

def mutate(n, source):
    mutations = {
        4003: source.replace("int(x,16)", "int(x,10)"),
        4004: source.replace("range(t,x-1,-1)", "range(t,x-1,1)"),
        4029: source.replace('digits[::-1]', 'digits'),
        4085: source.replace("sorted(set(a[1:n+1]))", "sorted(a[1:n+1])"),
        3718: source.replace("range(16)", "range(15)"),
        6645: source.replace("rem//2", "rem//10"),
        7745: source.replace("reverse=True", "reverse=False"),
        23007: source.replace("key=key", "key=lambda v: tuple(map(int,v.split('.')))[::-1]"),
        27706: source.replace("[::-1]", ""),
        28557: source.replace("(a%10+b%10+carry)//10", "(a%10+b%10+carry)//9"),
    }
    changed = mutations[n]
    assert changed != source
    return changed

def first_diff(n, source, entry):
    probes = {
        4003: "1\nA\n", 4004: "2 3\n1 2\n", 4029: "-380\n",
        4085: "4\n1 1 2 3\n", 3718: "1\n1 32768\n", 6645: "2\n",
        7745: "2 3 4 5 6 7 8 9 10 11\n",
        23007: "2\n2.1\n1.10\n", 27706: "first second third\n",
        28557: "1\n9 9\n",
    }
    case = probes[n]
    try:
        bad = run(source, case).split()
        runtime_error = False
    except (RuntimeError, subprocess.TimeoutExpired) as exc:
        bad = [f"<runtime error: {type(exc).__name__}>"]
        runtime_error = True
    good = oracle(n, case).split()
    return {"case": case, "status": "caught" if bad != good else "missed",
            "mutated_output": bad, "oracle_output": good,
            "runtime_error": runtime_error}

def reproduce(directory):
    data=directory/"data"
    before={p.name:p.read_bytes() for p in data.iterdir()}
    p=subprocess.run([sys.executable,"producecase.py"],cwd=directory,
                     capture_output=True,text=True,timeout=600)
    return p.returncode==0 and before=={p.name:p.read_bytes() for p in data.iterdir()}

def main():
    manifest=json.loads(MANIFEST.read_text(encoding="utf-8"))
    report=[]
    for entry in manifest["entries"]:
        n=entry["local_number"]; ref=REFERENCE[n]
        # The misconception probe is deliberately adjacent to the sample checks.
        assert run(ref, entry["sample_input"]).split()==entry["sample_output"].split()
        assert oracle(n, entry["sample_input"]).split()==entry["sample_output"].split()
        probe=first_diff(n, mutate(n, ref), entry)
        assert probe["status"]=="caught", (n, probe)
        generator=GENERATORS[n]
        for seed in range(20000):
            generator(random.Random(n+seed))
        for seed in range(1000):
            case=generator(random.Random(n+seed))
            assert run(ref,case).split()==oracle(n,case).split(), n
        cases=[entry["sample_input"]]
        for i in range(1,21):
            for attempt in range(100):
                case=generator(random.Random(n+i+attempt*1000))
                if case not in cases: cases.append(case); break
            else: raise AssertionError(f"insufficient diversity {n}")
        d=TESTS/bucket(n)/f"{n:05d}_made"; data=d/"data"; data.mkdir(parents=True,exist_ok=True)
        outputs=[run(ref,x) for x in cases]
        (d/"samplecode.py").write_text("# T-004-r2 reference implementation\n"+ref,encoding="utf-8")
        gsource=inspect.getsource(generator)
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
   for attempt in range(100):
    content={generator.__name__}(random.Random({n}+index+attempt*1000))
    if content not in seen: break
   else: raise AssertionError("insufficient diversity")
  seen.append(content)
  result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
  (root/f"{{index}}.in").write_text(content,encoding="utf-8")
  (root/f"{{index}}.out").write_text(result.stdout,encoding="utf-8")
'''
        (d/"producecase.py").write_text(produce,encoding="utf-8")
        for p in data.glob("*"): p.unlink()
        for i,out in enumerate(outputs):
            (data/f"{i}.in").write_text(cases[i],encoding="utf-8")
            (data/f"{i}.out").write_text(out,encoding="utf-8")
        freq=Counter(tuple(x.split()) for x in outputs)
        report.append({
            "local_number":n,"title":entry["title"],"source":entry["source"],
            "reference_source":"LLM-written","generator":generator.__name__,"seed":n,
            "test_cases":len(cases),"distinct_input_cases":len(set(cases)),
            "distinct_outputs":len(freq),"max_output_frequency":max(freq.values()),
            "constant_output_probe":{"status":"rejected" if max(freq.values())<len(cases) else "accepted",
                                     "frequency":max(freq.values()),"total":len(cases)},
            "constraints":CONSTRAINTS[n],"structure_checked":False,
            "generator_seed_smoke":{"seeds":20000,"status":"passed"},
            "reference_seed_smoke":{"seeds":1000,"status":"passed"},
            "independent_oracle_smoke":{"seeds":1000,"status":"passed"},
            "sample_reproduced":run(ref,entry["sample_input"]).split()==entry["sample_output"].split(),
            "independent_sample_agreement":oracle(n,entry["sample_input"]).split()==entry["sample_output"].split(),
            "misconception_probe":probe,
            "producecase_reproduced":reproduce(d),
        })
        print("built",n,flush=True)
    REPORT.write_text(json.dumps({"batch":"T-004-r2","entries":report},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

if __name__=="__main__":
    main()

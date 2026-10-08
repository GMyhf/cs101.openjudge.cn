import random,re,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='n = int(input())\nl = [int(x) for x in input().split()]\nk = int(input())\nl.sort()\nfor i in range(-1, -k-1, -1):\n    print(l[i])'
SAMPLE='10\n4 5 6 9 8 7 1 2 3 0\n5\n'
GENERATOR_NAME='g7617'
def valid(text):
    """题面：第一行 n（n<100000）；第二行 n 个整数单空格分隔，|x|≤1e8；第三行 k（k<n，取 k≥1）。"""
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    if len(lines) != 3:
        return False
    if not re.fullmatch(r"[1-9][0-9]*", lines[0]) or not re.fullmatch(r"[1-9][0-9]*", lines[2]):
        return False
    n, k = int(lines[0]), int(lines[2])
    if not (n < 100000 and 1 <= k < n):
        return False
    toks = lines[1].split(" ")
    if len(toks) != n:
        return False
    for t in toks:
        if not re.fullmatch(r"-?(0|[1-9][0-9]*)", t) or t == "-0" or abs(int(t)) > 100000000:
            return False
    return True


M=100000000
def g7617(r,seed):
    if seed<=4:   n=r.choice([2,3])                 # 最小规模
    elif seed<=20: n=r.randint(4,60)
    elif seed<=28: n=r.randint(1000,20000)
    elif seed in (29,32,33,37): n=99999              # 题面：n < 100000；保留 4 组满规模
    else:         n=r.randint(20000,40000)           # 其余大组缩小，data/ 控制在 10MB 内
    kmode=seed%4
    k=[1,n-1,r.randint(1,n-1),max(1,n//2)][kmode]    # 题面：k < n
    vmode=seed%5
    if vmode==0:   vals=[r.randint(-M,M) for _ in range(n)]
    elif vmode==1: vals=[r.randint(-20,20) for _ in range(n)]          # 大量重复
    elif vmode==2: vals=[r.randint(-M,-1) for _ in range(n)]           # 全为负数
    elif vmode==3: vals=[r.choice([M,-M,0,r.randint(-M,M)]) for _ in range(n)]  # 取到值域两端
    else:          vals=[r.randint(-10**7,10**7) for _ in range(n)]
    if n>=50000 and vmode in (0,2,3):
        # 控制 .in ≤ 1MB：满规模组大部分取 7 位以内，少量取到 ±1e8
        vals=[v if r.random()<.15 else v//100 for v in vals]
    return f"{n}\n"+" ".join(map(str,vals))+f"\n{k}\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"; p.write_text(REFERENCE,encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[g7617(random.Random(seed),seed) for seed in range(1, 40)]
    assert all(valid(t) for t in cases), "有数据越出题面约束"
    assert len(set(cases))==len(cases), "有重复数据"
    assert all(len(t.encode())<=10**6 for t in cases), "输入超过 1MB"
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text,encoding="utf-8")
        (data/f"{i}.out").write_text(run(text),encoding="utf-8")
if __name__=="__main__": main()

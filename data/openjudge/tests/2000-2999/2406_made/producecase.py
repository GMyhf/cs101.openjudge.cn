import random, subprocess, sys, tempfile
from pathlib import Path
def valid(text):
    """题面契约：若干行，每行一个由可打印字符（ASCII 32..126）组成、长度 1..10^6 的串 s；
    最后一行是单独的点号 "."，其后不再有内容；终止行之前不得出现单独的 "."。"""
    try:
        if not text.endswith("\n.\n"):return False
        lines=text[:-1].split("\n")
        if len(lines)<2 or lines[-1]!=".":return False
        for x in lines[:-1]:
            if not 1<=len(x)<=10**6 or x==".":return False
            if any(not 32<=ord(c)<=126 for c in x):return False
        return True
    except Exception:
        return False

# 字符取 ASCII 33..126（含 '.'，不含空格）：提示要求 scanf，官方数据应无空格
CH=[chr(c) for c in range(33,127)]
def g2406(r, seed=None):
    end=lambda rows:"\n".join(rows)+"\n.\n"
    rs=lambda n,al=CH:"".join(r.choice(al) for _ in range(n))
    def aperiodic(n,al):   # 本身不是任何更短串的幂
        while True:
            b=rs(n,al)
            if all(n%k or b[:k]*(n//k)!=b for k in range(1,n)):return b
    if seed is None or seed>=30:   # 原有的小规模随机组
        rows=[]
        for _ in range(r.randint(1, 15)):
            base = "".join(r.choice("abcd") for _ in range(r.randint(1, 18)))
            rows.append(base * r.randint(1, 15))
        return end(rows)
    L=997920   # 2^5*3^4*5*7*11，240 个因子；单组文件控制在 1e6 字节内
    S=99792    # 2^4*3^4*7*11，缩小规模组用（控制 data/ 合计 ≤ 10MB）
    if seed==1:return end(["a","~","!","..","...",".a",rs(1,[c for c in CH if c!="."])])
    if seed==2:return end(["a"*999997])
    if seed==3:return end(["a"*(L-1)+"b"])
    if seed==4:return end(["b"+"a"*(S-1)])
    if seed==5:return end([aperiodic(1008,"ab")*(L//1008)])   # 长度 L（240 个因子），答案 990
    if seed==6:return end([aperiodic(S//144,"ab")*144])
    if seed==7:b=aperiodic(1008,"ab")*(S//1008);return end([b[:-1]+("a" if b[-1]=="b" else "b")])   # 末位被改，答案 1
    if seed==8:return end(["ab"*(S//2)+"a"])                 # 有周期但不整除，答案 1
    if seed==9:return end([aperiodic(2,"xy")*(S//2)])
    if seed==10:return end([aperiodic(499979,CH)*2])          # 质数长度的基串平方
    if seed==11:return end(["."*99990])                     # 全是点号（不是终止行）
    if seed==12:return end([rs(L)])
    if seed==13:return end([aperiodic(7,"ab")*14285])         # 长度 99995
    if seed==14:return end([aperiodic(r.randint(1,50),"abc")*r.randint(1,60) for _ in range(400)])
    if seed==15:
        rows=[]
        for _ in range(30):
            k=r.choice([d for d in range(1,10001) if 10000%d==0]);b=aperiodic(k,"ab")*(10000//k)
            if r.random()<.3:b=b[:-1]+("a" if b[-1]=="b" else "b")
            rows.append(b)
        return end(rows)
    if seed==16:return end(["aab"*(L//3),"aba"*(L//3//1000)])
    if seed==17:p=aperiodic(31,CH);return end([(p*3)*1000])     # 基串可再分：答案 3000
    if seed==18:return end(["ab"*49998])
    if 19<=seed<=24:
        k=r.choice([d for d in range(1,S+1) if S%d==0 and d<=20000]);return end([aperiodic(k,r.choice(["ab","abc",CH]))*(S//k)])
    rows=[]
    for _ in range(r.randint(1,40)):
        k=r.randint(1,60);rows.append(aperiodic(k,r.choice(["ab","ab.",CH]))*r.randint(1,500))
    return end(rows)

REFERENCE="# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md\n# Heading: 2406: 字符串乘方\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md\n# Upstream problem: http://cs101.openjudge.cn/2024sp_routine/02406/\n# License: not declared in source collection; no license is inferred.\nwhile True:\n    s = input().strip()\n    if s == '.':\n        break\n    len_s = len(s)\n    max_power = 1\n    for i in range(1, len_s // 2 + 1):\n        if len_s % i == 0:\n            a = s[:i]\n            if a * (len_s // i) == s:\n                max_power = max(max_power, len_s // i)\n    print(max_power)\n"
SAMPLE='abcd\naaaa\nababab\n.\n'
GENERATOR='g2406'

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as folder:
        script=Path(folder)/"main.py"; script.write_text(REFERENCE)
        result=subprocess.run([sys.executable,"-I",str(script)],input=text,text=True,capture_output=True,timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    for old in data.glob("*"): old.unlink()
    cases=[SAMPLE]+[globals()[GENERATOR](random.Random(seed),seed) for seed in range(1, 40)]
    for i,case in enumerate(cases):
        (data/f"{i}.in").write_text(case); (data/f"{i}.out").write_text(run(case))
if __name__=="__main__": main()

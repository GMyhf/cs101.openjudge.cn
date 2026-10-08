import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE="# External reference: cs101.openjudge.cn practice/19546 statistics, Accepted solution 30264505.\n# Source: http://cs101.openjudge.cn/practice/solution/30264505/\n# Statistics: http://cs101.openjudge.cn/practice/19546/statistics/\n# License: not declared on submission page; no license inferred\nm = int(input())\nfor i in range(m):\n    a = list(map(float,input().split()))\n    for i in range(5, len(a)):\n        mom = a[i] - a[i-5]\n        if abs(mom - round(mom,1))<1e-6:\n            mom = round(mom,1)\n        else:\n            mom = round(mom,2)\n        print(mom, end = ' ')\n    print()\n"
LANGUAGE='Python3'
SAMPLE='2\n5.81 5.77 5.73 5.7 5.57 5.49 5.62 5.57 5.84 5.82 5.7\n4.97 4.99 5.08 5.03 4.98 4.95 5.02\n'
GENERATOR_NAME='g19546'
import re
_PRICE=re.compile(r"\d+\.\d{1,2}")
def valid(text):
    """题面：第一行整数 m；接下来 m 行，每行一个收盘价序列，空格分开，小数点后有一位或者两位。
    （输出要求周期为 5 的 MOM，序列至少要有 6 个价格才有输出，这里按至少 6 个核。）"""
    lines=text.split("\n")
    if lines[-1]!="": return False
    lines=lines[:-1]
    if not lines or not lines[0].isdigit(): return False
    m=int(lines[0])
    if m<1 or len(lines)!=m+1: return False
    for l in lines[1:]:
        t=l.split(" ")
        if len(t)<6 or not all(_PRICE.fullmatch(x) for x in t): return False
    return True

def _extra(seed):
    """补充：较大规模、恰 6 个价格、价格不变（MOM=0）、整数差、单调涨跌。"""
    r=random.Random(seed); out=[]
    p2=lambda: f"{r.randint(1,99999)/100:.2f}"
    p1=lambda: f"{r.randint(10,9999)/10:.1f}"
    pr=lambda: p2() if r.random()<.5 else p1()
    out.append("1000\n"+"\n".join(" ".join(pr() for _ in range(r.randint(6,100))) for _ in range(1000))+"\n")
    out.append("3\n"+"\n".join(" ".join(pr() for _ in range(6)) for _ in range(3))+"\n")
    out.append("2\n"+" ".join(["12.50"]*12)+"\n"+" ".join(["3.0","4.0","5.0","6.0","7.0","8.0","9.0","10.0","11.0"])+"\n")
    out.append("2\n"+" ".join(f"{x/100:.2f}" for x in range(100,2000,37))+"\n"+" ".join(f"{x/10:.1f}" for x in range(9990,9000,-13))+"\n")
    out.append("1\n"+" ".join(pr() for _ in range(5000))+"\n")
    return out

def g19546(r):
    line=lambda: " ".join(f"{r.randint(1,999)/100:.2f}" if r.random()<.5 else f"{r.randint(10,999)/10:.1f}" for _ in range(r.randint(6,15)))
    m=r.randint(1,8); return f"{m}\n"+"\n".join(line() for _ in range(m))+"\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        d=Path(d); src=d/'main.py'
        src.write_text(REFERENCE); cmd=[sys.executable,str(src)]
        if LANGUAGE=="G++":
            exe=d/"main"; subprocess.run(["g++","-std=c++17","-O2",str(src),"-o",str(exe)],check=True)
            cmd=[str(exe)]
        x=subprocess.run(cmd,input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1, 40)]+_extra(19546)
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text)
        (data/f"{i}.out").write_text(run(text))
if __name__=="__main__": main()

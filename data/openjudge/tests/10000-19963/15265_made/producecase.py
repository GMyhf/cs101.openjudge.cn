import random,re,subprocess,sys,tempfile
from pathlib import Path
REFERENCE="import sys\nn=int(input())\nnums=[int(x) for x in input().split()]\noutput=[]\nk=4\nwhile (1<<k)>n:\n    k-=1\nwhile k>0:\n    t=(1<<k)-1\n    for i in range(t):\n        for j in range((n-1-i)//t+1):\n            e,kk=nums[i+t*j],j\n            while kk>0 and e<nums[i+t*(kk-1)]:\n                nums[i+t*kk]=nums[i+t*(kk-1)]\n                kk-=1\n            nums[i+t*kk]=e\n    output.append(' '.join(map(str,nums)))\n    k-=1\nsys.stdout.write('\\n'.join(output)+'\\n')\n"
SAMPLE='10\n4 7 3 13 11 12 0 47 34 98\n'
GENERATOR_NAME='g15265'
def g15265(r):
    n=r.randint(2,20); z=[r.randint(0,100) for _ in range(n)]
    return f"{n}\n"+" ".join(map(str,z))+"\n"

def valid(text):
    # 题面：第一行 n（2<=n<=20）；第二行 n 个 0~100 的整数，空格分隔
    if not text.endswith("\n"): return False
    lines=text[:-1].split("\n")
    if len(lines)!=2 or not lines[0].isdigit(): return False
    n=int(lines[0]); a=lines[1].split(" ")
    if not 2<=n<=20 or len(a)!=n: return False
    return all(re.fullmatch(r"0|[1-9][0-9]*",x) and int(x)<=100 for x in a)
def fmt(a): return f"{len(a)}\n"+" ".join(map(str,a))+"\n"
# 追加的边界组：逆序满规模、全相等、已有序、n=2 逆序、含 0 与 100、n=16（首趟增量 15）、n=4/8（增量 3/7 恰好开始生效）
DESIGNED=[list(range(100,80,-1)),[50]*20,list(range(0,100,5)),[100,0],[1,0],
          [100,0,100,0,100,0,100,0,100,0,100,0,100,0,100,0],[3,2,1,0],[100,90,80,70,60,50,40,0],
          [0,100]*10]
def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"; p.write_text(REFERENCE,encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1, 40)]+[fmt(a) for a in DESIGNED]
    assert all(valid(t) for t in cases)
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text,encoding="utf-8")
        (data/f"{i}.out").write_text(run(text),encoding="utf-8")
if __name__=="__main__": main()

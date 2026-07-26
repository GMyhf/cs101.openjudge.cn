import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE="# External reference: cs101.openjudge.cn practice/19546 statistics, Accepted solution 30264505.\n# Source: http://cs101.openjudge.cn/practice/solution/30264505/\n# Statistics: http://cs101.openjudge.cn/practice/19546/statistics/\n# License: not declared on submission page; no license inferred\nm = int(input())\nfor i in range(m):\n    a = list(map(float,input().split()))\n    for i in range(5, len(a)):\n        mom = a[i] - a[i-5]\n        if abs(mom - round(mom,1))<1e-6:\n            mom = round(mom,1)\n        else:\n            mom = round(mom,2)\n        print(mom, end = ' ')\n    print()\n"
LANGUAGE='Python3'
SAMPLE='2\n5.81 5.77 5.73 5.7 5.57 5.49 5.62 5.57 5.84 5.82 5.7\n4.97 4.99 5.08 5.03 4.98 4.95 5.02\n'
GENERATOR_NAME='g19546'
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
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1,21)]
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text)
        (data/f"{i}.out").write_text(run(text))
if __name__=="__main__": main()

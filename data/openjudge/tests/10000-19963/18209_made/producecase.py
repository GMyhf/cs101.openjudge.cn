import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE="# External reference: cs101.openjudge.cn practice/18209 statistics, Accepted solution 38077709.\n# Source: http://cs101.openjudge.cn/practice/solution/38077709/\n# Statistics: http://cs101.openjudge.cn/practice/18209/statistics/\n# License: not declared on submission page; no license inferred\nfrom math import log\nn = int(input())\na, b = 0, 0\nlst = list(map(float, input().split()))\nlst.sort()\nfor i in range(n):\n    a -= log(lst[i], 2) * lst[i]\n    if i != 0 and i != n - 1:\n        b -= log(lst[i], 2) * lst[i]\nprint('%.3f' % a)\nprint('%.3f' % b)\n"
LANGUAGE='Python3'
SAMPLE='3\n0.2 0.7 0.1\n'
GENERATOR_NAME='g18209'
def g18209(r):
    n=r.randint(3,10); cuts=sorted(r.sample(range(1,100),n-1)); vals=[]; last=0
    for x in cuts+[100]: vals.append((x-last)/100); last=x
    return f"{n}\n"+" ".join(f"{x:.6f}" for x in vals)+"\n"

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

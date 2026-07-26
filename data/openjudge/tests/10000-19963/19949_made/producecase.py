import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/19949 statistics, Accepted solution 52459098.\n# Source: http://cs101.openjudge.cn/practice/solution/52459098/\n# Statistics: http://cs101.openjudge.cn/practice/19949/statistics/\n# License: not declared on submission page; no license inferred\nn=int(input())\nc=0\n\ndef count(query):\n    t=query.split()\n    cnt=0\n    status=False\n    for piece in t:\n        if "###" in piece:\n            if piece.startswith("###") and piece.endswith("###"):\n                if not status:\n                    cnt+=1\n                    status=True\n        else:\n            status=False\n    return cnt\n\nfor _ in range(n):\n    c+=count(input())\n\nprint(c)\n'
LANGUAGE='Python3'
SAMPLE='1\n###John### has an ###apple### .\n'
GENERATOR_NAME='g19949'
def g19949(r):
    n=r.randint(1,10); rows=[]
    for _ in range(n):
        rows.append(" ".join(r.choice(["###Alice###","plain","###Bob###","word","###X###"]) for _ in range(r.randint(2,10))))
    return f"{n}\n"+"\n".join(rows)+"\n"

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

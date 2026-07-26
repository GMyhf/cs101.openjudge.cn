import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE="# External reference: cs101.openjudge.cn practice/19967 statistics, Accepted solution 51312141.\n# Source: http://cs101.openjudge.cn/practice/solution/51312141/\n# Statistics: http://cs101.openjudge.cn/practice/19967/statistics/\n# License: not declared on submission page; no license inferred\nN = int(input())\nl = []\nfor _ in range(N):\n    inp = input().split()\n    if inp[0] == '+':\n        idx, data = int(inp[1]), int(inp[2])\n        l.insert(idx, data)\n    elif inp[0] == '-':\n        idx = int(inp[1])\n        del l[idx]\n    elif inp[0] == '*':\n        idx, data = int(inp[1]), int(inp[2])\n        l[idx] = data\n    elif inp[0] == '?':\n        data = int(inp[1])\n        if data not in l:\n            print('Failed')\n        else:\n            print(l.index(data))\n"
LANGUAGE='Python3'
SAMPLE='6\n+ 0 1\n+ 0 2\n? 2\n* 1 3\n- 1\n? 1\n'
GENERATOR_NAME='g19967'
def g19967(r):
    ops=[]; size=0
    for _ in range(r.randint(8,30)):
        choices=["+"] if size==0 else ["+","?","*","-"]
        op=r.choice(choices)
        if op=="+": idx=r.randint(0,size); ops.append(f"+ {idx} {r.randint(-20,20)}"); size+=1
        elif op=="-": idx=r.randrange(size); ops.append(f"- {idx}"); size-=1
        elif op=="*": ops.append(f"* {r.randrange(size)} {r.randint(-20,20)}")
        else: ops.append(f"? {r.randint(-20,20)}")
    return f"{len(ops)}\n"+"\n".join(ops)+"\n"

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

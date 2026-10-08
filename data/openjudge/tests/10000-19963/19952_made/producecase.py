import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/19952 statistics, Accepted solution 52328950.\n# Source: http://cs101.openjudge.cn/practice/solution/52328950/\n# Statistics: http://cs101.openjudge.cn/practice/19952/statistics/\n# License: not declared on submission page; no license inferred\na=[0 for i in range(201)]\nb=[0 for i in range(201)]\na[1]=2\nb[1]=1\nfor k in range(2,201):\n    a[k]=2*a[k-1]+2*b[k-1]\n    b[k]=a[k-1]\nt=int(input())\nfor i in range(t):\n    n=int(input())\n    print(a[n]+b[n])\n'
LANGUAGE='Python3'
SAMPLE='1\n1\n'
GENERATOR_NAME='g19952'
def g19952(r):
    t=r.randint(1,12); return f"{t}\n"+"\n".join(str(r.randint(1,200)) for _ in range(t))+"\n"

def valid(text):
    """题面契约：首行正整数 t；接下来恰 t 行，每行一个正整数 N，1<=N<=200。题面未给 t 的上限。"""
    try:
        if not text.endswith("\n"):
            return False
        lines = text[:-1].split("\n")
        t = int(lines[0])
        if t < 1 or len(lines) != t + 1:
            return False
        for line in lines[1:]:
            if line.strip() != line or not 1 <= int(line) <= 200:
                return False
        return True
    except ValueError:
        return False


def extra_cases():
    r = random.Random(199520)
    allN = list(range(1, 201))
    r.shuffle(allN)
    cases = [
        "1\n2\n",
        "1\n200\n",
        "3\n200\n1\n200\n",
        "200\n" + "".join(f"{x}\n" for x in allN),                     # 覆盖每个 N
        "1000\n" + "".join(f"{r.randint(1, 200)}\n" for _ in range(1000)),
        "50\n" + "".join(f"{r.randint(30, 200)}\n" for _ in range(50)),  # 超出 64 位
    ]
    return cases


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
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1, 40)]
    cases+=extra_cases()
    assert len(set(cases))==len(cases), "存在重复测试组"
    for i,text in enumerate(cases):
        assert valid(text), i
        (data/f"{i}.in").write_text(text)
        (data/f"{i}.out").write_text(run(text))
if __name__=="__main__": main()

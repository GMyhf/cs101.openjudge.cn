import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE="# External reference: cs101.openjudge.cn practice/19974 statistics, Accepted solution 28435155.\n# Source: http://cs101.openjudge.cn/practice/solution/28435155/\n# Statistics: http://cs101.openjudge.cn/practice/19974/statistics/\n# License: not declared on submission page; no license inferred\nt = int(input())\nlis = []\nfor T in range(t):\n    m,p,q = input().split()\n    m = int(m)\n    p = int(p)\n    q = int(q)\n    num = 0\n    if m == 0:\n        lis.append('0')\n    elif m > 0:\n        mat = [[0 for _ in range(q+1)]for _ in range(p+1)]\n        for j in range(q+1):\n            if j < m:\n                mat[0][j] = 1\n        for i in range(p+1):\n            mat[i][0] = 1\n        for j in range(1,q+1):\n            for i in range(1,p+1):\n                if j >= i+m:\n                    mat[i][j] = 0\n                else:\n                    mat[i][j] = mat[i-1][j] + mat[i][j-1]\n        lis.append(str(mat[p][q]))\n    elif m < 0:\n        m = -m\n        mat = [[0 for _ in range(q+1)]for _ in range(p+1)]\n        for i in range(p+1):\n            if i < m:\n                mat[i][0] = 1\n        for j in range(q+1):\n            mat[0][j] = 1\n        for j in range(1,q+1):\n            for i in range(1,p+1):\n                if j <= i-m:\n                    mat[i][j] = 0\n                else:\n                    mat[i][j] = mat[i-1][j] + mat[i][j-1]\n        lis.append(str(mat[p][q]))\nfor _ in lis:\n    print(_)\n"
LANGUAGE='Python3'
SAMPLE='1\n1 2 2\n'
GENERATOR_NAME='g19974'
def g19974(r):
    t=r.randint(1,8); return f"{t}\n"+"\n".join(f"{r.randint(-5,5)} {r.randint(1,15)} {r.randint(1,15)}" for _ in range(t))+"\n"

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

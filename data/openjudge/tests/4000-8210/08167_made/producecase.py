import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='import copy\nn, m = map(int, input().split())\nmatrix = [[int(x) for x in input().split()] for _ in range(n)]\nmat = copy.deepcopy(matrix)\nfor i in range(1, n-1):\n    for j in range(1, m-1):\n        mat[i][j] = round((matrix[i][j]+matrix[i][j-1]+matrix[i-1][j]+matrix[i+1][j]+matrix[i][j+1])/5)\nfor i in mat:\n    print(*i)'
SAMPLE='4 5\n100 0 100 0 50\n50 100 200 0 0\n50 50 100 100 200\n100 100 50 50 100\n'
GENERATOR_NAME='g8167'
def g8167(r):
    n,m=r.randint(1,10),r.randint(1,10); z=[[r.randint(0,255) for _ in range(m)] for _ in range(n)]
    return f"{n} {m}\n"+"\n".join(" ".join(map(str,x)) for x in z)+"\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"; p.write_text(REFERENCE,encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1,21)]
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text,encoding="utf-8")
        (data/f"{i}.out").write_text(run(text),encoding="utf-8")
if __name__=="__main__": main()

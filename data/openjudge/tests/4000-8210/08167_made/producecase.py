import random,re,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='import copy\nn, m = map(int, input().split())\nmatrix = [[int(x) for x in input().split()] for _ in range(n)]\nmat = copy.deepcopy(matrix)\nfor i in range(1, n-1):\n    for j in range(1, m-1):\n        mat[i][j] = round((matrix[i][j]+matrix[i][j-1]+matrix[i-1][j]+matrix[i+1][j]+matrix[i][j+1])/5)\nfor i in mat:\n    print(*i)'
SAMPLE='4 5\n100 0 100 0 50\n50 100 200 0 0\n50 50 100 100 200\n100 100 50 50 100\n'
GENERATOR_NAME='g8167'
def g8167(r):
    n,m=r.randint(1,10),r.randint(1,10); z=[[r.randint(0,255) for _ in range(m)] for _ in range(n)]
    return f"{n} {m}\n"+"\n".join(" ".join(map(str,x)) for x in z)+"\n"

def valid(text):
    """题面契约：首行 n m（1 <= n, m <= 100），其后 n 行各 m 个 0~255 的整数，单空格分隔。"""
    if not text.endswith("\n"):
        return False
    lines=text[:-1].split("\n")
    head=lines[0].split(" ")
    if len(head)!=2 or not all(re.fullmatch(r"[1-9][0-9]*",t) for t in head):
        return False
    n,m=map(int,head)
    if not (1<=n<=100 and 1<=m<=100) or len(lines)!=n+1:
        return False
    for line in lines[1:]:
        row=line.split(" ")
        if len(row)!=m or not all(re.fullmatch(r"0|[1-9][0-9]*",t) and int(t)<=255 for t in row):
            return False
    return True

def grid(r,n,m,lo=0,hi=255):
    z=[[r.randint(lo,hi) for _ in range(m)] for _ in range(n)]
    return f"{n} {m}\n"+"\n".join(" ".join(map(str,x)) for x in z)+"\n"

# 追加的边界/规模组：原 40 组最大 10x10，没有 1x1、3x3（唯一内点）、满规模 100x100、全 0/全 255、
# 以及余数为 3、4（向上舍入）与 1、2（向下舍入）的集中检验
def extra_cases():
    r=random.Random(81670)
    out=[grid(r,1,1),grid(r,3,3),grid(r,2,100),grid(r,100,2),grid(r,3,100),grid(r,100,3),grid(r,1,100),grid(r,100,1),
         "3 3\n0 0 0\n0 0 0\n0 0 0\n","3 3\n255 255 255\n255 255 255\n255 255 255\n",
         "3 3\n0 1 0\n1 0 1\n0 1 0\n","3 3\n0 1 0\n1 1 1\n0 0 0\n","3 3\n0 1 0\n1 1 1\n0 1 0\n",
         "3 4\n0 1 1 0\n1 2 2 1\n0 1 1 0\n",
         grid(r,100,100),grid(r,100,100,250,255),grid(r,99,100,0,3),grid(r,100,99)]
    return out

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"; p.write_text(REFERENCE,encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1, 40)]
    cases+=extra_cases()
    assert all(valid(c) for c in cases) and len(set(cases))==len(cases)
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text,encoding="utf-8")
        (data/f"{i}.out").write_text(run(text),encoding="utf-8")
if __name__=="__main__": main()

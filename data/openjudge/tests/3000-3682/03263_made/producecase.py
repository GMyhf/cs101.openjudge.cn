import random,subprocess,tempfile
from pathlib import Path
# 参考解：自底向上 DP，best[i][j] = max(a[i][j], best[i+1][j], best[i+1][j+1])，O(N^2)。
# （原先的递归 f(i,j) 不记忆化，是 O(2^N)，N=100 时跑不完。）
REFERENCE_SOURCE='import sys\na=iter(sys.stdin.read().split()); out=[]\nwhile True:\n n=int(next(a))\n if n==0: break\n t=[[int(next(a)) for _ in range(i+1)] for i in range(n)]\n row,col=int(next(a))-1,int(next(a))-1\n best=t[n-1][:]\n for i in range(n-2,row-1,-1):\n  best=[max(t[i][j],best[j],best[j+1]) for j in range(i+1)]\n out.append(str(best[col]))\nprint("\\n".join(out))'
SAMPLE_IN='1\n2\n1 1\n5\n7\n3 8\n8 1 0\n2 7 4 4\n4 5 2 6 5\n1 1\n6\n88\n97 26\n39 16 47\n94 25 66 4\n64 49 20 36 27\n37 87 29 37 10 40\n2 1\n0\n'
def valid(text):
    """题面：多组数据；每组首行 N(0<=N<=100，N=0 表示结束)，随后 N 行数字三角形（第 i 行 i 个 0..100 的整数），
    再一行 R C 表示第 R 行第 C 个位置（1<=R<=N，1<=C<=R）。"""
    if not text.endswith('\n'):
        return False
    lines = text[:-1].split('\n')
    def ints(ln):
        t = ln.split(' ')
        if not all(x.isdigit() and (x == '0' or x[0] != '0') for x in t):
            return None
        return list(map(int, t))
    k = 0
    while True:
        if k >= len(lines):
            return False
        h = ints(lines[k]); k += 1
        if h is None or len(h) != 1 or not 0 <= h[0] <= 100:
            return False
        n = h[0]
        if n == 0:
            return k == len(lines)
        for i in range(1, n + 1):
            if k >= len(lines):
                return False
            row = ints(lines[k]); k += 1
            if row is None or len(row) != i or not all(0 <= v <= 100 for v in row):
                return False
        if k >= len(lines):
            return False
        rc = ints(lines[k]); k += 1
        if rc is None or len(rc) != 2 or not (1 <= rc[0] <= n and 1 <= rc[1] <= rc[0]):
            return False

def tri(r,n,lo=0,hi=100):
    return [[r.randint(lo,hi) for _ in range(i+1)] for i in range(n)]
def g3263(r,index):
    cases=[]
    def add(rows,R=None,C=None):
        n=len(rows)
        R=R if R is not None else r.randint(1,n)
        C=C if C is not None else r.randint(1,R)
        cases.append((rows,R,C))
    if index==1:
        for v in (0,100,r.randint(1,99)):add([[v]],1,1)
    elif index==2:
        add([[0]*(i+1) for i in range(100)],1,1)
        add([[100]*(i+1) for i in range(100)],50,25)
        add([[0]*(i+1) for i in range(30)],30,30)
    elif index==3:
        for _ in range(4):
            rows=tri(r,r.randint(2,100));n=len(rows)
            add(rows,n,1);add(rows,n,n);add(rows,n,r.randint(1,n))
    elif index==4:
        # 起点本身就是最大值：起点 100，可达区其余都 < 100
        for _ in range(3):
            n=100;rows=tri(r,n,0,99);R=r.randint(1,n);C=r.randint(1,R);rows[R-1][C-1]=100;add(rows,R,C)
    elif index==5:
        # 全局最大值放在可达锥体外紧邻处，卡“取整个三角形/子矩形最大值”的写法
        for _ in range(4):
            n=100;rows=tri(r,n,0,60);R=r.randint(2,60);C=r.randint(1,R)
            i=r.randint(R,n-1)  # 0-based 行号，可达列为 C-1..C-1+(i-R+1)
            outside=[j for j in (C-2,C+i-R+1) if 0<=j<=i]
            rows[i][r.choice(outside)]=100
            add(rows,R,C)
    elif index in (6,7,8):
        for _ in range(8):add(tri(r,100),1,1)
    elif index in (9,10,11,12):
        for _ in range(8):add(tri(r,100))
    elif index<=25:
        for _ in range(r.randint(1,6)):add(tri(r,r.randint(1,100)))
    else:
        for _ in range(r.randint(1,8)):add(tri(r,r.randint(1,10),0,r.choice((5,100))))
    lines=[]
    for rows,R,C in cases:
        lines+=[str(len(rows))]+[" ".join(map(str,x)) for x in rows]+[f"{R} {C}"]
    return "\n".join(lines+["0"])+"\n"
def main():
 with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
  handle.write(REFERENCE_SOURCE);handle.flush()
  root=Path(__file__).parent/"data";root.mkdir(exist_ok=True)
  for p in root.glob("*"):p.unlink()
  for index in range(40):
   content=SAMPLE_IN if index==0 else g3263(random.Random(3263+index),index)
   assert valid(content),index
   result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=60,check=True)
   (root/f"{index}.in").write_text(content,encoding="utf-8")
   (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")
if __name__=="__main__":main()

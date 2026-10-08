import random,subprocess,sys,tempfile
from pathlib import Path
import re

# ---- 输入契约（照题面）：若干组，每组首行 N（3<=N<=100），后跟 N×N 邻接矩阵，
# 对角线为 0，任意两农场距离不超过 100000（非负整数，矩阵对称）。
# 注：题面称物理行长不超过 80 字符、矩阵行会折行；但平台上通过的参考解（及大量学生解）按行读矩阵，
# 说明实际判题数据是一行一整行矩阵。这里沿用一行一行的写法，valid() 只核逻辑结构、不核 80 字符。
_INT=re.compile(r'(0|[1-9][0-9]*)$')
def valid(text):
    try:
        if not text.endswith('\n'): return False
        toks=text.split()
        if not toks or any(not _INT.match(x) for x in toks): return False
        a=list(map(int,toks));p=0
        while p<len(a):
            n=a[p];p+=1
            if not 3<=n<=100 or p+n*n>len(a): return False
            M=a[p:p+n*n];p+=n*n
            for i in range(n):
                if M[i*n+i]!=0: return False
                for j in range(n):
                    if i!=j and not (M[i*n+j]<=100000 and M[i*n+j]==M[j*n+i]): return False
        return True
    except Exception:
        return False

def _case(r,n,kind='rand'):
    M=[[0]*n for _ in range(n)]
    pts=[(r.randint(0,70000),r.randint(0,70000)) for _ in range(n)]
    for i in range(n):
        for j in range(i+1,n):
            if kind=='max': w=100000
            elif kind=='few': w=r.choice([1,2,100000])
            elif kind=='geo': w=min(100000,int(((pts[i][0]-pts[j][0])**2+(pts[i][1]-pts[j][1])**2)**.5))
            elif kind=='hi': w=r.randint(99000,100000)
            else: w=r.randint(1,100000)
            M[i][j]=M[j][i]=w
    if kind=='iso':   # 某个点到其余点全是 100000，其他边都小
        for i in range(n):
            for j in range(i+1,n): M[i][j]=M[j][i]=r.randint(1,1000)
        v=r.randrange(n)
        for j in range(n):
            if j!=v: M[v][j]=M[j][v]=100000
    return f"{n}\n"+"\n".join(" ".join(map(str,row)) for row in M)

def generate(seed):
    r=random.Random(1258*1_000_003+seed)
    cs=[]
    if seed==1: cs=[_case(r,3),"3\n0 1 1\n1 0 1\n1 1 0","3\n0 100000 100000\n100000 0 100000\n100000 100000 0"]
    elif seed==2: cs=[_case(r,100,'max')]                  # 全是 100000：答案 9900000
    elif seed==3: cs=[_case(r,100,'iso'),_case(r,50,'iso'),_case(r,3,'iso')]
    elif seed==4: cs=[_case(r,100) for _ in range(8)]
    elif seed==5: cs=[_case(r,100,'geo') for _ in range(4)]
    elif seed==6: cs=[_case(r,100,'few') for _ in range(4)]
    elif seed==7: cs=[_case(r,100,'hi') for _ in range(4)]
    else:
        for _ in range(r.randint(1,6)):
            n=r.choice([r.randint(3,100),100,r.randint(3,10)])
            cs.append(_case(r,n,r.choice(['rand','rand','geo','few','hi','iso'])))
    return "\n".join(cs)+"\n"

REFERENCE='# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md\n# Heading: 1258: Agri-Net\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md\n# Upstream problem: http://cs101.openjudge.cn/practice/01258/\n# License: not declared in source collection; no license is inferred.\nimport sys\n#王昊 光华管理学院\nfrom heapq import heappop, heappush\n\n\nwhile True:\n    try:\n        n = int(input())\n    except:\n        break\n    mat, cur = [], 0\n    for i in range(n):\n        mat.append(list(map(int, input().split())))\n    d, v, q, cnt = [10**9 for i in range(n)], set(), [], 0\n    d[0] = 0\n    heappush(q, (d[0], 0))\n    while q:\n        x, y = heappop(q)\n        if y in v:\n            continue\n        v.add(y)\n        cnt += d[y]\n        for i in range(n):\n            if d[i] > mat[y][i]:\n                d[i] = mat[y][i]\n                heappush(q, (d[i], i))\n    print(cnt)\n'
NUMBER=1258
SAMPLE='4\n0 4 9 21\n4 0 8 17\n9 8 0 16\n21 17 16 0\n'
CASES=40
def run(x):
 with tempfile.TemporaryDirectory() as t:
  p=Path(t)/'s.py';p.write_text(REFERENCE);q=subprocess.run([sys.executable,'-I',str(p)],input=x,text=True,capture_output=True,timeout=120)
  if q.returncode:raise SystemExit(q.stderr)
  return '\n'.join(line.rstrip() for line in q.stdout.rstrip().splitlines())+'\n'
def main():
 d=Path('data');d.mkdir(exist_ok=True)
 for p in d.glob('*'):p.unlink()
 for i,x in enumerate([SAMPLE]+[generate(s) for s in range(1, CASES)]):
  assert valid(x),i
  (d/f'{i}.in').write_text(x);(d/f'{i}.out').write_text(run(x))
if __name__=='__main__':main()

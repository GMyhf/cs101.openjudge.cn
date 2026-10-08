import random,subprocess,sys,tempfile
from pathlib import Path
import re

# ---- 输入契约（照题面）：若干个数据集直到文件尾，每个为 "cash N n1 D1 ... nN DN"，
# 0<=cash<=100000，0<=N<=10，0<=nk<=1000，1<=Dk<=1000，且 N 种面额互不相同（exactly N distinct bill denominations）；
# 数之间可出现任意空白。
_INT=re.compile(r'(0|[1-9][0-9]*)$')
def valid(text):
    try:
        if not text.endswith('\n'): return False
        toks=text.split()
        if not toks or any(not _INT.match(x) for x in toks): return False
        a=list(map(int,toks));p=0
        while p<len(a):
            if p+2>len(a): return False
            cash,n=a[p],a[p+1];p+=2
            if not (0<=cash<=100000 and 0<=n<=10) or p+2*n>len(a): return False
            ds=a[p+1:p+2*n:2];cs=a[p:p+2*n:2];p+=2*n
            if any(not 0<=c<=1000 for c in cs) or any(not 1<=d<=1000 for d in ds) or len(set(ds))!=n: return False
        return True
    except Exception:
        return False

def _ds(r,cash,pairs,ws):
    toks=[str(cash),str(len(pairs))]+[str(x) for c,d in pairs for x in (c,d)]
    if ws=='plain': return " ".join(toks)
    if ws=='double':   # 与样例一致：每对之间两个空格
        return " ".join(toks[:2])+"".join("  "+toks[i]+" "+toks[i+1] for i in range(2,len(toks),2))
    seps=[" "," ","  ","\n","   "," \n "]   # 空白可任意出现（含换行）
    return toks[0]+"".join(r.choice(seps)+t for t in toks[1:])

def _pairs(r,n,cmax=1000,dlo=1,dhi=1000):
    ds=r.sample(range(dlo,dhi+1),n)
    return [(r.choice([r.randint(0,cmax),cmax,r.randint(0,5)]),d) for d in ds]

def generate(seed):
    r=random.Random(1276*1_000_003+seed)
    ws='free' if seed%4==0 else ('double' if seed%4==1 else 'plain')
    D=[]
    if seed==1:
        D=[(0,[]),(100000,[]),(0,[(1000,1)]),(735,[(0,1),(0,2)]),(1,[(1000,2)]),(999,[(1,1000)]),(1000,[(1,1000)]),(100000,[(1000,1)])]
    elif seed==2:   # 满规模：cash=1e5、N=10、每种 1000 张
        D=[(100000,[(1000,d) for d in r.sample(range(1,1001),10)]) for _ in range(3)]
    elif seed==3:   # 面额都大且互素，凑不满
        D=[(100000,[(1000,d) for d in r.sample(range(900,1001),10)]),(99999,[(r.randint(1,1000),d) for d in (991,997,983,977,971,967,953,947,941,937)]),
           (100000,[(3,d) for d in r.sample(range(500,1001),10)])]
    elif seed==4:   # 总额不足 cash：答案就是全部钞票之和
        D=[(100000,[(r.randint(0,10),r.randint(1,1000)) for _ in range(1)]),(100000,_pairs(r,10,cmax=9))]
    elif seed==5:   # 只有偶数面额 / 公因数，cash 为奇数
        D=[(99999,[(1000,d) for d in r.sample(range(2,1001,2),10)]),(77777,[(1000,d) for d in r.sample(range(7,1001,7),10)])]
    else:
        for _ in range(r.randint(1,12)):
            heavy=sum(1 for c,_ in D if c>20000)
            cash=r.choice([r.randint(0,100000),100000,r.randint(0,1000)]) if heavy<3 else r.randint(0,20000)
            n=r.choice([r.randint(0,10),10,10])
            D.append((cash,_pairs(r,n,cmax=r.choice([1000,1000,30]),dlo=r.choice([1,1,100,500]))))
    return "\n".join(_ds(r,c,p,ws) for c,p in D)+"\n"

REFERENCE='# External reference: statistics page /practice/01276/\n# Accepted submission: 51703514\n# Source: http://cs101.openjudge.cn/practice/solution/51703514/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\ndef solve():\n    data = sys.stdin.read().strip().split()\n    idx = 0\n    results = []\n    while idx < len(data):\n        cash = int(data[idx])\n        idx += 1\n        N = int(data[idx])\n        idx += 1\n        if N == 0:\n            results.append("0")\n            continue\n        bills = []\n        for _ in range(N):\n            nk = int(data[idx])\n            idx += 1\n            Dk = int(data[idx])\n            idx += 1\n            bills.append((nk, Dk))\n        items = []\n        for nk, Dk in bills:\n            k = 1\n            while nk > 0:\n                take = min(k, nk)\n                items.append((take * Dk, take))\n                nk -= take\n                k <<= 1\n        dp = [False] * (cash + 1)\n        dp[0] = True\n        for value, _ in items:\n            for j in range(cash, value - 1, -1):\n                if dp[j - value]:\n                    dp[j] = True\n        for j in range(cash, -1, -1):\n            if dp[j]:\n                results.append(str(j))\n                break\n    sys.stdout.write("\\n".join(results))\nif __name__ == "__main__":\n    solve()\n'
NUMBER=1276
SAMPLE='735 3  4 125  6 5  3 350\n633 4  500 30  6 100  1 5  0 1\n735 0\n0 3  10 100  10 50  10 10\n'
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

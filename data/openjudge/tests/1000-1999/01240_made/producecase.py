import random,subprocess,sys,tempfile
from pathlib import Path
import re
from math import comb

# ---- 输入契约（照题面）：若干行 "m s1 s2"，1<=m<=20，s1/s2 长度 1..26 且等长，
# 恰由前 k 个小写字母组成（各出现一次）；保证至少存在一棵树；答案在 32 位有符号整数内；以单独一行 0 结束。
_INT=re.compile(r'-?(0|[1-9][0-9]*)$')
def _count(m,pre,post):
    # 计数满足前序/后序的 m 叉树个数；不存在返回 0
    if len(pre)!=len(post) or not pre or pre[0]!=post[-1]: return 0
    pre,post=pre[1:],post[:-1];res=1;cnt=0;i=0
    while i<len(pre):
        j=post.find(pre[i])
        if j<i: return 0
        c=_count(m,pre[i:j+1],post[i:j+1])
        if c==0: return 0
        res*=c;cnt+=1;i=j+1
    return 0 if cnt>m else res*comb(m,cnt)

def valid(text):
    try:
        if not text.endswith('\n'): return False
        lines=text[:-1].split('\n')
        if len(lines)<2 or lines[-1]!='0': return False
        for ln in lines[:-1]:
            t=ln.split(' ')
            if len(t)!=3 or not _INT.match(t[0]): return False
            m=int(t[0]);s1,s2=t[1],t[2];k=len(s1)
            if not 1<=m<=20 or not 1<=k<=26 or len(s2)!=k: return False
            al=set(chr(97+i) for i in range(k))
            if len(set(s1))!=k or set(s1)!=al or set(s2)!=al: return False
            c=_count(m,s1,s2)
            if not 1<=c<=2**31-1: return False
        return True
    except Exception:
        return False

def _tree(r,k,m,shape):
    # 随机生成每个结点至多 m 个孩子的有根树，返回 (前序串, 后序串)
    ch=[[] for _ in range(k)]
    for v in range(1,k):
        if shape=='deep': cand=[u for u in range(max(0,v-2),v) if len(ch[u])<m]
        elif shape=='wide': cand=[u for u in range(min(v,3)) if len(ch[u])<m]
        else: cand=[u for u in range(v) if len(ch[u])<m]
        if not cand: cand=[u for u in range(v) if len(ch[u])<m]
        ch[r.choice(cand)].append(v)
    for c in ch: r.shuffle(c)
    pre=[];post=[]
    def dfs(u):
        pre.append(u)
        for w in ch[u]: dfs(w)
        post.append(u)
    dfs(0)
    letters=[chr(97+i) for i in range(k)]
    if r.random()<.7: r.shuffle(letters)   # 前序不一定是 abc… 顺序
    lab={u:letters[i] for i,u in enumerate(pre)}
    return "".join(lab[u] for u in pre),"".join(lab[u] for u in post)

def _line(r,k,m,shape,big=False):
    # 随机树计数越过 32 位时逐步减小 m（m=1 时答案恒为 1，必然成功）
    while True:
        best=None
        for _ in range(40 if big else 200):
            s1,s2=_tree(r,k,m,shape);c=_count(m,s1,s2)
            if c<=2**31-1:
                if not big: return f"{m} {s1} {s2}"
                if best is None or c>best[0]: best=(c,f"{m} {s1} {s2}")
        if best: return best[1]
        m-=1

def generate(seed):
    r=random.Random(1240*1_000_003+seed)
    rows=[]
    if seed==1:   # k=1，各种 m
        rows=[f"{m} a a" for m in (1,2,7,20)]
    elif seed==2: # m=1：只有一种树
        rows=[_line(r,k,1,'any') for k in (1,2,5,26)]+["1 "+"".join(chr(97+i) for i in range(26))+" "+"".join(chr(97+i) for i in range(26))[::-1]]
    elif seed==3: # 根有 20 个孩子（m=20，C(20,20)=1）以及 25 叶子不同挂法
        rows=["20 "+"".join(chr(97+i) for i in range(21))+" "+"".join(chr(98+i) for i in range(20))+"a"]
        rows+=[_line(r,26,20,'wide') for _ in range(5)]
    elif seed==4: # 答案尽量接近 2^31-1
        rows=[_line(r,r.randint(8,26),r.randint(2,20),r.choice(['any','deep','wide']),big=True) for _ in range(20)]
    elif seed==5: # 链：m^(k-1) 不越界的最大情况
        rows=["20 abcdefgh hgfedcba","2 "+"".join(chr(97+i) for i in range(26))+" "+"".join(chr(97+i) for i in range(26))[::-1],
              "3 "+"".join(chr(97+i) for i in range(20))+" "+"".join(chr(97+i) for i in range(20))[::-1]]
    else:
        for _ in range(r.randint(1,40)):
            k=r.choice([r.randint(1,26),26,r.randint(15,26)])
            m=r.choice([r.randint(1,20),r.randint(1,4),20])
            rows.append(_line(r,k,m,r.choice(['any','any','deep','wide']),big=r.random()<.3))
    return "\n".join(rows)+"\n0\n"

REFERENCE="# External reference: http://cs101.openjudge.cn/practice/01240/statistics/\n# Accepted submission: 49174560\n# Source: http://cs101.openjudge.cn/practice/solution/49174560/\n# License: not declared on the submission page; no license is inferred.\n\nfrom math import comb\ndef count(m,sPre,sPost):\n    if not sPre or not sPost:\n        return 1\n    i=1\n    j=0\n    res=1\n    k=0\n    while i<len(sPre):\n        k+=1\n        root=sPre[i]\n        ind=sPost.index(root)\n        sub_tree=ind-j+1\n        newPre=sPre[i:i+sub_tree]\n        newPost=sPost[j:ind+1]\n        res*=count(m,newPre,newPost)\n        i=i+sub_tree\n        j=ind+1\n    res*=comb(m,k)\n    return res\nwhile True:\n    line=input().split()\n    if line[0]=='0':\n        break\n    m=int(line[0])\n    sPre=line[1]\n    sPost=line[2]\n    print(count(m,sPre,sPost))\n"
NUMBER=1240
SAMPLE='2 abc cba\n2 abc bca\n10 abc bca\n13 abejkcfghid jkebfghicda\n0\n'
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

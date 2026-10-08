import random,re,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\na=list(map(int,sys.stdin.read().split())); i=0; out=[]\nwhile i+1<len(a):\n cap,n=a[i],a[i+1]; i+=2; dp=[0]*(cap+1)\n for _ in range(n):\n  p,v=a[i],a[i+1]; i+=2\n  for x in range(cap,p-1,-1): dp[x]=max(dp[x],dp[x-p]+v)\n out.append(str(dp[cap]))\nprint("\\n".join(out))'
# 题面样例含两组数据（读到文件结束）
SAMPLE_IN='90 4\n20 25\n30 20\n40 50\n10 18\n40 2\n25 30\n10 8\n'

def valid(text):
    # 题面：若干组数据直到文件结束；每组首行 C N（1<=C<=1000，1<=N<=100），
    # 接着 N 行，每行两个 1..100 的整数：价格、评价分数
    if not isinstance(text,str) or not text.endswith("\n") or "\r" in text:
        return False
    lines=text[:-1].split("\n")
    i=0
    if not lines or lines==[""]:
        return False
    def nums(line):
        if not re.fullmatch(r"[1-9]\d* [1-9]\d*",line):return None
        return tuple(map(int,line.split()))
    while i<len(lines):
        h=nums(lines[i])
        if h is None:return False
        c,n=h
        if not (1<=c<=1000 and 1<=n<=100):return False
        if i+1+n>len(lines):return False
        for line in lines[i+1:i+1+n]:
            pv=nums(line)
            if pv is None or not all(1<=x<=100 for x in pv):return False
        i+=1+n
    return True

def block(r,kind):
    if kind=="max":
        c,n=1000,100
        items=[(r.randint(1,100),r.randint(1,100)) for _ in range(n)]
    elif kind=="greedy":
        # 性价比贪心会错：一个高性价比小件挤掉两个刚好装满的大件
        c=r.randint(50,1000)
        n=r.randint(3,100)
        items=[]
        while len(items)<n:
            a=r.randint(c//3+1,max(c//3+1,min(100,c//2))) if c<=200 else r.randint(60,100)
            items.append((a,r.randint(60,100)))
            if len(items)<n:
                items.append((r.randint(max(1,c-2*a+1),100) if c-2*a+1<=100 else r.randint(1,100),r.randint(1,100)))
        items=items[:n]
    elif kind=="zero":
        # 额度小于所有价格，答案 0
        c=r.randint(1,99)
        n=r.randint(1,100)
        items=[(r.randint(c+1,100),r.randint(1,100)) for _ in range(n)]
    elif kind=="all":
        # 额度够点所有菜
        n=r.randint(1,10)
        items=[(r.randint(1,100),r.randint(1,100)) for _ in range(n)]
        c=min(1000,sum(p for p,_ in items)+r.randint(0,20))
    elif kind=="exact":
        # 价格和恰为 C 的子集
        n=r.randint(1,100)
        items=[(r.randint(1,100),r.randint(1,100)) for _ in range(n)]
        sub=r.sample(items,r.randint(1,min(n,10)))
        c=max(1,min(1000,sum(p for p,_ in sub)))
    elif kind=="tiny":
        c=r.randint(1,10);n=r.randint(1,5)
        items=[(r.randint(1,12),r.randint(1,100)) for _ in range(n)]
    else:
        c=r.randint(1,1000);n=r.randint(1,100)
        items=[(r.randint(1,100),r.randint(1,100)) for _ in range(n)]
    return f"{c} {len(items)}\n"+"\n".join(f"{p} {v}" for p,v in items)

def g3714(r,index):
    if index==1:
        return "1 1\n1 1\n"
    if index==2:
        return "1000 100\n"+"100 100\n"*100
    if index==3:
        return "1 1\n2 100\n100 3\n51 60\n50 50\n50 50\n10 3\n5 10\n5 10\n10 19\n"
    kinds=["rand","greedy","zero","all","exact","tiny"]
    if index<=12:
        blocks=[block(r,r.choice(kinds)) for _ in range(r.randint(1,3))]
    elif index<=30:
        blocks=[block(r,r.choice(kinds+["max"])) for _ in range(r.randint(3,10))]
    else:
        blocks=[block(r,"max") for _ in range(r.randint(15,20))]+[block(r,r.choice(kinds)) for _ in range(3)]
        r.shuffle(blocks)
    return "\n".join(blocks)+"\n"

def main():
    with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE);handle.flush()
        root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
        for index in range(40):
            if index==0:content=SAMPLE_IN
            else:
                for attempt in range(100):
                    content=g3714(random.Random(3714+index+attempt*1000),index)
                    if content not in seen:break
                else:raise AssertionError("insufficient diversity")
            assert valid(content),index
            seen.append(content)
            result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
            (root/f"{index}.in").write_text(content,encoding="utf-8")
            (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")

if __name__=="__main__":
    main()

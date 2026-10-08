import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE="import sys\n\ndef solve():\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n    \n    n = int(input_data[0])\n    w = int(input_data[1])\n    \n    items = []\n    for i in range(n):\n        items.append(int(input_data[2 + i]))\n        \n    # 核心剪枝 1：从大到小排序，优先放大的道具\n    items.sort(reverse=True)\n    \n    # ans 记录全局最优解，最坏情况下需要 n 个包（每个道具一个包）\n    ans = n\n    # bags 数组就是你要的“记录装了一半的包”的数据结构\n    bags = []\n\n    def dfs(idx):\n        nonlocal ans\n        \n        # 核心剪枝 2：如果当前用的包数已经大于等于已知的最优解，直接放弃这条搜索分支\n        if len(bags) >= ans:\n            return\n            \n        # 如果所有道具都放完了，更新最优解\n        if idx == n:\n            ans = min(ans, len(bags))\n            return\n            \n        current_item = items[idx]\n        \n        # 尝试 1：把当前道具放进已经开过的包里\n        for i in range(len(bags)):\n            if bags[i] + current_item <= w:\n                bags[i] += current_item  # 放进去\n                dfs(idx + 1)             # 继续放下一个道具\n                bags[i] -= current_item  # 回溯：拿出来，尝试下一种可能\n                \n        # 尝试 2：新开一个包来装当前道具\n        bags.append(current_item)\n        dfs(idx + 1)\n        bags.pop() # 回溯：把新开的包撤销\n\n    dfs(0)\n    print(ans)\n\nif __name__ == '__main__':\n    solve()\n"
SAMPLE='5 1996\n1\n2\n1994\n12\n29\n'
GENERATOR_NAME='g15286'
def valid(text):
    """题面：第一行 N W；接下来 N 行每行一个 Ci；1<=N<=18，1<=Ci<=W<=1e8。"""
    if not text.endswith("\n"): return False
    lines=text[:-1].split("\n")
    try:
        head=lines[0].split()
        if len(head)!=2 or lines[0]!=" ".join(head): return False
        n,w=map(int,head)
        if not (1<=n<=18 and 1<=w<=10**8): return False
        if len(lines)!=n+1: return False
        for s in lines[1:]:
            if s.strip()!=s or len(s.split())!=1: return False
            c=int(s)
            if not 1<=c<=w: return False
    except ValueError:
        return False
    return True

def _split(r,w,parts):
    cuts=sorted(r.sample(range(1,w),parts-1))
    return [b-a for a,b in zip([0]+cuts,cuts+[w])]

def g15286(r,kind):
    W=10**8
    if kind=="tiny":            # 小规模、小载重
        n=r.randint(1,10); w=r.randint(1,100); z=[r.randint(1,w) for _ in range(n)]
    elif kind=="rand":          # 大规模随机
        n=r.randint(12,18); w=r.choice([W,r.randint(10**6,W)]); lo=r.choice([1,w//10,w//5,w//4])
        z=[r.randint(max(1,lo),w) for _ in range(n)]
    elif kind=="perfect":       # 18 件恰好拼成若干满包，卡贪心（首次适应递减等）
        w=r.randint(W//2,W)
        while True:
            z=[]
            while len(z)<18: z+=_split(r,w,r.randint(2,4))
            if len(z)==18: break
        r.shuffle(z); n=18
    elif kind=="nearthird":     # 重量在 W/4~W/3 附近，每包装 2~3 件，搜索分支多
        n=r.randint(13,15); w=W; z=[r.randint(w//4+1,w//3+w//20) for _ in range(n)]
    elif kind=="full":          # Ci=W，答案为 N
        n=18; w=r.randint(1,W); z=[w]*n
    elif kind=="light":         # 总重不超过 W，答案为 1
        n=18; w=W; z=[r.randint(1,W//18) for _ in range(n)]
    return f"{n} {w}\n"+"\n".join(map(str,z))+"\n"

KINDS=["tiny"]*5+["rand"]*7+["perfect"]*11+["nearthird"]*6+["full"]*2+["light"]*3
FIXED=["1 1\n1\n","1 100000000\n100000000\n","3 100000000\n"+"50000000\n"*3,
       "2 100000000\n50000000\n50000001\n","2 100000000\n50000000\n50000000\n"]

def build_cases():
    cases=[SAMPLE]+list(FIXED)
    for seed,kind in enumerate(KINDS,1):
        for attempt in range(100):
            t=g15286(random.Random(seed*1000+attempt),kind)
            if t not in cases: cases.append(t); break
        else: raise AssertionError("生成器多样性不足")
    return cases

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"; p.write_text(REFERENCE,encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=build_cases()
    assert len(cases)==40 and all(valid(t) for t in cases)
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text,encoding="utf-8")
        (data/f"{i}.out").write_text(run(text),encoding="utf-8")
if __name__=="__main__": main()

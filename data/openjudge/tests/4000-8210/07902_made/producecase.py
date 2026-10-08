import random,re,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='def max_peanuts(M, N, K, field):\n    # 提取所有有花生的位置及其数量\n    peanuts = []\n    for i in range(M):\n        for j in range(N):\n            if field[i][j] > 0:\n                peanuts.append((field[i][j], i, j))\n    \n    # 按照花生数量从大到小排序\n    peanuts.sort(reverse=True, key=lambda x: x[0])\n    \n    # 初始化当前时间和采摘的花生总数\n    current_time = 0\n    total_peanuts = 0\n    \n    # 初始位置设为路边\n    current_pos = (-1, 0)\n    \n    for peanut in peanuts:\n        amount, x, y = peanut\n        \n        # 计算从当前位置到该位置的时间\n        if current_pos[0] == -1:  # 从路边跳到第一行\n            time_to_reach = x + 1 + abs(current_pos[1] - y)\n        else:\n            time_to_reach = abs(current_pos[0] - x) + abs(current_pos[1] - y)\n        \n        if current_pos == (-1, 0):  # 从路边跳到第一行的时间\n            current_time += (x + 1)\n        else:\n            current_time += time_to_reach\n        \n        # 采摘花生需要1单位时间\n        current_time += 1\n        \n        if current_time + x + 1 <= K:\n            total_peanuts += amount\n            current_pos = (x, y)\n        else:\n            break\n    \n    return total_peanuts\n\n# 读取输入\nM, N, K = map(int, input().split())\nfield = []\nfor _ in range(M):\n    field.append(list(map(int, input().split())))\n\n# 计算并输出结果\nresult = max_peanuts(M, N, K, field)\nprint(result)\n'
SAMPLE='6 7 21\n0 0 0 0 0 0 0\n0 0 0 0 13 0 0\n0 0 0 0 0 0 7\n0 15 0 0 0 0 0\n0 0 0 9 0 0 0\n0 0 0 0 0 0 0\n'
SAMPLE2='6 7 20\n0 0 0 0 0 0 0\n0 0 0 0 13 0 0\n0 0 0 0 0 0 7\n0 15 0 0 0 0 0\n0 0 0 9 0 0 0\n0 0 0 0 0 0 0\n'
GENERATOR_NAME='g7902'


def valid(text):
    """题面契约：首行 M N K（1 <= M, N <= 20，0 <= K <= 1000），其后 M 行各 N 个整数 0 <= Pij <= 500，
    单空格分隔；题面"假设这些植株下的花生个数各不相同"——非零的 Pij 两两互异。"""
    if not text.endswith("\n"):
        return False
    lines=text[:-1].split("\n")
    nat=lambda t: re.fullmatch(r"0|[1-9][0-9]*",t) is not None
    head=lines[0].split(" ")
    if len(head)!=3 or not all(map(nat,head)):
        return False
    m,n,k=map(int,head)
    if not (1<=m<=20 and 1<=n<=20 and 0<=k<=1000) or len(lines)!=m+1:
        return False
    vals=[]
    for line in lines[1:]:
        row=line.split(" ")
        if len(row)!=n or not all(map(nat,row)) or any(int(x)>500 for x in row):
            return False
        vals+=[int(x) for x in row if x!="0"]
    return len(vals)==len(set(vals))


def render(m,n,k,z):
    return f"{m} {n} {k}\n"+"\n".join(" ".join(map(str,x)) for x in z)+"\n"


def place(r,m,n,cnt,hi=500):
    """在 m*n 网格里随机放 cnt 棵互异的非零花生（1..hi）。"""
    z=[[0]*n for _ in range(m)]
    cells=r.sample([(i,j) for i in range(m) for j in range(n)],cnt)
    for (i,j),v in zip(cells,r.sample(range(1,hi+1),cnt)):
        z[i][j]=v
    return z


def g7902(r):
    m,n=r.randint(1,20),r.randint(1,20)
    cnt=r.randint(1,min(m*n,r.choice([5,15,60,400])))
    z=place(r,m,n,cnt)
    k=r.randint(0,1000) if r.random()<.3 else r.randint(0,6*(m+n))
    return render(m,n,k,z)


def extra_cases():
    r=random.Random(79020)
    out=[render(1,1,3,[[500]]),render(1,1,2,[[500]]),render(1,1,0,[[0]]),
         render(3,3,1000,[[0]*3 for _ in range(3)]),
         render(4,4,0,place(r,4,4,5)),
         render(20,20,1000,place(r,20,20,400)),           # 满格、K 上限
         render(20,20,1000,place(r,20,20,200)),
         render(20,20,60,place(r,20,20,400)),
         render(20,1,41,[[0]]*19+[[500]]),                # 恰好够来回：20+1+20
         render(20,1,40,[[0]]*19+[[500]]),                # 差 1 个单位
         render(1,20,1000,[list(range(500,480,-1))]),
         # 最大的离得远、次大的就在路边：必须在最大那棵就停下（不能跳过去采次大）
         render(10,10,15,[[0]*9+[400]]+[[0]*10 for _ in range(8)]+[[0]*9+[500]]),
         render(10,10,12,[[499]+[0]*9]+[[0]*10 for _ in range(8)]+[[0]*9+[500]]),
        ]
    for i in range(6):
        m,n=r.randint(15,20),r.randint(15,20)
        out.append(render(m,n,r.randint(100,1000),place(r,m,n,r.randint(50,m*n))))
    return out

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"; p.write_text(REFERENCE,encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE,SAMPLE2]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(2, 40)]+extra_cases()
    assert all(valid(c) for c in cases) and len(set(cases))==len(cases)
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text,encoding="utf-8")
        (data/f"{i}.out").write_text(run(text),encoding="utf-8")
if __name__=="__main__": main()

"""16926 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001d
生成器与循环取自 scripts/build_001d.py（批次 001d），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 16926
SAMPLE_IN = '1\n20 1 10 400\n20 20 30 10 20\n5 5 5 5 5\n'
SAMPLE_OUT = 'Case 1:\n000:00 blue lion 1 born\nIts loyalty is 10\n000:10 blue lion 1 marched to city 1 with 10 elements and force 5\n000:50 20 elements in red headquarter\n000:50 10 elements in blue headquarter\n000:55 blue lion 1 has 0 sword 1 bomb 0 arrow and 10 elements\n001:05 blue lion 1 ran away\n001:50 20 elements in red headquarter\n001:50 10 elements in blue headquarter\n002:50 20 elements in red headquarter\n002:50 10 elements in blue headquarter\n003:50 20 elements in red headquarter\n003:50 10 elements in blue headquarter\n004:50 20 elements in red headquarter\n004:50 10 elements in blue headquarter\n005:50 20 elements in red headquarter\n005:50 10 elements in blue headquarter\n'
REFERENCE_SOURCE = '# 本题参考解（替换原题解集代码）：原代码判「战斗不再变化」时把武器下标也算进状态，\n# 双方只剩攻击力为 0 的 sword 且件数不同（如攻击力 <5 的武士）时下标永远在转，战斗死循环。\n# 这里改为：双方都没有武器、或双方剩下的都只是伤害为 0 的 sword 时，判平局结束。\nimport sys\nNAMES=["dragon","ninja","iceman","lion","wolf"]\nWN=["sword","bomb","arrow"]\nclass W:\n    pass\ndef make(side,kind,num,hp,atk,left):\n    w=W(); w.side=side; w.kind=kind; w.num=num; w.hp=hp; w.atk=atk; w.loy=left; w.arms=[]  # arms: [type, uses]\n    def give(t): w.arms.append([t,2 if t==2 else 1])\n    if kind in ("dragon","iceman","lion"): give(num%3)\n    elif kind=="ninja": give(num%3); give((num+1)%3)\n    return w\ndef dmg(w,t): return w.atk*(2,4,3)[t]//10\ndef tag(w): return f"{w.side} {w.kind} {w.num}"\ndef fight(a,b):\n    """a 先手。返回后双方状态已更新。"""\n    for w in (a,b): w.arms.sort(key=lambda x:(x[0],x[1]))\n    ptr={id(a):0,id(b):0}\n    def stuck(w):\n        return all(x[0]==0 for x in w.arms) and (not w.arms or dmg(w,0)==0)\n    cur,oth=a,b\n    while True:\n        if not a.arms and not b.arms: return\n        if stuck(a) and stuck(b): return\n        if cur.arms:\n            p=ptr[id(cur)]; x=cur.arms[p]; d=dmg(cur,x[0]); oth.hp-=d\n            if x[0]==1:\n                if cur.kind!="ninja": cur.hp-=d//2\n                cur.arms.pop(p)\n            else:\n                if x[0]==2:\n                    x[1]-=1\n                if x[0]==2 and x[1]==0: cur.arms.pop(p)\n                else: p+=1\n                ptr[id(cur)]=p\n            if cur.arms: ptr[id(cur)]=ptr[id(cur)]%len(cur.arms)\n            else: ptr[id(cur)]=0\n            if a.hp<=0 or b.hp<=0: return\n        cur,oth=oth,cur\ndef take(dst,src_list,limit=10):\n    n=0\n    for x in src_list:\n        if len(dst.arms)>=limit: break\n        dst.arms.append(x); n+=1\n    return n\ndef case(M,N,K,T,hps,atks,out):\n    order={"red":["iceman","lion","wolf","ninja","dragon"],"blue":["lion","dragon","ninja","iceman","wolf"]}\n    elem={"red":M,"blue":M}; cnt={"red":0,"blue":0}; stop={"red":False,"blue":False}\n    red=[None]*(N+2); blue=[None]*(N+2)\n    h=0\n    while h*60<=T:\n        ts=f"{h:03d}"\n        for side,arr,home in (("red",red,0),("blue",blue,N+1)):\n            if stop[side]: continue\n            k=order[side][cnt[side]%5]; i=NAMES.index(k)\n            if elem[side]<hps[i]: stop[side]=True; continue\n            elem[side]-=hps[i]; cnt[side]+=1\n            w=make(side,k,cnt[side],hps[i],atks[i],elem[side]); arr[home]=w\n            out.append(f"{ts}:00 {tag(w)} born")\n            if k=="lion": out.append(f"Its loyalty is {w.loy}")\n        if h*60+5>T: break\n        for c in range(N+2):\n            w=red[c]\n            if w and w.kind=="lion" and c!=N+1 and w.loy<=0: out.append(f"{ts}:05 {tag(w)} ran away"); red[c]=None\n            w=blue[c]\n            if w and w.kind=="lion" and c!=0 and w.loy<=0: out.append(f"{ts}:05 {tag(w)} ran away"); blue[c]=None\n        if h*60+10>T: break\n        nr=[None]*(N+2); nb=[None]*(N+2)\n        for c in range(N+2):\n            for w,nc,dst in ((red[c],c+1,nr),(blue[c],c-1,nb)):\n                if w is None: continue\n                if w.kind=="iceman": w.hp-=w.hp//10\n                if w.kind=="lion": w.loy-=K\n                dst[nc]=w\n        red,blue=nr,nb\n        over=False\n        for c in range(N+2):\n            for w in (red[c],blue[c]):\n                if w is None: continue\n                if c==0 or c==N+1:\n                    hq="red" if c==0 else "blue"\n                    out.append(f"{ts}:10 {tag(w)} reached {hq} headquarter with {w.hp} elements and force {w.atk}")\n                    out.append(f"{ts}:10 {hq} headquarter was taken"); over=True\n                else:\n                    out.append(f"{ts}:10 {tag(w)} marched to city {c} with {w.hp} elements and force {w.atk}")\n        if over: break\n        if h*60+35>T: break\n        for c in range(1,N+1):\n            r,b=red[c],blue[c]\n            if not(r and b) or (r.kind=="wolf")==(b.kind=="wolf"): continue\n            wolf,vic=(r,b) if r.kind=="wolf" else (b,r)\n            if not vic.arms: continue\n            t=min(x[0] for x in vic.arms)\n            cand=sorted([x for x in vic.arms if x[0]==t],key=lambda x:-x[1])\n            got=[]\n            for x in cand:\n                if len(wolf.arms)>=10: break\n                wolf.arms.append(x); got.append(x)\n            for x in got: vic.arms.remove(x)\n            if got: out.append(f"{ts}:35 {tag(wolf)} took {len(got)} {WN[t]} from {tag(vic)} in city {c}")\n        if h*60+40>T: break\n        for c in range(1,N+1):\n            r,b=red[c],blue[c]\n            if not(r and b): continue\n            if c%2: fight(r,b)\n            else: fight(b,r)\n            if r.hp<=0 and b.hp<=0:\n                out.append(f"{ts}:40 both {tag(r)} and {tag(b)} died in city {c}"); red[c]=blue[c]=None\n            elif r.hp<=0 or b.hp<=0:\n                win,lose=(b,r) if r.hp<=0 else (r,b)\n                lose.arms.sort(key=lambda x:(x[0],-x[1])); take(win,lose.arms)\n                out.append(f"{ts}:40 {tag(win)} killed {tag(lose)} in city {c} remaining {win.hp} elements")\n                if win.kind=="dragon": out.append(f"{ts}:40 {tag(win)} yelled in city {c}")\n                if lose is r: red[c]=None\n                else: blue[c]=None\n            else:\n                out.append(f"{ts}:40 both {tag(r)} and {tag(b)} were alive in city {c}")\n                for w in (r,b):\n                    if w.kind=="dragon": out.append(f"{ts}:40 {tag(w)} yelled in city {c}")\n        if h*60+50>T: break\n        out.append(f"{ts}:50 {elem[\'red\']} elements in red headquarter")\n        out.append(f"{ts}:50 {elem[\'blue\']} elements in blue headquarter")\n        if h*60+55>T: break\n        for c in range(N+2):\n            for w in (red[c],blue[c]):\n                if w is None: continue\n                n=[sum(1 for x in w.arms if x[0]==t) for t in range(3)]\n                out.append(f"{ts}:55 {tag(w)} has {n[0]} sword {n[1]} bomb {n[2]} arrow and {w.hp} elements")\n        h+=1\ndef main():\n    d=list(map(int,sys.stdin.read().split())); t=d[0]; p=1; out=[]\n    for k in range(1,t+1):\n        M,N,K,T=d[p:p+4]; hps=d[p+4:p+9]; atks=d[p+9:p+14]; p+=14\n        out.append(f"Case {k}:"); case(M,N,K,T,hps,atks,out)\n    print("\\n".join(out))\nmain()\n'

def valid(text):
    """题面：第一行 t（组数，题面未给上界，要求 t>=1）；每组三行：
    M N K T（1<=M<=100000，1<=N<=20，0<=K<=100，0<=T<=6000）；
    五个初始生命值、五个攻击力，都大于 0 小于等于 200。"""
    if not text.endswith("\n"): return False
    lines=text[:-1].split("\n")
    def ints(s,k):
        t=s.split()
        if len(t)!=k or s!=" ".join(t): raise ValueError
        return list(map(int,t))
    try:
        (t,)=ints(lines[0],1)
        if t<1 or len(lines)!=1+3*t: return False
        for i in range(t):
            m,n,k,tt=ints(lines[1+3*i],4)
            if not (1<=m<=100000 and 1<=n<=20 and 0<=k<=100 and 0<=tt<=6000): return False
            for row in (lines[2+3*i],lines[3+3*i]):
                if not all(1<=v<=200 for v in ints(row,5)): return False
    except ValueError:
        return False
    return True

def _one(r):
    kind=r.random()
    if kind<0.14: m,n,k,t=r.randint(1,50),r.randint(1,20),0,0                                  # 下界 + K=0 + T=0
    elif kind<0.24: m,n,k,t=100000,20,100,6000                                                 # 贴上界
    elif kind<0.5: m,n,k,t=r.randint(1,120),r.randint(1,4),r.randint(0,100),r.randint(0,150)
    else: m,n,k,t=r.randint(20,3000),r.randint(1,20),r.randint(0,100),r.randint(0,1200)
    hp=" ".join(str(r.randint(1,200)) for _ in range(5)); atk=" ".join(str(r.randint(1,200)) for _ in range(5))
    return f"{m} {n} {k} {t}\n{hp}\n{atk}\n"

def _lowatk(r):
    """攻击力很低（sword 伤害为 0）：大量平局、双方只剩 0 伤害武器的僵局，wolf 抢到多件 sword。"""
    m=r.choice([r.randint(50,500),r.randint(1000,20000)]); n=r.randint(1,20); k=r.randint(0,30); t=r.randint(600,6000)
    hp=" ".join(str(r.randint(1,60)) for _ in range(5)); atk=" ".join(str(r.randint(1,r.choice([4,9,14]))) for _ in range(5))
    return f"{m} {n} {k} {t}\n{hp}\n{atk}\n"

def g16926(r,kind="legacy"):
    if kind=="legacy": return "1\n"+_one(r)
    if kind=="lowatk": return "1\n"+_lowatk(r)
    # 多组数据：每组之间状态必须清零
    t=r.randint(2,8); parts=[(_lowatk if r.random()<0.3 else _one)(r) for _ in range(t)]
    return f"{t}\n"+"".join(parts)

KINDS=["legacy"]*10+["lowatk"]*4+["multi"]*5

def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, len(KINDS) + 1):
        for attempt in range(100):
            value = g16926(random.Random(NUMBER + i + attempt * 1000), KINDS[i-1])
            if value not in cases:
                cases.append(value)
                break
        else:
            raise AssertionError("生成器多样性不足")
    assert len(cases) == 20 and all(valid(c) for c in cases)
    return cases

def solve_reference(content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE)
        handle.flush()
        result = subprocess.run(["python3", handle.name], input=content, text=True,
                                capture_output=True, timeout=120, check=True)
    return result.stdout


def main():
    cases = build_cases()
    assert cases[0] == SAMPLE_IN, "第 0 组必须是题面样例"
    assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split(), "参考解法跑不出样例输出"
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for index, content in enumerate(cases):
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")


if __name__ == "__main__":
    main()

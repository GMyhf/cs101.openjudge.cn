"""仓库自产数据：按完整题面构造边界与典型错解反例；固定种子可复现。"""
import importlib.util
from pathlib import Path
import random
import re
spec=importlib.util.spec_from_file_location('reference',Path(__file__).with_name('samplecode.py'))
reference=importlib.util.module_from_spec(spec)
spec.loader.exec_module(reference)
NUMBER=27207
SAMPLE_IN = '3\n3\n1 3\n1 1 2\n2 2\n2 2\n9 0\n\n2\n4 0\n\n1 1\n2\n1\n1 0\n\n'
SAMPLE_OUT = '4\n'

def parse(text):
    lines=text.splitlines(); n=int(lines[0]); pos=1; recipes=[]
    if not 1<=n<=10000: raise ValueError('n')
    for u in range(n):
        k=int(lines[pos]); pos+=1
        if not 1<=k<=100: raise ValueError('k')
        row=[]
        for _ in range(k):
            t,x=map(int,lines[pos].split()); ingredients=list(map(int,lines[pos+1].split())); pos+=2
            if not (0<=t<=10000 and 0<=x<=10000 and len(ingredients)==x and all(0<=v<n for v in ingredients)): raise ValueError('配方')
            row.append((t,ingredients))
        recipes.append(row)
    if pos!=len(lines): raise ValueError('多余行')
    # 依赖图须无环；同一前体出现多次表示多个摩尔，不能去重计价。
    deps=[set(v for _,vs in row for v in vs) for row in recipes]; done=set()
    parents=[[] for _ in range(n)]; degree=list(map(len,deps))
    for u,vs in enumerate(deps):
        for v in vs: parents[v].append(u)
    queue=[u for u in range(n) if not degree[u]]
    for u in queue:
        done.add(u)
        for v in parents[u]:
            degree[v]-=1
            if not degree[v]: queue.append(v)
    if len(done)!=n: raise ValueError('循环制备')
    return recipes

def valid(text):
    try: parse(text); return True
    except (ValueError,IndexError,TypeError): return False

def encode(recipes):
    lines=[str(len(recipes))]
    for row in recipes:
        lines.append(str(len(row)))
        for t,vs in row: lines.extend((f'{t} {len(vs)}',' '.join(map(str,vs))))
    return '\n'.join(lines)+'\n'

def generate(number,seed):
    assert number==27207 and 1<=seed<=20
    rng=random.Random(number*100+seed)
    if seed==1: rows=[[(0,[])]]
    elif seed==2: rows=[[(10000,[])]]
    elif seed==3: rows=[[(1,[1,1,1])],[(2,[])]]
    elif seed==4: rows=[[(1,[1]),(10,[])],[(100,[])]]
    elif seed==5: rows=[[(0,[1,2])],[(0,[3])],[(0,[3])],[(7,[])]]
    elif seed==18: rows=[[(0,[1]*10000)],[(10000,[])]]
    elif seed==19: rows=[[(t,[]) for t in range(100)]]
    elif seed==20: rows=[[(10000,[u+1])] for u in range(9999)]+[[(10000,[])]]
    else:
        n=(seed-4)*7; rows=[]
        for u in range(n):
            row=[]
            for _ in range(rng.randint(1,5)):
                x=0 if u==n-1 else rng.randint(0,min(8,n-u-1))
                row.append((rng.randint(0,10000),[rng.randrange(u+1,n) for _ in range(x)]))
            rows.append(row)
        # 打乱节点编号；0号仍为目标，不承诺依赖编号有序。
        order=list(range(1,n)); rng.shuffle(order); mapping=[0]+order; shuffled=[None]*n
        for u,row in enumerate(rows): shuffled[mapping[u]]=[(t,[mapping[v] for v in vs]) for t,vs in row]
        rows=shuffled
    return encode(rows)

def build(target=None):
    target=Path(target) if target is not None else Path(__file__).parent/'data'
    target.mkdir(parents=True,exist_ok=True); seen=set()
    for seed in range(21):
        given=SAMPLE_IN if seed==0 else generate(NUMBER,seed)
        assert valid(given) and given not in seen, (seed,'非法或重复输入')
        seen.add(given)
        answer=reference.solve(given)+'\n'
        if seed==0: assert answer==SAMPLE_OUT, '题面样例答案不符'
        (target/f'{seed}.in').write_bytes(given.encode())
        (target/f'{seed}.out').write_bytes(answer.encode())

if __name__=='__main__': build()

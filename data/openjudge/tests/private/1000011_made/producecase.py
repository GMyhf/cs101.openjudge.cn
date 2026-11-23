"""数算 A 往年私有题：确定性数据、逐项输入契约与独立小规模 oracle。

本仓库自写；参考解出处见同目录 samplecode.py。大规模组另外经真判验证。
"""
import importlib.util
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('reference_' + HERE.name, HERE / 'samplecode.py')
reference = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reference)

SAMPLE_IN = '6\n1 2\n1 3\n3 4\n4 5\n4 6\n'
SAMPLE_OUT = '5\n'


def parse(text):
    lines=text.splitlines(); n=int(lines[0]); edges=[tuple(map(int,line.split())) for line in lines[1:]]
    return n,edges


def valid(text):
    try:
        n,edges=parse(text)
        if not 2<=n<=50000 or len(edges)!=n-1: return False
        children=[[] for _ in range(n+1)]; parents=set()
        for row in edges:
            if len(row)!=2: return False
            u,v=row
            if not(1<=u<=n and 2<=v<=n) or v in parents: return False
            parents.add(v); children[u].append(v)
            if len(children[u])>2: return False
        seen={1}; stack=[1]
        for u in stack:
            for v in children[u]:
                if v in seen: return False
                seen.add(v); stack.append(v)
        return len(seen)==n
    except (ValueError,IndexError):
        return False


def oracle(text):
    """枚举删除叶子后重新计算整棵树，用于小树和只有一个叶子的长链。"""
    n,edges=parse(text)
    children=[[] for _ in range(n+1)]
    for u,v in edges: children[u].append(v)
    leaves=[i for i in range(1,n+1) if not children[i]]
    if n>100 and len(leaves)>1: return None
    best=10**30
    order=[1]
    for u in order: order.extend(children[u])
    for leaf in leaves:
        sizes=[0]*(n+1); total=0
        for u in reversed(order):
            if u==leaf: continue
            parts=[sizes[v] for v in children[u]]+[0,0]
            sizes[u]=1+sum(parts)
            total+=abs(parts[0]-parts[1])
        best=min(best,total)
    return str(best)+'\n'


def render(n,edges):
    return str(n)+'\n'+''.join(f'{u} {v}\n' for u,v in edges)


def cases(seed):
    rng=random.Random(1000011+seed)
    yield SAMPLE_IN
    yield render(2,[(1,2)])
    yield render(3,[(1,2),(1,3)])
    yield render(4,[(1,2),(2,3),(3,4)])
    for i in range(4,18):
        n=2*i+5; slots=[1,1]; edges=[]
        for v in range(2,n+1):
            j=rng.randrange(len(slots)); u=slots.pop(j)
            edges.append((u,v)); slots.extend([v,v])
        rng.shuffle(edges)
        yield render(n,edges)
    yield render(50000,[(i,i+1) for i in range(1,50000)])
    yield render(32767,[(i//2,i) for i in range(2,32768)])
    n=50000; perm=list(range(2,n+1)); rng.shuffle(perm); mp=[0,1]+perm
    edges=[(mp[i//2],mp[i]) for i in range(2,n+1)]; rng.shuffle(edges)
    yield render(n,edges)

def generate(number, seed):
    """固定种子；number 选择边界形状，seed 控制内容。"""
    return list(cases(seed))[number % 21]


def build():
    data = HERE / 'data'
    data.mkdir(exist_ok=True)
    seen = set()
    for i, text in enumerate(cases(1)):
        assert valid(text), (i, text[:200])
        assert text not in seen, i
        seen.add(text)
        answer = reference.solve(text)
        expected = oracle(text)
        if expected is not None:
            assert answer == expected, (i, answer[:200], expected[:200])
        if i == 0:
            assert text == SAMPLE_IN and answer == SAMPLE_OUT, answer
        (data / f'{i}.in').write_text(text, encoding='utf-8')
        (data / f'{i}.out').write_text(answer, encoding='utf-8')
    assert len(seen) == 21
    print(HERE.name, '21 组，样例与独立 oracle 通过')


if __name__ == '__main__':
    build()

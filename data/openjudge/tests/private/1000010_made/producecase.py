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

SAMPLE_IN = '4\n1 2 1\n1 3 1\n1 4 2\n'
SAMPLE_OUT = '12\n'


def parse(text):
    lines=text.splitlines(); n=int(lines[0])
    edges=[tuple(map(int,line.split())) for line in lines[1:]]
    return n,edges


def valid(text):
    try:
        n,edges=parse(text)
        if not 1<=n<=100000 or len(edges)!=n-1: return False
        parent=list(range(n+1))
        def find(u):
            while parent[u]!=u:
                parent[u]=parent[parent[u]]; u=parent[u]
            return u
        for row in edges:
            if len(row)!=3: return False
            u,v,w=row
            if not(1<=u<=n and 1<=v<=n and 1<=w<=100000): return False
            u,v=find(u),find(v)
            if u==v: return False
            parent[u]=v
        return True
    except (ValueError,IndexError):
        return False


def oracle(text):
    """小树逐对走唯一路径：新边必须严格大于路径最大权。"""
    n,edges=parse(text)
    if n>100: return None
    graph=[[] for _ in range(n+1)]
    original=set()
    answer=sum(w for u,v,w in edges)
    for u,v,w in edges:
        graph[u].append((v,w)); graph[v].append((u,w)); original.add(tuple(sorted((u,v))))
    for start in range(1,n+1):
        stack=[(start,0,0)]
        while stack:
            u,parent,m=stack.pop()
            if u>start and (start,u) not in original: answer+=m+1
            for v,w in graph[u]:
                if v!=parent: stack.append((v,u,max(m,w)))
    return str(answer)+'\n'


def render(n,edges):
    return str(n)+'\n'+''.join(f'{u} {v} {w}\n' for u,v,w in edges)


def cases(seed):
    rng=random.Random(1000010+seed)
    yield SAMPLE_IN
    yield render(1,[])
    yield render(2,[(1,2,100000)])
    yield render(4,[(1,2,1),(2,3,1),(3,4,1)])
    for i in range(4,18):
        n=i*3
        edges=[(rng.randrange(1,v),v,rng.choice([1,1,100000,rng.randint(1,100000)])) for v in range(2,n+1)]
        rng.shuffle(edges)
        yield render(n,edges)
    yield render(100000,[(i,i+1,100000) for i in range(1,100000)])
    yield render(100000,[(1,i,1) for i in range(2,100001)])
    yield render(100000,[(rng.randrange(1,i),i,rng.randint(1,100000)) for i in range(2,100001)])

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

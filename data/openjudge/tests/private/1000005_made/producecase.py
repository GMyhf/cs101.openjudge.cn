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

from collections import deque
import heapq
SAMPLE_IN = '3\n1 3\n2 2\n3 1\n'
SAMPLE_OUT = '25\n'


def valid(text):
    try:
        lines=text.splitlines()
        n=int(lines[0])
        rows=[tuple(map(int,line.split())) for line in lines[1:]]
        return 1<=n<=200000 and len(rows)==n and all(len(r)==2 and all(1<=v<=200000 for v in r) for r in rows) and len({r[0] for r in rows})==n
    except (ValueError,IndexError):
        return False


def oracle(text):
    """两个单调队列，每项为一个等权游程，不使用参考解的堆。"""
    a=list(map(int,text.split()))
    leaves=deque(sorted([a[i],a[i+1]] for i in range(1,len(a),2)))
    merged=deque()
    total=sum(c for _,c in leaves)
    answer=0
    def queue():
        return leaves if leaves and (not merged or leaves[0][0]<=merged[0][0]) else merged
    def take():
        q=queue()
        w,c=q[0]
        if c==1: q.popleft()
        else: q[0][1]-=1
        return w
    while total>1:
        q=queue()
        w,c=q[0]
        if c>=2:
            pairs=c//2
            if c%2: q[0][1]=1
            else: q.popleft()
            merged.append([2*w,pairs])
            answer+=2*w*pairs
            total-=pairs
        else:
            w=take()+take()
            merged.append([w,1])
            answer+=w
            total-=1
    return str(answer)+'\n'


def render(rows):
    return str(len(rows))+'\n'+''.join(f'{w} {c}\n' for w,c in rows)


def cases(seed):
    rng=random.Random(1000005+seed)
    yield SAMPLE_IN
    yield render([(1,1)])
    yield render([(200000,1)])
    yield render([(1,200000)])
    yield render([(1,199999)])
    yield render([(2,3),(1,1)])
    for i in range(6,18):
        n=5+i
        rows=[(w,rng.randint(1,200000 if i%3==0 else 30)) for w in rng.sample(range(1,200001),n)]
        yield render(rows)
    yield render([(w,1) for w in range(200000,0,-1)])
    yield render([(w,200000) for w in range(1,1001)])
    yield render([(w,200000) for w in range(1,200001)])

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

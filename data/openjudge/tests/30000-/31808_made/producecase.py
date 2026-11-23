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

SAMPLE_IN = '4\n0 0\n1 1\n1 0\n0 1\n'
SAMPLE_OUT = '4\n'


def valid(text):
    try:
        lines=text.splitlines(); n=int(lines[0])
        rows=[list(map(int,line.split())) for line in lines[1:]]
        return 1<=n<=200000 and len(rows)==n and all(len(r)==2 and all(0<=v<=10**9 for v in r) for r in rows)
    except (ValueError,IndexError):
        return False


def oracle(text):
    """归并排序统计 v 非逆序对，与 Fenwick 的实现独立。"""
    a=list(map(int,text.split()))
    values=[v for _,v in sorted((x+y,x-y) for x,y in zip(a[1::2],a[2::2]))]
    def merge(a):
        if len(a)<=1: return a,0
        left,x=merge(a[:len(a)//2]); right,y=merge(a[len(a)//2:])
        out=[]; i=j=0; count=x+y
        while i<len(left) and j<len(right):
            if left[i]<=right[j]:
                count+=len(right)-j
                out.append(left[i]); i+=1
            else:
                out.append(right[j]); j+=1
        return out+left[i:]+right[j:],count
    return str(merge(values)[1])+'\n'


def render(points):
    return str(len(points))+'\n'+''.join(f'{x} {y}\n' for x,y in points)


def cases(seed):
    rng=random.Random(1000006+seed)
    yield SAMPLE_IN
    yield render([(0,0),(0,0),(1,1),(1,2)])
    yield render([(10**9,10**9)])
    yield render([(0,i) for i in range(30)])
    yield render([(i,0) for i in range(31)])
    yield render([(i,i) for i in range(32)])
    yield render([(i,33-i) for i in range(33)])
    yield render([(5,5)]*34)
    for i in range(8,18):
        points=[(rng.randrange(10 if i%2 else 10**9+1),rng.randrange(10 if i%2 else 10**9+1)) for _ in range(i*7)]
        yield render(points)
    yield render([(0,0)]*200000)
    yield render([(i,i) for i in range(200000)])
    yield render([(rng.randrange(10**9+1),rng.randrange(10**9+1)) for _ in range(200000)])

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

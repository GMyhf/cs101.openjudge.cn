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

SAMPLE_IN = '5\n3\n1 2 1\n5\n1 2 2 3 2\n3\n1 1 2\n4\n1 2 2 1\n10\n1 1 2 2 3 3 4 4 5 5\n'
SAMPLE_OUT = 'YES\nYES\nNO\nYES\nNO\n'


def parse(text):
    lines=text.splitlines(); t=int(lines[0]); rows=[]
    if len(lines)!=1+2*t: raise ValueError('行数')
    for i in range(t):
        n=int(lines[1+2*i]); row=list(map(int,lines[2+2*i].split()))
        if len(row)!=n: raise ValueError('长度')
        rows.append(row)
    return rows


def valid(text):
    try:
        rows=parse(text)
        return 1<=len(rows)<=20 and sum(map(len,rows))<=500000 and all(len(r)>=1 and all(1<=x<=200000 for x in r) for r in rows)
    except (ValueError,IndexError):
        return False


def oracle(text):
    """按值记录所有出现的位置，检查最大最小位置距离。"""
    answer=[]
    for row in parse(text):
        positions={}
        for i,x in enumerate(row): positions.setdefault(x,[]).append(i)
        answer.append('YES' if any(max(p)-min(p)>=2 for p in positions.values()) else 'NO')
    return '\n'.join(answer)+'\n'


def render(rows):
    return str(len(rows))+'\n'+''.join(str(len(r))+'\n'+' '.join(map(str,r))+'\n' for r in rows)


def cases(seed):
    rng=random.Random(1000008+seed)
    yield SAMPLE_IN
    yield render([[1]])
    yield render([[1,1]])
    yield render([[1,2,1]])
    yield render([[1,1,1]])
    yield render([[1,2,2]])
    for i in range(6,18):
        yield render([[rng.randint(1,10+i) for _ in range(3+i*j)] for j in range(1,5)])
    yield render([[x for x in range(1,200001) for _ in range(2)]])
    yield render([[200000]*500000])
    yield render([list(range(1,200001))+[1]])

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

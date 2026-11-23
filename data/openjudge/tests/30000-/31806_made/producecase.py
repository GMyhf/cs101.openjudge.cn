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

from collections import Counter
SAMPLE_IN = '4 2 2 10\ncbaa\nac\nb c\na a\n0\n1\n2\n3\n4\n5\n6\n7\n8\n9\n'
SAMPLE_OUT = 'c\na\nc\nc\nb\na\na\nc\na\nc\n'


def parse(text):
    lines = text.splitlines()
    na, nb, k, q = map(int, lines[0].split())
    return na, nb, k, q, lines[1], lines[2], [tuple(x.split()) for x in lines[3:3+k]], list(map(int, lines[3+k:]))


def valid(text):
    try:
        na, nb, k, q, a, b, ban, queries = parse(text)
        if not (1 <= na <= 200000 and 1 <= nb <= 200000 and 0 <= k <= 676 and 1 <= q <= 100000):
            return False
        if len(text.splitlines()) != 3+k+q or len(a) != na or len(b) != nb or len(queries) != q:
            return False
        if any(not 'a' <= c <= 'z' for c in a+b) or any(len(x) != 2 or any(len(c) != 1 or not 'a' <= c <= 'z' for c in x) for x in ban):
            return False
        ca, cb = Counter(a), Counter(b)
        length = 2 * (na*nb - sum(ca[x]*cb[y] for x, y in set(ban)))
        return all(0 <= t < length for t in queries)
    except (ValueError, IndexError):
        return False


def render(a, b, ban, queries):
    return f'{len(a)} {len(b)} {len(ban)} {len(queries)}\n{a}\n{b}\n' + ''.join(f'{x} {y}\n' for x,y in ban) + ''.join(f'{t}\n' for t in queries)


def oracle(text):
    na, nb, k, q, a, b, ban, queries = parse(text)
    if na*nb > 100000:
        return None
    banned = set(ban)
    c = ''.join(x+y for x in a for y in b if (x,y) not in banned)
    return ''.join(c[t]+'\n' for t in queries)


def cases(seed):
    rng = random.Random(1000004 + seed)
    yield SAMPLE_IN
    yield render('a','b',[],[0,1])
    yield render('baaa','a',[('b','a')],[0,1,4,5])
    yield render('aaab','a',[('a','a')],[0,1])
    yield render('a','baaa',[('a','b')],[0,1,4,5])
    yield render('a','aaab',[('a','a')],[0,1])
    for i in range(6,21):
        size = 200000 if i in (18,19,20) else 10+i
        a = ''.join(rng.choices('abcxyz',k=size))
        b = ''.join(rng.choices('abcxyz',k=size if i != 20 else 1))
        ban = [(x,y) for x in 'abcxyz' for y in 'abcxyz' if rng.random() < .4] if i % 3 else []
        ca,cb=Counter(a),Counter(b)
        length=2*(len(a)*len(b)-sum(ca[x]*cb[y] for x,y in ban))
        if not length:
            ban=[]
            length=2*len(a)*len(b)
        queries=[0,1,length-2,length-1] + [rng.randrange(length) for _ in range(99996 if i==19 else i)]
        yield render(a,b,ban,queries)

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

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

SAMPLE_IN = 'baaababaab\n0001010000\n'
SAMPLE_OUT = 'aba\n'


def valid(text):
    lines=text.splitlines()
    return len(lines)==2 and 1<=len(lines[0])<=1000000 and len(lines[0])==len(lines[1]) and all('a'<=c<='z' for c in lines[0]) and set(lines[1])<={'0','1'}


def possible(s,p):
    """小规模穷举全部子串，给不可解的 -1 提供独立依据。"""
    if '1' not in p: return True
    first=p.index('1')
    for length in range(1,len(s)-first+1):
        t=s[first:first+length]
        if ''.join('1' if s.startswith(t,i) else '0' for i in range(len(s)))==p:
            return True
    return False


def oracle(text):
    s,p=text.split()
    if len(s)<=100:
        answer=reference.solve(text).strip()
        assert (answer!='-1')==possible(s,p), (s,p,answer)
    return None


def render(s,p):
    return s+'\n'+p+'\n'


def mask(s,t):
    # 生成时使用 Python 内建 startswith，仅用于短模式或小数据。
    return ''.join('1' if s.startswith(t,i) else '0' for i in range(len(s)))


def cases(seed):
    rng=random.Random(1000007+seed)
    yield SAMPLE_IN
    yield render('zqjzqj','000000')
    yield render('zqjzqj','100001')
    yield render('a','1')
    yield render('a','0')
    yield render('aaaaa','11110')
    yield render('aaaaaa','010100')
    yield render('ababa','10100')
    yield render('abcab','10000')
    yield render('ababab','001010')
    for i in range(10,18):
        s=''.join(rng.choices('abcz',k=15+i))
        p=mask(s,s[3:3+i//2]) if i%2 else ''.join(rng.choices('01',k=len(s)))
        yield render(s,p)
    yield render('a'*1000000,'1'*999999+'0')
    yield render('ab'*500000,'10'*499999+'00')
    yield render('z'*1000000,'0'*1000000)

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

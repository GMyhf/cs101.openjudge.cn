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

SAMPLE_IN = 'sycstudiosyc\n'
SAMPLE_OUT = '6\n'


def valid(text):
    lines=text.splitlines()
    return len(lines)==1 and 1<=len(lines[0])<=100000 and all('a'<=c<='z' for c in lines[0])


def oracle(text):
    """用内建串比较按定义穷举周期；大串先用 Z 函数找周期。"""
    s=text.strip(); n=len(s)
    if n<=1000:
        p=next(p for p in range(1,n+1) if s[p:]==s[:n-p])
    else:
        z=[0]*n; l=r=0
        for i in range(1,n):
            if i<=r: z[i]=min(r-i+1,z[i-l])
            while i+z[i]<n and s[z[i]]==s[i+z[i]]: z[i]+=1
            if i+z[i]-1>r: l,r=i,i+z[i]-1
        p=next((i for i in range(1,n) if z[i]==n-i),n)
    return str(p if p==n else (-n)%p)+'\n'


def cases(seed):
    rng=random.Random(1000009+seed)
    yield SAMPLE_IN
    for s in ['a','aa','ab','aba','abab','abcab','abcabc','aaaaab','aaaaaba','abcabca']:
        yield s+'\n'
    for i in range(11,18):
        unit=''.join(rng.choices('abcz',k=i))
        yield (unit*5)[:i*4+3]+'\n'
    yield 'a'*100000+'\n'
    yield 'a'*99999+'b\n'
    yield ('abcdefg'*14286)[:100000]+'\n'

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

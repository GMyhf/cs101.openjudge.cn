"""仓库自产数据：按完整题面构造边界与典型错解反例；固定种子可复现。"""
import importlib.util
from pathlib import Path
import random
import re
spec=importlib.util.spec_from_file_location('reference',Path(__file__).with_name('samplecode.py'))
reference=importlib.util.module_from_spec(spec)
spec.loader.exec_module(reference)
NUMBER=31178
SAMPLE_IN='Hello, OJ Inject!\n'
SAMPLE_OUT='Hello, OJ Inject!\n'

def valid(text):
    return isinstance(text,str) and re.fullmatch(r'[^\r\n]{1,100}(?:\r?\n)?',text) is not None

def generate(number,seed):
    assert number==31178 and 1<=seed<=20
    shapes=['a','Z','0','!',' a ','two words','word   spaces','a\tb', ' '*100,
            'x'*100,'a'*99+'Z','<> & \" \\','Hello, OJ Inject?','0123456789'*10]
    if seed<=len(shapes): given=shapes[seed-1]
    else:
        rng=random.Random(number*100+seed);given=''.join(rng.choice('Aa 09!?>') for _ in range(seed*5))
    return given+'\n'

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

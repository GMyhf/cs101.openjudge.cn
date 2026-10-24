"""仓库自产数据：按完整题面构造边界与典型错解反例；固定种子可复现。"""
import importlib.util
from pathlib import Path
import random
import re
spec=importlib.util.spec_from_file_location('reference',Path(__file__).with_name('samplecode.py'))
reference=importlib.util.module_from_spec(spec)
spec.loader.exec_module(reference)
NUMBER=31200
SAMPLE_IN='100 500\n'
SAMPLE_OUT='153 370 371 407\n'

def valid(text):
    try:
        lines=text.splitlines()
        if len(lines)!=1 or len(lines[0].split())!=2: return False
        a,b=map(int,lines[0].split());return 100<=a<=b<=999
    except (ValueError,TypeError): return False

def generate(number,seed):
    assert number==31200 and 1<=seed<=20
    ranges=[(100,999),(153,153),(370,370),(371,371),(407,407),(100,100),(999,999),
            (154,369),(372,406),(408,999),(152,153),(153,154),(369,370),(370,371),
            (371,372),(406,407),(407,408),(100,152),(153,407),(370,407)]
    a,b=ranges[seed-1];return f'{a} {b}\n'

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

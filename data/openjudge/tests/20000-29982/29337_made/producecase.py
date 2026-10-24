"""仓库自产数据：按完整题面构造边界与典型错解反例；固定种子可复现。"""
import importlib.util
from pathlib import Path
import random
import re
spec=importlib.util.spec_from_file_location('reference',Path(__file__).with_name('samplecode.py'))
reference=importlib.util.module_from_spec(spec)
spec.loader.exec_module(reference)
NUMBER=29337
SAMPLE_IN='1 1 1 1 1\n3\n'
SAMPLE_OUT='5\n'

def valid(text):
    try:
        lines=text.splitlines()
        if len(lines)!=2: return False
        nums=list(map(int,lines[0].split())); target=int(lines[1])
        return 1<=len(nums)<=20 and all(0<=v<=1000 for v in nums) and sum(nums)<=1000 and -1000<=target<=1000
    except (ValueError,TypeError): return False

def generate(number,seed):
    assert number==29337 and 1<=seed<=20
    vectors=[([0]*20,0),([0],1),([1000],1000),([1000],-1000),([1],0),([1],1),
             ([1,1],0),([1,2,3],-6),([1,2,3],5),([0,0,1],1),([50]*20,0),
             ([1]*20,20),([1]*20,-20),([0]*19+[1],-1),([999,1],1000)]
    if seed<=len(vectors): nums,target=vectors[seed-1]
    else:
        rng=random.Random(number*100+seed); nums=[rng.randrange(40) for _ in range(20)]
        target=sum(v*rng.choice((-1,1)) for v in nums)
    return ' '.join(map(str,nums))+f'\n{target}\n'

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

"""仓库自产数据：按完整题面构造边界与典型错解反例；固定种子可复现。"""
import importlib.util
from pathlib import Path
import random
import re
spec=importlib.util.spec_from_file_location('reference',Path(__file__).with_name('samplecode.py'))
reference=importlib.util.module_from_spec(spec)
spec.loader.exec_module(reference)
NUMBER=29894
SAMPLE_IN='5 7 32 4\n'
SAMPLE_OUT='13\n'

def valid(text):
    try:
        lines=text.splitlines()
        if len(lines)!=1 or len(lines[0].split())!=4: return False
        a,n,m,x=map(int,lines[0].split())
        if not (a>=0 and n>=4 and m>=0 and 1<=x<n): return False
        ca,cb=reference.coefficients(n-1)
        return (m==ca*a if cb==0 else m>ca*a and (m-ca*a)%cb==0)
    except (ValueError,TypeError): return False

def passengers(a,n,second):
    boarding=[0,a,second]; counts=[0,a,a]
    for station in range(3,n):
        boarding.append(boarding[-1]+boarding[-2])
        counts.append(counts[-1]+boarding[-1]-boarding[-2])
    return counts

def generate(number,seed):
    assert number in (29893,29894) and 1<=seed<=20
    vectors=[(1,5,1,1),(7,5,1,2),(4,4,9,3),(3,5,1,4),(3,5,7,4),
             (1,20,1,19),(1,20,1,18),(100,7,1,1),(5,7,3,2),(5,7,3,6)]
    if seed<=len(vectors): a,n,second,x=vectors[seed-1]
    else:
        rng=random.Random(number*100+seed);a=rng.randint(1,30);n=rng.randint(5,15);second=rng.randint(1,20);x=rng.randint(1,n-1)
    counts=passengers(a,n,second)
    return f'{a} {n} {counts[n-1]} {x}\n'

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

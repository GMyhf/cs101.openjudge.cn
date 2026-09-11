import random, subprocess
from pathlib import Path
ROOT = Path(__file__).parent
SAMPLE = '4\n0 0 0 1 0 0 1 1 0 1 1 1\n'
def case(i):
    if i == 0: return SAMPLE
    rng = random.Random(370200 + i); n = 2 + i % 9; pts=[]; used=set()
    while len(pts) < n:
        p=tuple(rng.randrange(101) for _ in range(3))
        if p not in used: used.add(p); pts.append(p)
    return str(n) + '\n' + ' '.join(map(str, sum((list(p) for p in pts), []))) + '\n'
for i in range(21):
    inp=case(i); out=subprocess.run(['python3',str(ROOT/'samplecode.py')],input=inp,text=True,capture_output=True,check=True).stdout
    (ROOT/'data'/f'{i}.in').write_text(inp); (ROOT/'data'/f'{i}.out').write_text(out)

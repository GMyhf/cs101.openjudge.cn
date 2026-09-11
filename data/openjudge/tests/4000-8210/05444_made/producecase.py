import random, subprocess
from pathlib import Path
ROOT = Path(__file__).parent
SAMPLE = '7\n4 5 3 6 2 7 1\n'
def case(i):
    if i == 0: return SAMPLE
    rng=random.Random(544400+i); n=1+i%18
    if i%4==0:
        seq=list(range(1,n+1)); rng.shuffle(seq)
    elif i%4==1:
        seq=list(range(n,0,-1))
    elif i%4==2:
        seq=list(range(1,n+1)); seq[-1]=n+1
    else:
        seq=list(range(1,n+1)); seq[n//2]=seq[max(0,n//2-1)]
    return str(n)+'\n'+' '.join(map(str,seq))+'\n'
for i in range(21):
    inp=case(i); out=subprocess.run(['python3',str(ROOT/'samplecode.py')],input=inp,text=True,capture_output=True,check=True).stdout
    (ROOT/'data'/f'{i}.in').write_text(inp); (ROOT/'data'/f'{i}.out').write_text(out)

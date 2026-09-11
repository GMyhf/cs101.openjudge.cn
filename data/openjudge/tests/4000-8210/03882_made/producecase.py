import random, subprocess
from pathlib import Path
ROOT=Path(__file__).parent
SAMPLE='3\n3+5*8\n(3+5)*8\n(23+34*45/(5+6+7))\n'
def case(i):
    if i==0:return SAMPLE
    rng=random.Random(388200+i); expr=[]
    expr.append(f'{i+2}+{i}*3-{i%5+1}')
    expr.append(f'({i+3}+{i%7+2})*({i%9+3}-{i%4+1})')
    expr.append(f'({i+20}*{i%11+2})/({i%6+2})')
    if i%3==0: expr.append('100000*100000+2147483647')
    if i%3==1: expr.append('(5-1000000000)/3')
    if i%3==2: expr.append('2147483647+1')
    if i>12: expr.append('+'.join(str(rng.randrange(1,100000)) for _ in range(8)))
    return str(len(expr))+'\n'+'\n'.join(expr)+'\n'
for i in range(21):
    inp=case(i); out=subprocess.run(['python3',str(ROOT/'samplecode.py')],input=inp,text=True,capture_output=True,check=True).stdout
    (ROOT/'data'/f'{i}.in').write_text(inp); (ROOT/'data'/f'{i}.out').write_text(out)

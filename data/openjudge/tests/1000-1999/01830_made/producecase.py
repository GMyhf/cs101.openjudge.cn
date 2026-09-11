import random, subprocess
from pathlib import Path
ROOT = Path(__file__).parent
SAMPLE = '''2
3
0 0 0
1 1 1
1 2
1 3
2 1
2 3
3 1
3 2
0 0
3
0 0 0
1 0 1
1 2
2 1
0 0
'''
def case(i):
    if i == 0: return SAMPLE
    rng = random.Random(183000 + i); k = 1 + i % 3; chunks = [str(k)]
    for c in range(k):
        n = 1 + (i + c * 3) % 8; start = [rng.randrange(2) for _ in range(n)]; target = [rng.randrange(2) for _ in range(n)]
        chunks += [str(n), ' '.join(map(str, start)), ' '.join(map(str, target))]
        for a in range(n):
            for b in range(n):
                if a != b and rng.random() < (0.2 + 0.08 * ((i+c) % 4)): chunks.append(f'{a+1} {b+1}')
        chunks.append('0 0')
    return '\n'.join(chunks) + '\n'
for i in range(21):
    inp = case(i); out = subprocess.run(['python3', str(ROOT/'samplecode.py')], input=inp, text=True, capture_output=True, check=True).stdout
    (ROOT/'data'/f'{i}.in').write_text(inp); (ROOT/'data'/f'{i}.out').write_text(out)

import random
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent
SAMPLE = "I\n4\n3\nI am a student .\nI live in Beijing and I love Bejing\nI also love travelling, life in there\nBeijing is beautiful\n"

def generate(i):
    if i == 0: return SAMPLE
    rng = random.Random(3119300 + i)
    words = ['alpha', 'beta', 'gamma', 'delta', 'omega', f'w{i}']
    n = 1 + (i * 7) % 9
    rows = []
    for line in range(n):
        rows.append(' '.join(rng.choice(words[:3 + i % 4]) for _ in range(1 + rng.randrange(7))))
    query = (words[i % 3] if i % 4 else 'missing')
    rank = 1 + (i * 3) % (sum(len(r.split()) for r in rows) + 2)
    return f'{query}\n{n}\n{rank}\n' + '\n'.join(rows) + '\n'

for i in range(21):
    case = generate(i)
    out = subprocess.run(['python3', str(ROOT / 'samplecode.py')], input=case, text=True, capture_output=True, check=True).stdout
    (ROOT / 'data' / f'{i}.in').write_text(case)
    (ROOT / 'data' / f'{i}.out').write_text(out)

import random, subprocess
from pathlib import Path
SAMPLE_IN='1\n20 1 10 10 1000\n20 20 30 10 20\n5 5 5 5 5\n'
def g3433(r):
    m = r.randint(20, 100); n = r.randint(1, 3); t = r.randint(0, 180)
    hp = [r.randint(10, 50) for _ in range(5)]
    atk = [r.randint(5, 50) for _ in range(5)]
    return f"1\n{m} {n} {t}\n{' '.join(map(str, hp))}\n{' '.join(map(str, atk))}\n"

root=Path(__file__).parent; binary=root/"reference"
subprocess.run(["g++", "-std=c++17", "-O2", str(root/"samplecode_ac.cpp"), "-o", str(binary)], check=True)
for i in range(21):
 c=SAMPLE_IN if i == 0 else g3433(random.Random(3433+i))
 p=subprocess.run([str(binary)], input=c, text=True, capture_output=True, check=True)
 (root/"data"/f"{i}.in").write_text(c); (root/"data"/f"{i}.out").write_text(p.stdout)

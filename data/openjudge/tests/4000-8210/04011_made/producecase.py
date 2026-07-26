import random, subprocess, tempfile
from pathlib import Path
SAMPLE_IN='4 4\n0 1 1\n0 2 2\n1 3 3\n2 3 1\n2\n0.01 0.1\n0.5 0.8\n0.5 0.8\n0.7 0.9\n0 0\n'
def g4011(r):
    n = r.randint(2, 7)
    roads = [f"{i} {i+1} {r.randint(1, 6)}" for i in range(n - 1)]
    p = r.randint(1, 3)
    rows = [" ".join(f"{r.random():.4f}" for _ in range(p)) for _ in range(n)]
    return f"{n} {n-1}\n" + "\n".join(roads) + f"\n{p}\n" + "\n".join(rows) + "\n0 0\n"

root=Path(__file__).parent
with tempfile.TemporaryDirectory() as folder:
 binary=Path(folder)/"reference"
 subprocess.run(["g++", "-std=c++17", "-O2", str(root/"samplecode_ac.cpp"), "-o", str(binary)], check=True)
 for i in range(21):
  c=SAMPLE_IN if i == 0 else g4011(random.Random(4011+i))
  p=subprocess.run([str(binary)], input=c, text=True, capture_output=True, check=True)
  (root/"data"/f"{i}.in").write_text(c); (root/"data"/f"{i}.out").write_text(p.stdout)

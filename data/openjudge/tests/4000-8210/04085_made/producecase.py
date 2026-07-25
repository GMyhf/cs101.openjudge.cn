import random,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\na=list(map(int,sys.stdin.read().split())); n=a[0]\nprint(" ".join(map(str,sorted(set(a[1:n+1])))))'
SAMPLE_IN='3\n4 4 2\n'
def g4085(r):
    n = r.randint(1, 80)
    return f"{n}\n" + " ".join(str(r.randint(0, 10_000)) for _ in range(n)) + "\n"

with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
 handle.write(REFERENCE_SOURCE);handle.flush()
 root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
 for index in range(21):
  if index==0: content=SAMPLE_IN
  else:
   for attempt in range(100):
    content=g4085(random.Random(4085+index+attempt*1000))
    if content not in seen: break
   else: raise AssertionError("insufficient diversity")
  seen.append(content)
  result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
  (root/f"{index}.in").write_text(content,encoding="utf-8")
  (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")

import random,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\nm,n=map(int,sys.stdin.read().split()); dp=[1]*n\nfor _ in range(m-1):\n    for j in range(1,n): dp[j]+=dp[j-1]\nprint(dp[n-1])'
SAMPLE_IN='2 3\n'
def g3717(r):
    m=r.randint(1, 19); n=r.randint(1, 20-m)
    return f"{m} {n}\n"

with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
 handle.write(REFERENCE_SOURCE);handle.flush()
 root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
 for index in range(21):
  if index==0: content=SAMPLE_IN
  else:
   for attempt_no in range(100):
    content=g3717(random.Random(3717+index+attempt_no*1000))
    if content not in seen: break
   else: raise AssertionError("insufficient diversity")
  seen.append(content)
  result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
  (root/f"{index}.in").write_text(content,encoding="utf-8")
  (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")

import random,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\na=list(map(int,sys.stdin.read().split())); n,t=a[:2]; dp=[0]*(t+1); dp[0]=1\nfor x in a[2:2+n]:\n    for s in range(t,x-1,-1): dp[s]+=dp[s-x]\nprint(dp[t])'
SAMPLE_IN='5 5\n1 2 3 4 5\n'
def g4004(r):
    n = r.randint(1, 20)
    values = [r.randint(1, 80) for _ in range(n)]
    return f"{n} {r.randint(1, 1000)}\n" + " ".join(map(str, values)) + "\n"

with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
 handle.write(REFERENCE_SOURCE);handle.flush()
 root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
 for index in range(21):
  if index==0: content=SAMPLE_IN
  else:
   for attempt in range(100):
    content=g4004(random.Random(4004+index+attempt*1000))
    if content not in seen: break
   else: raise AssertionError("insufficient diversity")
  seen.append(content)
  result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
  (root/f"{index}.in").write_text(content,encoding="utf-8")
  (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")

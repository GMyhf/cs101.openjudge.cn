import random,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\na=list(map(int,sys.stdin.read().split())); cap,n=a[:2]; dp=[0]*(cap+1)\nfor p,v in zip(a[2::2],a[3::2]):\n for x in range(cap,p-1,-1): dp[x]=max(dp[x],dp[x-p]+v)\nprint(dp[cap])'
SAMPLE_IN='90 4\n20 25\n30 20\n40 50\n10 18\n'
def g3714(r):
    n, cap = r.randint(1, 12), r.randint(1, 80)
    items = [(r.randint(1, 30), r.randint(1, 30)) for _ in range(n)]
    return f"{cap} {n}\n" + "\n".join(f"{p} {v}" for p, v in items) + "\n"

with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
 handle.write(REFERENCE_SOURCE);handle.flush()
 root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
 for index in range(21):
  if index==0:content=SAMPLE_IN
  else:
   for attempt in range(100):
    content=g3714(random.Random(3714+index+attempt*1000))
    if content not in seen:break
   else:raise AssertionError("insufficient diversity")
  seen.append(content)
  result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
  (root/f"{index}.in").write_text(content,encoding="utf-8")
  (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")

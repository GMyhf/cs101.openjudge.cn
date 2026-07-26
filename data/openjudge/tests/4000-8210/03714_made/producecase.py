import random,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\na=list(map(int,sys.stdin.read().split())); i=0; out=[]\nwhile i+1<len(a):\n cap,n=a[i],a[i+1]; i+=2; dp=[0]*(cap+1)\n for _ in range(n):\n  p,v=a[i],a[i+1]; i+=2\n  for x in range(cap,p-1,-1): dp[x]=max(dp[x],dp[x-p]+v)\n out.append(str(dp[cap]))\nprint("\\n".join(out))'
SAMPLE_IN='90 4\n20 25\n30 20\n40 50\n10 18\n'
def g3714(r):
    blocks=[]
    for _ in range(r.randint(1, 3)):
        n, cap = r.randint(1, 12), r.randint(1, 80)
        items = [(r.randint(1, 30), r.randint(1, 30)) for _ in range(n)]
        blocks.append(f"{cap} {n}\n" + "\n".join(f"{p} {v}" for p, v in items))
    return "\n".join(blocks) + "\n"

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

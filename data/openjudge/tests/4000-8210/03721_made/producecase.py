import random,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\na=list(map(int,sys.stdin.read().split())); n=a[0]; v=a[1:1+n]; ans=0\nfor i,x in enumerate(v):\n    seen=set()\n    for j,y in enumerate(v):\n        if j!=i and x-y in seen: ans+=1; break\n        if j!=i: seen.add(y)\nprint(ans)'
SAMPLE_IN='4\n1 2 3 4\n'
def g3721(r):
    n=r.randint(3, 30)
    return str(n)+"\n"+" ".join(str(r.randint(1,10000)) for _ in range(n))+"\n"

with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
 handle.write(REFERENCE_SOURCE);handle.flush()
 root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
 for index in range(21):
  if index==0: content=SAMPLE_IN
  else:
   for attempt_no in range(100):
    content=g3721(random.Random(3721+index+attempt_no*1000))
    if content not in seen: break
   else: raise AssertionError("insufficient diversity")
  seen.append(content)
  result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
  (root/f"{index}.in").write_text(content,encoding="utf-8")
  (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")

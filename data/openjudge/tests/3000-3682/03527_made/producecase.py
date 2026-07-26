import random,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\nfrom collections import Counter\ndef ok(v):\n if len(v)<2 or (len(v)-2)%3: return "XIANGGONG"\n def f(c,p):\n  if not sum(c.values()): return p is not None\n  x=min(k for k,v in c.items() if v)\n  if p is None and c[x]>=2:\n   c[x]-=2\n   if f(c,x): return True\n   c[x]+=2\n  if c[x]>=3:\n   c[x]-=3\n   if f(c,p): return True\n   c[x]+=3\n  if c.get(x+1,0) and c.get(x+2,0):\n   for y in (x,x+1,x+2): c[y]-=1\n   if f(c,p): return True\n   for y in (x,x+1,x+2): c[y]+=1\n  return None\n return "HU" if f(Counter(v),None) else "BUHU"\nout=[]\nfor line in sys.stdin:\n v=list(map(int,line.split()))\n if v and v[0]==0: break\n out.append(ok(v))\nprint("\\n".join(out))'
SAMPLE_IN='1 2\n4 4\n1 1 1 2 3 4 5 6 7 8 9 9 9\n1 1 1 2 3 4 5 6 7 8 9 9 9 9\n0\n'
def g3527(r):
    return "\n".join(" ".join(str(r.randint(1, 9)) for _ in range(r.choice([4,5,7,8,10,11,13,14]))) for _ in range(r.randint(1, 4))) + "\n0\n"

with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
 handle.write(REFERENCE_SOURCE);handle.flush()
 root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
 for index in range(21):
  if index==0:content=SAMPLE_IN
  else:
   for attempt in range(100):
    content=g3527(random.Random(3527+index+attempt*1000))
    if content not in seen:break
   else:raise AssertionError("insufficient diversity")
  seen.append(content)
  result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
  (root/f"{index}.in").write_text(content,encoding="utf-8")
  (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")

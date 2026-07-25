import random,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\ndef pos(r,c):\n t,l,b,rr=0,0,r-1,c-1\n while t<=b and l<=rr:\n  for j in range(l,rr+1): yield t,j\n  t+=1\n  for i in range(t,b+1): yield i,rr\n  rr-=1\n  if t<=b:\n   for j in range(rr,l-1,-1): yield b,j\n   b-=1\n  if l<=rr:\n   for i in range(b,t-1,-1): yield i,l\n   l+=1\nr,c,msg=sys.stdin.read().rstrip("\\n").split(" ",2); r,c=int(r),int(c)\nbits="".join(format(0 if x==" " else ord(x)-64,"05b") for x in msg).ljust(r*c,"0")\ng=[["0"]*c for _ in range(r)]\nfor (i,j),x in zip(pos(r,c),bits): g[i][j]=x\nprint("".join("".join(x) for x in g))'
SAMPLE_IN='4 4 ACM\n'
def g3421(r):
    rows, cols = r.randint(1, 8), r.randint(1, 8)
    msg = "".join(r.choice(" ABCXYZ") for _ in range(r.randint(0, rows * cols // 5)))
    return f"{rows} {cols} {msg}\n"

with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
 handle.write(REFERENCE_SOURCE);handle.flush()
 root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
 for index in range(21):
  if index==0:content=SAMPLE_IN
  else:
   for attempt in range(100):
    content=g3421(random.Random(3421+index+attempt*1000))
    if content not in seen:break
   else:raise AssertionError("insufficient diversity")
  seen.append(content)
  result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
  (root/f"{index}.in").write_text(content,encoding="utf-8")
  (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")

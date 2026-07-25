import random,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\na=sys.stdin.read().split(); s="".join(a[1:])\nl,rr,out=0,len(s)-1,[]\nwhile l<=rr:\n if s[l]<s[rr]: out.append(s[l]); l+=1\n elif s[l]>s[rr]: out.append(s[rr]); rr-=1\n else:\n  i,j=l,rr\n  while i<=j and s[i]==s[j]: i+=1; j-=1\n  if i>j or s[i]<=s[j]: out.append(s[l]); l+=1\n  else: out.append(s[rr]); rr-=1\nprint("".join(out))'
SAMPLE_IN='6\nA\nC\nD\nB\nC\nB\n'
def g3376(r):
    n = r.randint(1, 24)
    return str(n) + "\n" + "\n".join(r.choice("ABCXYZ") for _ in range(n)) + "\n"

with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
 handle.write(REFERENCE_SOURCE);handle.flush()
 root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
 for index in range(21):
  if index==0:content=SAMPLE_IN
  else:
   for attempt in range(100):
    content=g3376(random.Random(3376+index+attempt*1000))
    if content not in seen:break
   else:raise AssertionError("insufficient diversity")
  seen.append(content)
  result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
  (root/f"{index}.in").write_text(content,encoding="utf-8")
  (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")

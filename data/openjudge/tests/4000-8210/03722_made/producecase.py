import random,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\nn,m=map(int,sys.stdin.read().split()); answer=-1\nfor a in range(1,m):\n    if n%a==0 and n%(m-a)==0: answer=a; break\nprint(answer)'
SAMPLE_IN='35 10\n'
def g3722(r):
    n=r.randint(1, 1000000); m=r.randint(2, 200)
    return f"{n} {m}\n"

with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
 handle.write(REFERENCE_SOURCE);handle.flush()
 root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
 for index in range(21):
  if index==0: content=SAMPLE_IN
  else:
   for attempt_no in range(100):
    content=g3722(random.Random(3722+index+attempt_no*1000))
    if content not in seen: break
   else: raise AssertionError("insufficient diversity")
  seen.append(content)
  result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
  (root/f"{index}.in").write_text(content,encoding="utf-8")
  (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")

import random,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\na=list(map(int,sys.stdin.read().split()))\nodd=sorted((x for x in a if x%2),reverse=True)\neven=sorted(x for x in a if not x%2)\nprint(" ".join(map(str,odd+even)))'
SAMPLE_IN='4 7 3 13 11 12 0 47 34 98\n'
def g7745(r):
    return " ".join(str(r.randint(0, 100)) for _ in range(10)) + "\n"

with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
 handle.write(REFERENCE_SOURCE);handle.flush()
 root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
 for index in range(21):
  if index==0: content=SAMPLE_IN
  else:
   for attempt in range(100):
    content=g7745(random.Random(7745+index+attempt*1000))
    if content not in seen: break
   else: raise AssertionError("insufficient diversity")
  seen.append(content)
  result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
  (root/f"{index}.in").write_text(content,encoding="utf-8")
  (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")

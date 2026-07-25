import random,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\nprint(" ".join(sys.stdin.read().split()[::-1]))'
SAMPLE_IN="123? you can cage a swallow can't you but you can't swallow a cage can you\n"
def g27706(r):
    words = [r.choice(["alpha", "B2", "x!", "can't", "42", "node"]) for _ in range(r.randint(1, 20))]
    return " ".join(words) + "\n"

with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
 handle.write(REFERENCE_SOURCE);handle.flush()
 root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
 for index in range(21):
  if index==0: content=SAMPLE_IN
  else:
   for attempt in range(100):
    content=g27706(random.Random(27706+index+attempt*1000))
    if content not in seen: break
   else: raise AssertionError("insufficient diversity")
  seen.append(content)
  result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
  (root/f"{index}.in").write_text(content,encoding="utf-8")
  (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")

import random,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\na=sys.stdin.read().split(); t=int(a[0])\nprint("\\n".join(str(int(x,16)) for x in a[1:t+1]))'
SAMPLE_IN='4\nA\nF\nFFFE\n10001\n'
def g4003(r):
    digits = "0123456789ABCDEF"
    t = r.randint(1, 8)
    return str(t) + "\n" + "\n".join(
        "".join(r.choice(digits) for _ in range(r.randint(1, 8))).lstrip("0") or "0"
        for _ in range(t)
    ) + "\n"

with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
 handle.write(REFERENCE_SOURCE);handle.flush()
 root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
 for index in range(21):
  if index==0: content=SAMPLE_IN
  else:
   for attempt in range(100):
    content=g4003(random.Random(4003+index+attempt*1000))
    if content not in seen: break
   else: raise AssertionError("insufficient diversity")
  seen.append(content)
  result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
  (root/f"{index}.in").write_text(content,encoding="utf-8")
  (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")

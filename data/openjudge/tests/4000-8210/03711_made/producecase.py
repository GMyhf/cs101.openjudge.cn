import random,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\na,b=sys.stdin.read().split()\nif len(a)<len(b): a,b=b,a\nprint("true" if b in a+a else "false")'
SAMPLE_IN='AABCD CDAA\n'
def g3711(r):
    long = ''.join(r.choice('ABCD') for _ in range(r.randint(1, 12)))
    short = ''.join(r.choice('ABCD') for _ in range(r.randint(1, len(long))))
    return f"{long} {short}\n" if r.random() < .5 else f"{short} {long}\n"

with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
 handle.write(REFERENCE_SOURCE);handle.flush()
 root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
 for index in range(21):
  if index==0:content=SAMPLE_IN
  else:
   for attempt in range(100):
    content=g3711(random.Random(3711+index+attempt*1000))
    if content not in seen:break
   else:raise AssertionError("insufficient diversity")
  seen.append(content)
  result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
  (root/f"{index}.in").write_text(content,encoding="utf-8")
  (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")

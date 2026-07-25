import random,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\nout=[]\nfor line in sys.stdin.read().splitlines()[1:]:\n    a,b=map(int,line.split()); carry=0; count=0\n    while a or b:\n        carry,a,b=(a%10+b%10+carry)//10,a//10,b//10\n        count += carry\n    out.append(str(count))\nprint("\\n".join(out))'
SAMPLE_IN='5\n1 9\n18 100\n8374 29\n999 1\n123 967\n'
def g28557(r):
    n = r.randint(1, 10)
    return str(n) + "\n" + "\n".join(
        f"{r.randint(1, 1_000_000_000)} {r.randint(1, 1_000_000_000)}"
        for _ in range(n)
    ) + "\n"

with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
 handle.write(REFERENCE_SOURCE);handle.flush()
 root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
 for index in range(21):
  if index==0: content=SAMPLE_IN
  else:
   for attempt in range(100):
    content=g28557(random.Random(28557+index+attempt*1000))
    if content not in seen: break
   else: raise AssertionError("insufficient diversity")
  seen.append(content)
  result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
  (root/f"{index}.in").write_text(content,encoding="utf-8")
  (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")

import random,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\ndef f(s):\n n=int(s,2); out=[]\n if not n:return "0"\n while n: out.append(str(n%3)); n//=3\n return "".join(out[::-1])\na=sys.stdin.read().split(); print("\\n".join(f(x) for x in a[1:]))'
SAMPLE_IN='2\n10110\n1011\n'
def g3709(r):
    return "5\n" + "\n".join("1" + "".join(r.choice("01") for _ in range(r.randint(0, 18))) for _ in range(5)) + "\n"

with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
 handle.write(REFERENCE_SOURCE);handle.flush()
 root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
 for index in range(21):
  if index==0:content=SAMPLE_IN
  else:
   for attempt in range(100):
    content=g3709(random.Random(3709+index+attempt*1000))
    if content not in seen:break
   else:raise AssertionError("insufficient diversity")
  seen.append(content)
  result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
  (root/f"{index}.in").write_text(content,encoding="utf-8")
  (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")

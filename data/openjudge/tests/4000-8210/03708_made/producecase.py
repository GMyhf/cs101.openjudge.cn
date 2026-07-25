import random,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\nfor x in sys.stdin.read().split()[1:]: print(bin(int(x)).count("1"))'
SAMPLE_IN='4\n2\n100\n1000\n66\n'
def g3708(r):
    return str(5) + "\n" + "\n".join(str(r.randint(1, 10**9)) for _ in range(5)) + "\n"

with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
 handle.write(REFERENCE_SOURCE);handle.flush()
 root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
 for index in range(21):
  if index==0:content=SAMPLE_IN
  else:
   for attempt in range(100):
    content=g3708(random.Random(3708+index+attempt*1000))
    if content not in seen:break
   else:raise AssertionError("insufficient diversity")
  seen.append(content)
  result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
  (root/f"{index}.in").write_text(content,encoding="utf-8")
  (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")

import random,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\ns=sys.stdin.read().strip()\nsign="-" if s.startswith("-") else ""\ndigits=s[1:] if sign else s\nprint(sign + digits[::-1].lstrip("0") or "0")'
SAMPLE_IN='123\n'
def g4029(r):
    value = r.randint(-1_000_000_000, 1_000_000_000)
    return f"{value}\n"

with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
 handle.write(REFERENCE_SOURCE);handle.flush()
 root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
 for index in range(21):
  if index==0: content=SAMPLE_IN
  else:
   for attempt in range(100):
    content=g4029(random.Random(4029+index+attempt*1000))
    if content not in seen: break
   else: raise AssertionError("insufficient diversity")
  seen.append(content)
  result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
  (root/f"{index}.in").write_text(content,encoding="utf-8")
  (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")

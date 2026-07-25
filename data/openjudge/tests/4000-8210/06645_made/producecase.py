import random,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\ns=sys.stdin.read().strip(); bits=[]\nwhile int(s):\n    q,rem=[],0\n    for ch in s:\n        rem=rem*10+ord(ch)-48\n        if q or rem>=2: q.append(str(rem//2)); rem%=2\n    s="".join(q) or "0"; bits.append(str(rem))\nprint("".join(bits[::-1]) or "0")'
SAMPLE_IN='123456789012345678901234567890\n'
def g6645(r):
    if r.random() < .15:
        value = 0
    else:
        value = r.randrange(1, 10**40)
    return f"{value}\n"

with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
 handle.write(REFERENCE_SOURCE);handle.flush()
 root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
 for index in range(21):
  if index==0: content=SAMPLE_IN
  else:
   for attempt in range(100):
    content=g6645(random.Random(6645+index+attempt*1000))
    if content not in seen: break
   else: raise AssertionError("insufficient diversity")
  seen.append(content)
  result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
  (root/f"{index}.in").write_text(content,encoding="utf-8")
  (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")

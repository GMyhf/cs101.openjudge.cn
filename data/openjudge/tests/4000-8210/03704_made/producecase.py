import random,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\nfor line in sys.stdin.read().splitlines():\n    bad=[" "]*len(line); stack=[]\n    for i,ch in enumerate(line):\n        if ch=="(": stack.append(i)\n        elif ch==")":\n            if stack: stack.pop()\n            else: bad[i]="?"\n    for i in stack: bad[i]="$"\n    print(line); print("".join(bad).rstrip())'
SAMPLE_IN='((ABCD(x)\n)(rttyy())sss)(\n'
def g3704(r):
    lines=[]
    for _ in range(r.randint(1, 5)):
        s="".join(r.choice("()ABCxyz") for _ in range(r.randint(1, 40)))
        lines.append(s)
    return "\n".join(lines)+"\n"

with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
 handle.write(REFERENCE_SOURCE);handle.flush()
 root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
 for index in range(21):
  if index==0: content=SAMPLE_IN
  else:
   for attempt_no in range(100):
    content=g3704(random.Random(3704+index+attempt_no*1000))
    if content not in seen: break
   else: raise AssertionError("insufficient diversity")
  seen.append(content)
  result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
  (root/f"{index}.in").write_text(content,encoding="utf-8")
  (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")

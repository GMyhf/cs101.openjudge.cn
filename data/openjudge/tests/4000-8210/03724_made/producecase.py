import random,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\ndays=[31,28,31,30,31,30,31,31,30,31,30,31]\ndef leap(y): return y%400==0 or y%4==0 and y%100!=0\nfor token in sys.stdin.read().split():\n    rem=int(token); y=1970\n    while rem >= (366 if leap(y) else 365)*86400: rem-=(366 if leap(y) else 365)*86400; y+=1\n    month=1\n    while True:\n        md=days[month-1]+(month==2 and leap(y))\n        if rem < md*86400: break\n        rem-=md*86400; month+=1\n    print(f"{y:04d}-{month:02d}-{rem//86400+1:02d} {(rem%86400)//3600:02d}:{(rem%3600)//60:02d}:{rem%60:02d}")'
SAMPLE_IN='10\n1234567890\n'
def g3724(r):
    return "\n".join(str(r.randint(0, 2**31-1)) for _ in range(r.randint(1, 8)))+"\n"

with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
 handle.write(REFERENCE_SOURCE);handle.flush()
 root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
 for index in range(21):
  if index==0: content=SAMPLE_IN
  else:
   for attempt_no in range(100):
    content=g3724(random.Random(3724+index+attempt_no*1000))
    if content not in seen: break
   else: raise AssertionError("insufficient diversity")
  seen.append(content)
  result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
  (root/f"{index}.in").write_text(content,encoding="utf-8")
  (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")

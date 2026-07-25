import random,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\nm={"2":"abc","3":"def","4":"ghi","5":"jkl","6":"mno","7":"pqrs","8":"tuv","9":"wxyz"}\na=sys.stdin.read().split(); out=[]\nfor w,d in zip(a[1::2],a[2::2]): out.append("Y" if len(w)==len(d) and all(x.lower() in m[y] for x,y in zip(w,d)) else "N")\nprint("\\n".join(out))'
SAMPLE_IN='3\nILOVEYOU 45683968\ncomputer 26678837\nThankyou 84265967\n'
def g3712(r):
    mp = "abc def ghi jkl mno pqrs tuv wxyz".split()
    cases = []
    for _ in range(r.randint(1, 5)):
        digits = "".join(r.choice("23456789") for _ in range(r.randint(1, 12)))
        word = "".join(r.choice(mp[int(d)-2]) for d in digits)
        if r.random() < .35: word = word[:-1] + r.choice("xyz")
        cases.append(f"{word} {digits}")
    return str(len(cases)) + "\n" + "\n".join(cases) + "\n"

with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
 handle.write(REFERENCE_SOURCE);handle.flush()
 root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
 for index in range(21):
  if index==0:content=SAMPLE_IN
  else:
   for attempt in range(100):
    content=g3712(random.Random(3712+index+attempt*1000))
    if content not in seen:break
   else:raise AssertionError("insufficient diversity")
  seen.append(content)
  result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
  (root/f"{index}.in").write_text(content,encoding="utf-8")
  (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")

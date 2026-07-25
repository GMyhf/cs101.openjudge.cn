import random,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\na=list(map(int,sys.stdin.read().split())); out=[]\nfor x,y in zip(a[1::2],a[2::2]):\n    out.append("YES" if any(((x<<k)|(x>>(16-k)))&65535==y for k in range(16)) else "NO")\nprint("\\n".join(out))'
SAMPLE_IN='4\n2 4\n9 18\n45057 49158\n7 12\n'
def g3718(r):
    n = r.randint(1, 50)
    pairs = []
    for _ in range(n):
        a = r.randint(0, 65535)
        if r.random() < .5:
            k = r.randint(0, 15)
            b = ((a << k) | (a >> (16 - k))) & 65535
        else:
            b = r.randint(0, 65535)
        pairs.append(f"{a} {b}")
    return str(n) + "\n" + "\n".join(pairs) + "\n"

with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
 handle.write(REFERENCE_SOURCE);handle.flush()
 root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
 for index in range(21):
  if index==0: content=SAMPLE_IN
  else:
   for attempt in range(100):
    content=g3718(random.Random(3718+index+attempt*1000))
    if content not in seen: break
   else: raise AssertionError("insufficient diversity")
  seen.append(content)
  result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
  (root/f"{index}.in").write_text(content,encoding="utf-8")
  (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")

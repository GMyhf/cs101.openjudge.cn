import random,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\na=sys.stdin.read().split(); n=int(a[0]); versions=a[1:1+n]\ndef key(v): return tuple(map(int,v.split(".")))\nprint("\\n".join(sorted(versions,key=key)))'
SAMPLE_IN='9\n4.8\n4.8.2\n7.2\n2.96\n3.4.5\n1.0\n2\n6.4\n1.0.0\n'
def g23007(r):
    versions = []
    for _ in range(r.randint(1, 20)):
        versions.append(".".join(str(r.randint(0, 100)) for _ in range(r.randint(1, 6))))
    return str(len(versions)) + "\n" + "\n".join(versions) + "\n"

with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
 handle.write(REFERENCE_SOURCE);handle.flush()
 root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
 for index in range(21):
  if index==0: content=SAMPLE_IN
  else:
   for attempt in range(100):
    content=g23007(random.Random(23007+index+attempt*1000))
    if content not in seen: break
   else: raise AssertionError("insufficient diversity")
  seen.append(content)
  result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
  (root/f"{index}.in").write_text(content,encoding="utf-8")
  (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")

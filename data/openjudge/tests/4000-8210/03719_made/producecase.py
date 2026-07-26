import random,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\nlines=sys.stdin.read().splitlines()\nwhile lines and not lines[-1].strip(): lines.pop()\nn=len(lines)//2; rows=[]\nfor i in range(n):\n    name=lines[2*i]; a=lines[2*i+1].split()\n    ident,sex=a[0].split(","); age=a[1]\n    rows.append((name, i, ident, sex, age))\nfor x in sorted(rows,key=lambda z:z[0].lower()):\n    print(x[0]); print(f"{int(x[2]):08d},{x[3]} {x[4]}")\n'
SAMPLE_IN='Tom Hanks\n7863,M 18\nMary Lu\n18343,F 21\nSanta Fe\n27863,M 17\n'
def g3719(r):
    rows=[]
    for i in range(r.randint(1, 8)):
        name=r.choice(["Ann Lee","bob Stone","Cara Q","D E"])+" "+str(i)
        ident=r.randint(1,99999); sex=r.choice(["M","F"]); age=r.randint(1,100)
        rows.append(f"{name}\n{ident},{sex} {age}")
    return "\n".join(rows)+"\n"

with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
 handle.write(REFERENCE_SOURCE);handle.flush()
 root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
 for index in range(21):
  if index==0: content=SAMPLE_IN
  else:
   for attempt_no in range(100):
    content=g3719(random.Random(3719+index+attempt_no*1000))
    if content not in seen: break
   else: raise AssertionError("insufficient diversity")
  seen.append(content)
  result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
  (root/f"{index}.in").write_text(content,encoding="utf-8")
  (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")

import random,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\nfrom datetime import date\nlines=sys.stdin.read().splitlines(); n=len(lines)-1; rows=[]\nfor i in range(n):\n    parts=lines[1+i].split(); name=parts[0]; y,m,d,Y,M,D=map(int,parts[1:])\n    rows.append((name,(date(Y,M,D)-date(y,m,d)).days+1,i,a[p-1-0] if False else ""))\nfor row in sorted(rows,key=lambda x:(-x[1],x[2])): print(row[0],row[1])'
SAMPLE_IN='3\njohn 2007 10 1 2007 10 2\nabbot 2008 2 21 2008 3 1\nalcott 2006 2 20 2006 3 1\n'
def g3715(r):
    from datetime import date, timedelta
    rows=[]
    for i in range(r.randint(1, 8)):
        y=r.randint(1900, 9990); m=r.randint(1, 12)
        start=date(y,m,1)+timedelta(days=r.randint(0, 27))
        if start.year==9999: start=date(9998,12,1)
        end=start+timedelta(days=r.randint(1, 3000))
        rows.append(f"p{i:02d} {start.year} {start.month} {start.day} {end.year} {end.month} {end.day}")
    return "\n".join(rows)+"\n"

with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
 handle.write(REFERENCE_SOURCE);handle.flush()
 root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
 for index in range(21):
  if index==0: content=SAMPLE_IN
  else:
   for attempt_no in range(100):
    content=g3715(random.Random(3715+index+attempt_no*1000))
    if content not in seen: break
   else: raise AssertionError("insufficient diversity")
  seen.append(content)
  result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
  (root/f"{index}.in").write_text(content,encoding="utf-8")
  (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")

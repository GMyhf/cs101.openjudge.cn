import random,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\na=iter(sys.stdin.read().split()); out=[]\nwhile True:\n n=int(next(a))\n if n==0: break\n nrows=[[int(next(a)) for _ in range(i+1)] for i in range(n)]\n row,col=int(next(a))-1,int(next(a))-1\n def f(i,j):\n  if i==n-1:return nrows[i][j]\n  return max(nrows[i][j],f(i+1,j),f(i+1,j+1))\n out.append(str(f(row,col)))\nprint("\\n".join(out))'
SAMPLE_IN='1\n2\n1 1\n5\n7\n3 8\n8 1 0\n2 7 4 4\n4 5 2 6 5\n1 1\n6\n88\n97 26\n39 16 47\n94 25 66 4\n64 49 20 36 27\n37 87 29 37 10 40\n2 1\n0\n'
def g3263(r):
    cases = []
    for _ in range(r.randint(1, 3)):
        n = r.randint(1, 8)
        rows = [[r.randint(0, 100) for _ in range(i + 1)] for i in range(n)]
        cases.append((rows, r.randint(1, n), r.randint(1, n)))
        cases[-1] = (rows, cases[-1][1], r.randint(1, cases[-1][1]))
    lines = []
    for rows, row, col in cases:
        lines += [str(len(rows))] + [" ".join(map(str, x)) for x in rows] + [f"{row} {col}"]
    return "\n".join(lines + ["0"]) + "\n"

with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
 handle.write(REFERENCE_SOURCE);handle.flush()
 root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
 for index in range(21):
  if index==0:content=SAMPLE_IN
  else:
   for attempt in range(100):
    content=g3263(random.Random(3263+index+attempt*1000))
    if content not in seen:break
   else:raise AssertionError("insufficient diversity")
  seen.append(content)
  result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
  (root/f"{index}.in").write_text(content,encoding="utf-8")
  (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")

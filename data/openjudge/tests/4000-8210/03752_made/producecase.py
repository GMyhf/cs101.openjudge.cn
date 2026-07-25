import random,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\nfrom collections import deque\na=sys.stdin.read().split(); r,c=map(int,a[:2]); g=a[2:]; d=[[-1]*c for _ in range(r)]\nq=deque([(0,0)]); d[0][0]=1\nwhile q:\n    x,y=q.popleft()\n    for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):\n        u,v=x+dx,y+dy\n        if 0<=u<r and 0<=v<c and g[u][v]=="." and d[u][v]<0:\n            d[u][v]=d[x][y]+1; q.append((u,v))\nprint(d[-1][-1])'
SAMPLE_IN='5 5\n..###\n#....\n#.#.#\n#.#.#\n#.#..\n'
def g3752(r):
    rows,cols=r.randint(1, 12),r.randint(1, 12)
    grid=[["."]*cols for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            if (i,j) not in [(0,0),(rows-1,cols-1)] and r.random()<.25:
                grid[i][j]="#"
    # Force a monotone backbone, then verify the generated maze remains reachable.
    for i in range(rows): grid[i][0]="."
    for j in range(cols): grid[rows-1][j]="."
    assert grid[0][0]=="." and grid[-1][-1]=="."
    return f"{rows} {cols}\n"+"\n".join("".join(row) for row in grid)+"\n"

with tempfile.NamedTemporaryFile("w",suffix=".py",encoding="utf-8") as handle:
 handle.write(REFERENCE_SOURCE);handle.flush()
 root=Path(__file__).parent/"data";seen=[SAMPLE_IN]
 for index in range(21):
  if index==0: content=SAMPLE_IN
  else:
   for attempt_no in range(100):
    content=g3752(random.Random(3752+index+attempt_no*1000))
    if content not in seen: break
   else: raise AssertionError("insufficient diversity")
  seen.append(content)
  result=subprocess.run(["python3",handle.name],input=content,text=True,capture_output=True,timeout=10,check=True)
  (root/f"{index}.in").write_text(content,encoding="utf-8")
  (root/f"{index}.out").write_text(result.stdout,encoding="utf-8")

import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='import heapq\n\nk = int(input())\nn = int(input())\nroad = [set() for i in range(n + 1)]\nfor i in range(int(input())):\n    s, d, l, t = map(int, input().split())\n    road[s].add((d, l, t))\n\ndis = [{} for i in range(n + 1)]\ndis[1][0] = 0\nh = [(0, 1, 0)]\n\nwhile h:\n    d, u, c = heapq.heappop(h)\n    if u == n:\n        print(d)\n        break\n    for v, l, t in road[u]:\n        if c + t > k:\n            continue\n        if c + t not in dis[v] or d + l < dis[v][c + t]:\n            dis[v][c + t] = d + l\n            heapq.heappush(h, (d + l, v, c + t))\nelse:\n    print(-1)'
SAMPLE='5\n6\n7\n1 2 2 3\n2 4 3 3\n3 4 2 4\n1 3 4 1\n4 6 2 1\n3 5 2 0\n5 4 3 2\n'
GENERATOR_NAME='g7735'
def g7735(r):
    n=r.randint(3,10); k=r.randint(3,80); edges=[]
    for u in range(1,n): edges.append((u,u+1,r.randint(1,20),r.randint(0,min(10,k))))
    for _ in range(r.randint(0,12)):
        u=r.randint(1,n-1); v=r.randint(u+1,n)
        edges.append((u,v,r.randint(1,20),r.randint(0,min(10,k))))
    return f"{k}\n{n}\n{len(edges)}\n"+"\n".join(" ".join(map(str,e)) for e in edges)+"\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        p=Path(d)/"main.py"; p.write_text(REFERENCE,encoding="utf-8")
        x=subprocess.run([sys.executable,str(p)],input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1,21)]
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text,encoding="utf-8")
        (data/f"{i}.out").write_text(run(text),encoding="utf-8")
if __name__=="__main__": main()

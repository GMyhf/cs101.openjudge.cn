import random, subprocess, sys, tempfile
from pathlib import Path
def g1125(r):
    n = r.randint(2, 18); rows = []
    for i in range(1, n + 1):
        edges = {(i % n) + 1: r.randint(1, 10)}
        for _ in range(r.randint(0, min(5, n - 1))):
            j = r.randint(1, n)
            if j != i: edges[j] = r.randint(1, 10)
        rows.append(str(len(edges)) + " " + " ".join(f"{j} {w}" for j, w in sorted(edges.items())))
    return str(n) + "\n" + "\n".join(rows) + "\n0\n"

REFERENCE="# Source collection: /home/rocky/git/2020fall-cs101/2020fall_cs101.openjudge.cn_problems.md\n# Heading: 1125: Stockbroker Grapevine\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2020fall-cs101/blob/main/2020fall_cs101.openjudge.cn_problems.md\n# Upstream problem: http://cs101.openjudge.cn/practice/01125/\n# License: not declared in source collection; no license is inferred.\nimport heapq\nwhile True:\n    n=int(input())\n    if n==0:\n        break\n    contact=[{}]\n    for _ in range(n):\n        list1=list(map(int,input().split()))\n        dict1={}\n        for i in range((len(list1)-1)//2):\n            dict1[list1[2*i+1]]=list1[2*i+2]\n        contact.append(dict1)\n    i0=0\n    s=float('inf')\n    for i in range(1,n+1):\n        heap=[(0,i)]\n        heapq.heapify(heap)\n        time=[0]+[float('inf')]*n\n        time[i]=0\n        condition=[True]+[False]*n\n        while heap:\n            t,j=heapq.heappop(heap)\n            if condition[j]:\n                continue\n            condition[j]=True\n            if sum(condition)==n+1:\n                if max(time)<s:\n                    s=max(time)\n                    i0=i\n                break\n            for k in contact[j]:\n                t1=t+contact[j][k]\n                if not condition[k] and time[k]>t1:\n                    time[k]=t1\n                    heapq.heappush(heap,(t1,k))\n    if i0==0:\n        print('disjoint')\n    else:\n        print(f'{i0} {s}')\n"
SAMPLE='3\n2 2 4 3 5\n2 1 2 3 6\n2 1 2 2 2\n5\n3 4 4 2 8 5 3\n1 5 8\n4 1 6 4 10 2 7 5 2\n0\n2 2 5 1 5\n0\n'
GENERATOR='g1125'

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as folder:
        script=Path(folder)/"main.py"; script.write_text(REFERENCE)
        result=subprocess.run([sys.executable,"-I",str(script)],input=text,text=True,capture_output=True,timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    for old in data.glob("*"): old.unlink()
    cases=[SAMPLE]+[globals()[GENERATOR](random.Random(seed)) for seed in range(1,21)]
    for i,case in enumerate(cases):
        (data/f"{i}.in").write_text(case); (data/f"{i}.out").write_text(run(case))
if __name__=="__main__": main()

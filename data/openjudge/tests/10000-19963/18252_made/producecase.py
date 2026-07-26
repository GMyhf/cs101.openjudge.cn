import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE="# External reference: cs101.openjudge.cn practice/18252 statistics, Accepted solution 41303512.\n# Source: http://cs101.openjudge.cn/practice/solution/41303512/\n# Statistics: http://cs101.openjudge.cn/practice/18252/statistics/\n# License: not declared on submission page; no license inferred\ndef spfa(s):\n    dis = [float('inf') for _ in range(n)]\n    dis[s] = 0\n    queue = [s]\n    cnt = [0] * n\n    while queue:\n        u = queue.pop(0)\n        for v, w in G[u]:\n            if dis[v] > dis[u] + w:\n                dis[v] = dis[u] + w\n                queue.append(v)\n                cnt[v] += 1\n        if cnt[u] > n:\n            return ['Error']\n    return dis\n\n\nfor _ in range(int(input())):\n    n, m, s = map(int, input().split())\n    G = [[] for _ in range(n)]\n    for _ in range(m):\n        x, y, z = map(int, input().split())\n        G[x - 1].append((y - 1, z))\n    print(*(i if i != float('inf') else 'null' for i in spfa(s - 1)))\n"
LANGUAGE='Python3'
SAMPLE='4\n5 7 1\n1 2 3\n2 3 4\n3 4 8\n1 3 9\n4 5 1\n1 4 5\n1 5 10\n4 4 1\n1 2 -4\n2 3 8\n1 3 5\n3 4 0\n3 3 2\n1 2 -3\n2 3 -4\n3 1 6\n4 2 1\n1 2 1\n3 4 2\n'
GENERATOR_NAME='g18252'
def g18252(r):
    n=r.randint(2,8); edges=[(i,i+1,r.randint(1,20)) for i in range(1,n)]
    edges += [(r.randint(1,n-1),r.randint(2,n),r.randint(1,20)) for _ in range(r.randint(0,8))]
    edges=[e for e in edges if e[0]!=e[1]]
    return "1\n"+f"{n} {len(edges)} 1\n"+"\n".join(" ".join(map(str,e)) for e in edges)+"\n"

def run(text):
    with tempfile.TemporaryDirectory(prefix="producecase-") as d:
        d=Path(d); src=d/'main.py'
        src.write_text(REFERENCE); cmd=[sys.executable,str(src)]
        if LANGUAGE=="G++":
            exe=d/"main"; subprocess.run(["g++","-std=c++17","-O2",str(src),"-o",str(exe)],check=True)
            cmd=[str(exe)]
        x=subprocess.run(cmd,input=text,text=True,capture_output=True,timeout=30)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path("data"); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1,21)]
    for i,text in enumerate(cases):
        (data/f"{i}.in").write_text(text)
        (data/f"{i}.out").write_text(run(text))
if __name__=="__main__": main()

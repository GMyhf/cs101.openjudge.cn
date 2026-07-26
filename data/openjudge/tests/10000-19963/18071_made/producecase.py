import random,subprocess,sys,tempfile
from pathlib import Path
REFERENCE='# External reference: cs101.openjudge.cn practice/18071 statistics, Accepted solution 52688789.\n# Source: http://cs101.openjudge.cn/practice/solution/52688789/\n# Statistics: http://cs101.openjudge.cn/practice/18071/statistics/\n# License: not declared on submission page; no license inferred\nimport sys\n\ndata = sys.stdin.read().strip().splitlines()\nM, N = map(int, data[0].strip().split())\nmatrix = []\nfor i in range(1, M + 1):\n    line = list(map(int, data[i].split()))\n    matrix.append(line)\ngraph = {(i, j): [] for i in range(M) for j in range(N)}\n\ndire = [(0, 1), (0, -1), (1, 0), (-1, 0)]\nfor i in range(M):\n    for j in range(N):\n        if matrix[i][j] == 1:\n            for dx, dy in dire:\n                if 0 <= i + dx <= M - 1 and 0 <= j + dy <= N - 1:\n\n                    if matrix[i + dx][j + dy] == 1:\n                        graph[(i, j)].append((i + dx, j + dy))\n\n\ndef topological_sort_dfs(M, N, graph):\n    visited = [[0] * N for _ in range(M)]\n\n    def dfs(i, j, fi, fj):\n        visited[i][j] = 1\n        for v in graph[(i, j)]:\n            if v[0] == fi and v[1] == fj:\n                continue\n            if visited[v[0]][v[1]] == 1:\n                return False\n            if visited[v[0]][v[1]] == 0:\n                if not dfs(v[0], v[1], i, j):\n                    return False\n        visited[i][j] = 2\n        return True\n\n    for i in range(M):\n        for j in range(N):\n            if visited[i][j] == 0:\n                if not dfs(i, j, -1, -1):\n                    return None\n    return 1\n\n\nt = topological_sort_dfs(M, N, graph)\nif not t:\n    print("YES")\nelse:\n    print("NO")\n'
LANGUAGE='Python3'
SAMPLE='2 3\n1 1 0\n1 1 1\n'
GENERATOR_NAME='g18071'
def g18071(r):
    m,n=r.randint(2,8),r.randint(2,8); g=[[0]*n for _ in range(m)]
    if r.random()<.5:
        for i in range(1,m): g[i][0]=1
        for j in range(n): g[0][j]=1
    else:
        for i in range(2): 
            for j in range(2): g[i][j]=1
    return f"{m} {n}\n"+"\n".join(" ".join(map(str,x)) for x in g)+"\n"

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

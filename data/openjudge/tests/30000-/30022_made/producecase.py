import random
REFERENCE='# External reference: /practice/30022/statistics/\n# Accepted submission: 52733303\n# Source: http://cs101.openjudge.cn/practice/solution/52733303/\n# License: not declared on the submission page; no license is inferred.\n\nfrom collections import deque\nimport sys\n\ndef bfs(start, n, adj):\n    dist = [-1] * n\n    q = deque()\n    q.append(start)\n    dist[start] = 0\n    while q:\n        u = q.popleft()\n        for v in range(n):\n            if adj[u][v] == 1 and dist[v] == -1:\n                dist[v] = dist[u] + 1\n                q.append(v)\n    return dist\n\ndef main():\n    n, k, s = map(int, sys.stdin.readline().split())\n    adj = []\n    for _ in range(n):\n        row = list(map(int, sys.stdin.readline().split()))\n        adj.append(row)\n    \n    d1 = bfs(k, n, adj)\n    d2 = bfs(s, n, adj)\n    \n    min_len = float(\'inf\')\n    for u in range(n):\n        if d1[u] == -1 or d2[u] == -1:\n            continue\n        if d1[u] == d2[u]:\n            if d1[u] < min_len:\n                min_len = d1[u]\n    \n    print(min_len if min_len != float(\'inf\') else -1)\n\nif __name__ == "__main__":\n    main()'
SAMPLE='5 0 4\n0 1 0 0 1\n1 0 1 0 0\n0 1 0 1 0\n0 0 1 0 1\n1 0 0 1 0\n'
GENERATOR_NAME='g30022'
def g30022(r):
    n = r.randint(2, 45); k, s = r.sample(range(n), 2)
    matrix = [[0 if i == j else int(r.random() < .35) for j in range(n)] for i in range(n)]
    return f"{n} {k} {s}\n" + "\n".join(" ".join(map(str, row)) for row in matrix) + "\n"

from pathlib import Path
import random, subprocess, sys, tempfile
REFERENCE = REFERENCE
def solve(text):
    with tempfile.TemporaryDirectory(prefix='producecase-run-') as d:
        p=Path(d)/'main.py'; p.write_text(REFERENCE)
        result=subprocess.run([sys.executable, str(p)], input=text, text=True, capture_output=True, timeout=120)
        if result.returncode: raise SystemExit(result.stderr)
        return result.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(seed)) for seed in range(1,21)]
    for i, case in enumerate(cases):
        (data/f'{i}.in').write_text(case); (data/f'{i}.out').write_text(solve(case))
if __name__=='__main__': main()

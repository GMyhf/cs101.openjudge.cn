import random
REFERENCE="# External reference: /practice/30222/statistics/\n# Accepted submission: 52829485\n# Source: http://cs101.openjudge.cn/practice/solution/52829485/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\nfrom collections import deque\n\ndef solve():\n    # 读取所有输入\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n    \n    N = int(input_data[0])\n    M = int(input_data[1])\n    \n    # 任务耗时，采用1-based索引\n    T = [0] + [int(x) for x in input_data[2:2+N]]\n    \n    adj = [[] for _ in range(N + 1)]\n    in_degree = [0] * (N + 1)\n    \n    # 构建邻接表和入度数组\n    idx = 2 + N\n    for _ in range(M):\n        if idx >= len(input_data):\n            break\n        u = int(input_data[idx])\n        v = int(input_data[idx+1])\n        adj[u].append(v)\n        in_degree[v] += 1\n        idx += 2\n        \n    # 拓扑排序队列\n    queue = deque()\n    dp = [0] * (N + 1)\n    \n    # 初始化入度为 0 的节点\n    for i in range(1, N + 1):\n        dp[i] = T[i]\n        if in_degree[i] == 0:\n            queue.append(i)\n            \n    processed_count = 0\n    \n    # 拓扑排序与动态规划更新\n    while queue:\n        u = queue.popleft()\n        processed_count += 1\n        for v in adj[u]:\n            if dp[u] + T[v] > dp[v]:\n                dp[v] = dp[u] + T[v]\n            in_degree[v] -= 1\n            if in_degree[v] == 0:\n                queue.append(v)\n                \n    # 判断是否存在环\n    if processed_count < N:\n        print(-1)\n    else:\n        print(max(dp))\n\nif __name__ == '__main__':\n    solve()"
SAMPLE='3 2\n5 10 5\n1 2\n1 3\n'
GENERATOR_NAME='g30222'
CPP=False
def g30222(r):
    n = r.randint(2, 30); edges = [(i, r.randint(1, i-1)) for i in range(2, n+1) if r.random()<.5]
    return f"{n} {len(edges)}\n{' '.join(str(r.randint(1,100)) for _ in range(n))}\n" + "\n".join(f"{a} {b}" for a,b in edges) + "\n"

from pathlib import Path
import subprocess, sys, tempfile
def run(text):
    with tempfile.TemporaryDirectory(prefix='producecase-run-') as d:
        p=Path(d)/('main.cpp' if CPP else 'main.py'); p.write_text(REFERENCE)
        if CPP:
            exe=Path(d)/'main'; c=subprocess.run(['g++','-O2','-std=c++17',str(p),'-o',str(exe)],capture_output=True,text=True,timeout=30)
            if c.returncode: raise SystemExit(c.stderr)
            cmd=[str(exe)]
        else: cmd=[sys.executable,str(p)]
        x=subprocess.run(cmd,input=text,text=True,capture_output=True,timeout=120)
        if x.returncode: raise SystemExit(x.stderr)
        return x.stdout
def main():
    data=Path('data'); data.mkdir(exist_ok=True)
    cases=[SAMPLE]+[globals()[GENERATOR_NAME](random.Random(s)) for s in range(1,21)]
    for i,c in enumerate(cases): (data/f'{i}.in').write_text(c); (data/f'{i}.out').write_text(run(c))
if __name__=='__main__': main()

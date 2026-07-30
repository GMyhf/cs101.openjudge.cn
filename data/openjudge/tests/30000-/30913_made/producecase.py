#!/usr/bin/env python3
"""Problem-specific generators and input contracts for T-028 phase-2 round 25."""
from __future__ import annotations
import random
import re

NUMBERS={30102,30212,30218,30220,29740,29982,30913,30921}
EXEMPTIONS={}
FILTER_INVALID_ARCHIVE_INPUTS={30921}
INPUT_DOMAINS={
30102:"第一行包含一个整数 N (2 <= N <= 1,000,000)，代表数据的持续时间（以秒为单位）。",
30212:"对于所有评测用例，1 ≤ N≤ 10^9",30218:"1 <= N <= 1,000，状态绝对值在 [1, 1000] 之间。",
30220:"第一行包含两个整数 N 和 M，1 ≤ N, M ≤ 500。",
29740:"输入文件第一行是两个整数 n（1≤n≤100）和 p（0 ≤ p ≤ n(n-1)）。",
29982:"在两个正整数m和n给定的整数范围内（m 小于 n，且不包括m和n）取出各位数字之和均为k的倍数的所有数(k为正整数)",
30913:"第一行包含两个整数 n 和 m（1 <= n <= 10^5，0 <= m <= 2 * 10^5），分别表示公园里的岔路口数量和有向路径数量。",
30921:"第一行包含三个整数 n,q,s（1 <= n <= 10^5,0 <= q <= 5 * 10^5,2 <= s <= 10^9），表示积木数目、操作次数和一堆积木的数量上限。",
}
LABELS={
30102:"2..1000000 positive prices below 2^31 follow N on separate lines",
30212:"N is in 1..10^9 and K is a nonnegative feasible bit count",
30218:"1..1000 nonzero signed unit states have absolute values in 1..1000",
30220:"a 1..500 rectangular grid has values in -100..100",
29740:"1..100 neural nodes and bounded weighted directed edges obey initial-state and duplicate-edge rules",
29982:"positive m<n<=10000 and positive k use the exact comma-separated input protocol",
30913:"bounded directed weighted paths, including loops and parallel edges, precede an in-range start vertex",
30921:"bounded block operations use valid endpoints and a collapse threshold of at least two",
}
INVALID={30102:"1\n5\n",30212:"0 2\n",30218:"2\n1 0\n",30220:"1 2\n-101 0\n",
29740:"2 1\n1 0\n1 0\n1 3 1\n",29982:"35,11,3\n",30913:"2 1\n1 3 4\n1\n",
30921:"2 1 1\n1 2\n"}
SAMPLE_INPUTS={30220:"2 3\n1 -5 3\n-2 4 -1\n",
29740:"5 6\n1 0\n1 0\n0 1\n0 1\n0 1\n1 3 1\n1 4 1\n1 5 1\n2 3 1\n2 4 1\n2 5 1\n",
30913:"2 2\n1 2 4\n2 1 4\n1\n",
30921:"5 10 3\n1 2\n4 2\n1 5\n2 3\n4 1\n5 1\n2 4\n1 3\n2 5\n3 4\n"}
SAMPLE_OUTPUTS={30220:"9\n",29740:"3 1\n4 1\n5 1\n",30913:"16\n",
30921:"4\n5\n4\n3\n4\n3\n4\n5\n4\n3\n"}

def generate(number,seed):
 r=random.Random(number*1_000_003+seed)
 if number==30102:
  n=100000 if seed==20 else r.randint(2,5000);return f"{n}\n"+'\n'.join(str(r.randint(1,2**31-1)) for _ in range(n))+'\n'
 if number==30212:return f"{r.randint(1,10**9)} {r.randint(0,30)}\n"
 if number==30218:
  n=r.randint(1,1000);return f"{n}\n"+' '.join(str(r.choice((-1,1))*r.randint(1,1000)) for _ in range(n))+'\n'
 if number==30220:
  n,m=r.randint(1,40),r.randint(1,40);return f"{n} {m}\n"+'\n'.join(' '.join(str(r.randint(-100,100)) for _ in range(m)) for _ in range(n))+'\n'
 if number==29740:
  n=r.randint(1,40)
  if seed%4==0 and n==1:n=2
  edges=[]
  if seed%4==0:
   edges=[(i,i+1,r.randint(-5,5)) for i in range(1,n)]+[(n,1,r.randint(-5,5))]
  else:
   candidates=[(a,b) for a in range(1,n+1) for b in range(a+1,n+1)];chosen=r.sample(candidates,r.randint(0,min(len(candidates),100)))
   edges=[(a,b,r.randint(-10,10)) for a,b in chosen]
   if chosen and seed%3==0:
    a,b=r.choice(chosen);edges.append((a,b,r.randint(-10,10)))
  indegree=[0]*(n+1)
  for a,b,w in edges:indegree[b]+=1
  states=[(r.randint(-20,20) if indegree[i]==0 else 0,r.randint(-10,10)) for i in range(1,n+1)]
  return f"{n} {len(edges)}\n"+''.join(f"{c} {u}\n" for c,u in states)+''.join(f"{a} {b} {w}\n" for a,b,w in edges)
 if number==29982:
  m=r.randint(1,9998);n=r.randint(m+1,10000);k=r.randint(1,30);return f"{m},{n},{k}\n"
 if number==30913:
  n=r.randint(1,300);m=r.randint(0,1500);edges=[(r.randint(1,n),r.randint(1,n),r.randint(0,10**8)) for _ in range(m)];return f"{n} {m}\n"+''.join(f"{a} {b} {w}\n" for a,b,w in edges)+f"{r.randint(1,n)}\n"
 if number==30921:
  n=r.randint(1,1000);q=r.randint(1,3000);s=r.randint(2,2*n+10);return f"{n} {q} {s}\n"+''.join(f"{r.randint(1,n)} {r.randint(1,n)}\n" for _ in range(q))
 raise KeyError(number)

def valid(number,text):
 try:
  lines=text.rstrip('\n').splitlines();tokens=text.split()
  if number==30102:
   n=int(lines[0]);a=list(map(int,lines[1:]));return 2<=n<=1_000_000 and len(a)==n and all(1<=x<2**31 for x in a)
  if number==30212:
   n,k=map(int,tokens);return len(tokens)==2 and 1<=n<=10**9 and 0<=k<=30
  if number==30218:
   n=int(lines[0]);a=list(map(int,lines[1].split()));return len(lines)==2 and 1<=n<=1000 and len(a)==n and all(1<=abs(x)<=1000 for x in a)
  if number==30220:
   n,m=map(int,lines[0].split());rows=[list(map(int,x.split())) for x in lines[1:]];return 1<=n<=500 and 1<=m<=500 and len(rows)==n and all(len(x)==m and all(-100<=v<=100 for v in x) for x in rows)
  if number==29740:
   n,p=map(int,lines[0].split());states=[tuple(map(int,x.split())) for x in lines[1:n+1]];edges=[tuple(map(int,x.split())) for x in lines[n+1:]]
   if not 1<=n<=100 or not 0<=p<=n*(n-1) or len(states)!=n or len(edges)!=p or any(len(x)!=3 or not(1<=x[0]<=n and 1<=x[1]<=n) for x in edges):return False
   indegree=[0]*(n+1)
   for a,b,w in edges:indegree[b]+=1
   return all(len(state)==2 and (indegree[i]==0 or state[0]==0) for i,state in enumerate(states,1))
  if number==29982:
   if len(lines)!=1 or not re.fullmatch(r'\d+,\d+,\d+',lines[0]):return False
   m,n,k=map(int,lines[0].split(','));return 0<m<n<=10000 and k>0
  if number==30913:
   n,m=map(int,lines[0].split());edges=[tuple(map(int,x.split())) for x in lines[1:1+m]];s=int(lines[1+m]);return 1<=n<=10**5 and 0<=m<=200000 and len(lines)==m+2 and len(edges)==m and all(1<=a<=n and 1<=b<=n and 0<=w<=10**8 for a,b,w in edges) and 1<=s<=n
  if number==30921:
   n,q,s=map(int,lines[0].split());ops=[tuple(map(int,x.split())) for x in lines[1:]];return 1<=n<=10**5 and 0<=q<=500000 and 2<=s<=10**9 and len(ops)==q and all(1<=a<=n and 1<=b<=n for a,b in ops)
 except (ValueError,IndexError,TypeError):return False
 return False


import subprocess as _subprocess, sys as _sys, tempfile as _tempfile
from pathlib import Path as _Path
REFERENCE='# External reference: http://cs101.openjudge.cn/practice/30913/statistics/\n# Accepted submission: 52756598\n# Source: http://cs101.openjudge.cn/practice/solution/52756598/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\n\n\ndef solve():\n    # 使用 sys.stdin.read 快速读取输入，防止 I/O 成为瓶颈\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n    n = int(input_data[0])\n    m = int(input_data[1])\n\n    adj = [[] for _ in range(n + 1)]\n    radj = [[] for _ in range(n + 1)]\n\n    idx = 2\n    for _ in range(m):\n        u = int(input_data[idx])\n        v = int(input_data[idx + 1])\n        w = int(input_data[idx + 2])\n        adj[u].append((v, w))\n        radj[v].append(u)\n        idx += 3\n\n    s = int(input_data[idx])\n\n    # ---------------- Kosaraju 算法求强连通分量 (SCC) ----------------\n\n    # 步骤 1：在原图上运行非递归 DFS，求得后序遍历序列\n    visited = [False] * (n + 1)\n    order = []\n\n    for i in range(1, n + 1):\n        if not visited[i]:\n            state_stack = [(i, 0)]\n            visited[i] = True\n            while state_stack:\n                u, edge_idx = state_stack[-1]\n                if edge_idx < len(adj[u]):\n                    v, _ = adj[u][edge_idx]\n                    state_stack[-1] = (u, edge_idx + 1)\n                    if not visited[v]:\n                        visited[v] = True\n                        state_stack.append((v, 0))\n                else:\n                    order.append(u)\n                    state_stack.pop()\n\n    # 步骤 2：在反图上，按照后序遍历的逆序进行非递归 DFS，划分 SCC\n    visited2 = [False] * (n + 1)\n    scc_id = [-1] * (n + 1)\n    scc_count = 0\n\n    for u in reversed(order):\n        if not visited2[u]:\n            stack = [u]\n            visited2[u] = True\n            while stack:\n                curr = stack.pop()\n                scc_id[curr] = scc_count\n                for v in radj[curr]:\n                    if not visited2[v]:\n                        visited2[v] = True\n                        stack.append(v)\n            scc_count += 1\n\n    # ---------------- 榨干单条边能获得的最大愉悦度 ----------------\n    def harvest(w):\n        if w <= 0:\n            return 0\n        # 求解 T * (T - 1) / 2 < w 时的最大正整数 T\n        val = 1 + 8 * w\n        r = int(val**0.5)\n        T = (1 + r) // 2\n        # 对 T 进行微调以确保 100% 精确\n        while T * (T - 1) // 2 >= w:\n            T -= 1\n        while (T + 1) * T // 2 < w:\n            T += 1\n        return T * w - (T - 1) * T * (T + 1) // 6\n\n    # ---------------- 缩点构建 DAG ----------------\n    scc_val = [0] * scc_count\n    dag_edges = [{} for _ in range(scc_count)]\n\n    for u in range(1, n + 1):\n        su = scc_id[u]\n        for v, w in adj[u]:\n            sv = scc_id[v]\n            if su == sv:\n                # 强连通分量内部的边可以被无限次榨干\n                scc_val[su] += harvest(w)\n            else:\n                # 强连通分量之间的跨越边，只能走一次，多条边时保留权值最大的一条\n                if sv not in dag_edges[su] or dag_edges[su][sv] < w:\n                    dag_edges[su][sv] = w\n\n    # ---------------- 拓扑排序 (Kahn 算法) ----------------\n    in_degree = [0] * scc_count\n    for su in range(scc_count):\n        for sv in dag_edges[su]:\n            in_degree[sv] += 1\n\n    from collections import deque\n\n    queue = deque([i for i in range(scc_count) if in_degree[i] == 0])\n    topo_order = []\n    while queue:\n        u = queue.popleft()\n        topo_order.append(u)\n        for v in dag_edges[u]:\n            in_degree[v] -= 1\n            if in_degree[v] == 0:\n                queue.append(v)\n\n    # ---------------- DAG 上的动态规划 (DP) ----------------\n    dp = [-1] * scc_count\n    scc_s = scc_id[s]\n    dp[scc_s] = scc_val[scc_s]\n\n    for u in topo_order:\n        if dp[u] == -1:\n            continue\n        for v, w in dag_edges[u].items():\n            val = dp[u] + w + scc_val[v]\n            if val > dp[v]:\n                dp[v] = val\n\n    # 最大的愉悦度是所有可达节点中 dp 值的最大值\n    print(max(dp))\n\n\nif __name__ == "__main__":\n    solve()\n'
LANGUAGE='Python3'
NUMBER=30913
SAMPLE='2 2\n1 2 4\n2 1 4\n1\n'
def _build():
 with _tempfile.TemporaryDirectory() as folder:
  folder=_Path(folder);src=folder/('s.py' if LANGUAGE=='Python3' else 's.cpp');src.write_text(REFERENCE)
  cmd=[_sys.executable,'-I',str(src)]
  if LANGUAGE!='Python3':
   exe=folder/'s';_subprocess.run(['g++','-std=c++20','-O2','-pipe',str(src),'-o',str(exe)],check=True);cmd=[str(exe)]
  out=_Path('data');out.mkdir(exist_ok=True)
  for path in out.glob('*'):path.unlink()
  cases=([SAMPLE] if SAMPLE else [])+[generate(NUMBER,seed) for seed in range(1,21)]
  for index,case in enumerate(cases):
   result=_subprocess.run(cmd,input=case,text=True,capture_output=True,timeout=120,check=True)
   answer='\n'.join(line.rstrip() for line in result.stdout.rstrip().splitlines())+'\n'
   (out/f'{index}.in').write_text(case);(out/f'{index}.out').write_text(answer)
if __name__=='__main__':_build()

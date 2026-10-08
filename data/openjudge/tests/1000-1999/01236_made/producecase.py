import random,subprocess,sys,tempfile
from pathlib import Path
import re

# ---- 输入契约（照题面）：第一行 N（2<=N<=100），其后恰 N 行，第 i+1 行是学校 i 的接收者列表，
# 编号取 1..N，以 0 结尾；空列表只有一个 0。
_INT=re.compile(r'-?(0|[1-9][0-9]*)$')
def valid(text):
    try:
        if not text.endswith('\n'): return False
        lines=text[:-1].split('\n')
        if not _INT.match(lines[0].strip()): return False
        n=int(lines[0])
        if not 2<=n<=100 or len(lines)!=n+1: return False
        for ln in lines[1:]:
            t=ln.split()
            if not t or any(not _INT.match(x) for x in t): return False
            t=list(map(int,t))
            if t[-1]!=0 or any(not 1<=v<=n for v in t[:-1]): return False
        return True
    except Exception:
        return False

def _fmt(n,adj):
    return f"{n}\n"+"\n".join(" ".join(map(str,a+[0])) for a in adj)+"\n"

def _relabel(r,n,edges):
    perm=list(range(1,n+1));r.shuffle(perm)
    adj=[[] for _ in range(n)]
    for u,v in edges: adj[perm[u]-1].append(perm[v])
    for a in adj: r.shuffle(a)
    return adj

def _scc_dag(r,n,k,p_in,p_out):
    # 把 n 个点分到 k 个强连通块（块内一个环+随机边），块间只按编号顺序连边，形成 DAG
    cut=sorted(r.sample(range(1,n),k-1)) if k>1 else []
    groups=[];prev=0
    for c in cut+[n]: groups.append(list(range(prev,c)));prev=c
    edges=set()
    for g in groups:
        if len(g)>1:
            for i in range(len(g)): edges.add((g[i],g[(i+1)%len(g)]))
            for u in g:
                for v in g:
                    if u!=v and r.random()<p_in: edges.add((u,v))
    for a in range(k):
        for b in range(a+1,k):
            if r.random()<p_out: edges.add((r.choice(groups[a]),r.choice(groups[b])))
    return sorted(edges)

def generate(seed):
    r=random.Random(1236*1_000_003+seed)
    if seed==1: return _fmt(2,[[],[]])                      # 两个孤立点：A=2 B=2
    if seed==2: return _fmt(2,[[2],[]])                     # A=1 B=1
    if seed==3: return _fmt(2,[[2],[1]])                    # 已强连通：A=1 B=0
    if seed==4: return _fmt(100,[[] for _ in range(100)])   # 全空：A=100 B=100
    if seed==5:                                             # 一个大环：B=0
        return _fmt(100,_relabel(r,100,[(i,(i+1)%100) for i in range(100)]))
    if seed==6: return _fmt(100,[[j for j in range(1,101) if j!=i] for i in range(1,101)])
    if seed==7: return _fmt(100,_relabel(r,100,[(i,i+1) for i in range(99)]))      # 长链
    if seed==8: return _fmt(100,_relabel(r,100,[(0,i) for i in range(1,100)]))     # 一发多：A=1 B=99
    if seed==9: return _fmt(100,_relabel(r,100,[(i,0) for i in range(1,100)]))     # 多汇一：A=99 B=99
    if seed==10:                                            # 两个互不相连的大环
        e=[(i,(i+1)%50) for i in range(50)]+[(50+i,50+(i+1)%50) for i in range(50)]
        return _fmt(100,_relabel(r,100,e))
    if seed==11:                                            # 60 个源指向 1 个大环：A=60 B=60
        e=[(i,(i+1-60)%40+60) for i in range(60,100)]+[(i,60+r.randrange(40)) for i in range(60)]
        return _fmt(100,_relabel(r,100,e))
    if seed==12:                                            # 1 个源大环指向 70 个汇
        e=[(i,(i+1)%30) for i in range(30)]+[(r.randrange(30),i) for i in range(30,100)]
        return _fmt(100,_relabel(r,100,e))
    n=100 if seed%3 else r.randint(2,30)
    k=r.choice([1,2,3,r.randint(1,n),r.randint(1,n),n])
    p_in=r.choice([0.0,0.02,0.1,0.3])
    p_out=r.choice([0.0,0.01,0.05,0.2,0.6])
    return _fmt(n,_relabel(r,n,_scc_dag(r,n,k,p_in,p_out)))

REFERENCE='# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md\n# Heading: 1236: Network of Schools\n# Fenced code block index: 2\n# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md\n# Upstream problem: http://cs101.openjudge.cn/practice/01236/\n# License: not declared; no license is inferred.\nimport sys\n\n# 设置递归深度限制，以应对N=100的DFS调用\n# Python默认递归限制通常是1000，对于N=100的图，2000是绰绰有余的。\nsys.setrecursionlimit(2000)\n\n# 全局变量用于存储图和Tarjan算法的状态\nN = 0\ngraph = []\n\n# Tarjan算法相关变量\ntimer = 0\ndfn = []         # 节点的发现时间 (discovery time)\nlow = []         # 从节点u或其子树能追溯到的最早的发现时间 (lowest reachable discovery time)\nstack = []       # DFS栈，存储当前正在访问的节点\nin_stack = []    # 布尔数组，标记节点是否在栈中\nscc_id = []      # 存储每个节点所属的SCC的ID\nscc_count = 0    # 已找到的SCC的总数\n\ndef tarjan(u):\n    """\n    Tarjan算法的DFS实现，用于寻找强连通分量。\n    u: 当前正在访问的节点\n    """\n    global timer, scc_count\n\n    timer += 1\n    dfn[u] = timer\n    low[u] = timer\n    stack.append(u)\n    in_stack[u] = True\n\n    # 遍历节点u的所有邻居v\n    for v in graph[u]:\n        if dfn[v] == -1: # 如果v尚未访问\n            tarjan(v)\n            # 递归返回后，更新low[u]。u可以到达v能到达的最早发现时间。\n            low[u] = min(low[u], low[v])\n        elif in_stack[v]: # 如果v已经在栈中，说明是回边，或者v在同一个SCC中\n            # 更新low[u]。u可以到达v，所以u可以到达v的发现时间。\n            # 这里必须使用dfn[v]而不是low[v]，因为low[v]可能已经被子树更新到更早的时间，\n            # 而我们关注的是u通过v能够直接回溯到的栈中祖先。\n            low[u] = min(low[u], dfn[v])\n\n    # 如果dfn[u] == low[u]，说明u是某个SCC的根节点\n    if dfn[u] == low[u]:\n        scc_count += 1\n        # 从栈中弹出所有属于当前SCC的节点，直到u被弹出\n        while True:\n            node = stack.pop()\n            in_stack[node] = False\n            scc_id[node] = scc_count # 分配SCC ID\n            if node == u:\n                break\n\ndef solve():\n    """\n    主函数：读取输入，运行Tarjan算法，并解决两个子任务。\n    """\n    global N, graph, timer, dfn, low, stack, in_stack, scc_id, scc_count\n\n    # 读取学校数量N\n    N = int(sys.stdin.readline())\n    # 初始化邻接列表，使用1-based索引\n    graph = [[] for _ in range(N + 1)]\n\n    # 读取每个学校的分发列表，构建图\n    for i in range(1, N + 1):\n        line = list(map(int, sys.stdin.readline().split()))\n        # 输入列表以0结束，因此遍历到倒数第二个元素\n        for j in range(len(line) - 1):\n            graph[i].append(line[j])\n\n    # 初始化Tarjan算法所需变量\n    timer = 0\n    dfn = [-1] * (N + 1)\n    low = [-1] * (N + 1)\n    stack = []\n    in_stack = [False] * (N + 1)\n    scc_id = [0] * (N + 1) # scc_id[i] 表示节点i所属的SCC编号\n    scc_count = 0 # 强连通分量计数器\n\n    # 对所有未访问的节点运行Tarjan算法，确保处理所有连通分量\n    for i in range(1, N + 1):\n        if dfn[i] == -1: # 如果节点i尚未被访问\n            tarjan(i)\n\n    # --- 子任务 A: 计算最少需要从多少个学校分发软件 ---\n    # 这等价于计算缩点后DAG中入度为0的SCC的数量。\n\n    # scc_in_degree[k] 存储第k个SCC在缩点图中的入度\n    # scc_out_degree[k] 存储第k个SCC在缩点图中的出度\n    scc_in_degree = [0] * (scc_count + 1)\n    scc_out_degree = [0] * (scc_count + 1)\n\n    # 使用一个集合来存储缩点图中已添加的边，以避免重复计算入度和出度\n    condensation_graph_edges = set()\n\n    # 遍历原图的所有边，构建缩点图的入度和出度\n    for u in range(1, N + 1):\n        for v in graph[u]:\n            # 如果一条边连接了两个不同的SCC，则在缩点图中存在一条边\n            if scc_id[u] != scc_id[v]:\n                # 如果这条SCC间的边尚未被记录，则增加相应的入度和出度\n                if (scc_id[u], scc_id[v]) not in condensation_graph_edges:\n                    scc_out_degree[scc_id[u]] += 1\n                    scc_in_degree[scc_id[v]] += 1\n                    condensation_graph_edges.add((scc_id[u], scc_id[v]))\n\n    num_source_sccs = 0 # 入度为0的SCC数量\n    num_sink_sccs = 0   # 出度为0的SCC数量\n\n    # 统计入度为0和出度为0的SCC\n    for i in range(1, scc_count + 1):\n        if scc_in_degree[i] == 0:\n            num_source_sccs += 1\n        if scc_out_degree[i] == 0:\n            num_sink_sccs += 1\n\n    # 子任务A的答案是入度为0的SCC数量\n    # 从这些SCC中的任一学校开始分发，即可覆盖所有学校。\n    ans_A = num_source_sccs\n    print(ans_A)\n\n    # --- 子任务 B: 计算最少需要添加多少条边才能使整个网络强连通 ---\n    # 如果整个图本身就是一个SCC（scc_count == 1），则已经强连通，无需添加边。\n    if scc_count == 1:\n        print(0)\n    else:\n        # 否则，为了使整个图强连通，需要将所有“源”SCC连接到“汇”SCC，并最终形成一个大环。\n        # 最少需要添加的边数是源SCC数量和汇SCC数量的最大值。\n        ans_B = max(num_source_sccs, num_sink_sccs)\n        print(ans_B)\n\n# 执行主函数\nsolve()\n'
NUMBER=1236
SAMPLE='5\n2 4 3 0\n4 5 0\n0\n0\n1 0\n'
CASES=40
def run(x):
 with tempfile.TemporaryDirectory() as t:
  p=Path(t)/'s.py';p.write_text(REFERENCE);q=subprocess.run([sys.executable,'-I',str(p)],input=x,text=True,capture_output=True,timeout=120)
  if q.returncode:raise SystemExit(q.stderr)
  return '\n'.join(line.rstrip() for line in q.stdout.rstrip().splitlines())+'\n'
def main():
 d=Path('data');d.mkdir(exist_ok=True)
 for p in d.glob('*'):p.unlink()
 for i,x in enumerate([SAMPLE]+[generate(s) for s in range(1, CASES)]):
  assert valid(x),i
  (d/f'{i}.in').write_text(x);(d/f'{i}.out').write_text(run(x))
if __name__=='__main__':main()

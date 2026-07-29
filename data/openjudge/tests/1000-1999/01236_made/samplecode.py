# Source collection: /home/rocky/git/2024spring-cs201/2024spring_dsa_problems.md
# Heading: 1236: Network of Schools
# Fenced code block index: 2
# Source URL: https://github.com/GMyhf/2024spring-cs201/blob/main/2024spring_dsa_problems.md
# Upstream problem: http://cs101.openjudge.cn/practice/01236/
# License: not declared; no license is inferred.
import sys

# 设置递归深度限制，以应对N=100的DFS调用
# Python默认递归限制通常是1000，对于N=100的图，2000是绰绰有余的。
sys.setrecursionlimit(2000)

# 全局变量用于存储图和Tarjan算法的状态
N = 0
graph = []

# Tarjan算法相关变量
timer = 0
dfn = []         # 节点的发现时间 (discovery time)
low = []         # 从节点u或其子树能追溯到的最早的发现时间 (lowest reachable discovery time)
stack = []       # DFS栈，存储当前正在访问的节点
in_stack = []    # 布尔数组，标记节点是否在栈中
scc_id = []      # 存储每个节点所属的SCC的ID
scc_count = 0    # 已找到的SCC的总数

def tarjan(u):
    """
    Tarjan算法的DFS实现，用于寻找强连通分量。
    u: 当前正在访问的节点
    """
    global timer, scc_count

    timer += 1
    dfn[u] = timer
    low[u] = timer
    stack.append(u)
    in_stack[u] = True

    # 遍历节点u的所有邻居v
    for v in graph[u]:
        if dfn[v] == -1: # 如果v尚未访问
            tarjan(v)
            # 递归返回后，更新low[u]。u可以到达v能到达的最早发现时间。
            low[u] = min(low[u], low[v])
        elif in_stack[v]: # 如果v已经在栈中，说明是回边，或者v在同一个SCC中
            # 更新low[u]。u可以到达v，所以u可以到达v的发现时间。
            # 这里必须使用dfn[v]而不是low[v]，因为low[v]可能已经被子树更新到更早的时间，
            # 而我们关注的是u通过v能够直接回溯到的栈中祖先。
            low[u] = min(low[u], dfn[v])

    # 如果dfn[u] == low[u]，说明u是某个SCC的根节点
    if dfn[u] == low[u]:
        scc_count += 1
        # 从栈中弹出所有属于当前SCC的节点，直到u被弹出
        while True:
            node = stack.pop()
            in_stack[node] = False
            scc_id[node] = scc_count # 分配SCC ID
            if node == u:
                break

def solve():
    """
    主函数：读取输入，运行Tarjan算法，并解决两个子任务。
    """
    global N, graph, timer, dfn, low, stack, in_stack, scc_id, scc_count

    # 读取学校数量N
    N = int(sys.stdin.readline())
    # 初始化邻接列表，使用1-based索引
    graph = [[] for _ in range(N + 1)]

    # 读取每个学校的分发列表，构建图
    for i in range(1, N + 1):
        line = list(map(int, sys.stdin.readline().split()))
        # 输入列表以0结束，因此遍历到倒数第二个元素
        for j in range(len(line) - 1):
            graph[i].append(line[j])

    # 初始化Tarjan算法所需变量
    timer = 0
    dfn = [-1] * (N + 1)
    low = [-1] * (N + 1)
    stack = []
    in_stack = [False] * (N + 1)
    scc_id = [0] * (N + 1) # scc_id[i] 表示节点i所属的SCC编号
    scc_count = 0 # 强连通分量计数器

    # 对所有未访问的节点运行Tarjan算法，确保处理所有连通分量
    for i in range(1, N + 1):
        if dfn[i] == -1: # 如果节点i尚未被访问
            tarjan(i)

    # --- 子任务 A: 计算最少需要从多少个学校分发软件 ---
    # 这等价于计算缩点后DAG中入度为0的SCC的数量。

    # scc_in_degree[k] 存储第k个SCC在缩点图中的入度
    # scc_out_degree[k] 存储第k个SCC在缩点图中的出度
    scc_in_degree = [0] * (scc_count + 1)
    scc_out_degree = [0] * (scc_count + 1)

    # 使用一个集合来存储缩点图中已添加的边，以避免重复计算入度和出度
    condensation_graph_edges = set()

    # 遍历原图的所有边，构建缩点图的入度和出度
    for u in range(1, N + 1):
        for v in graph[u]:
            # 如果一条边连接了两个不同的SCC，则在缩点图中存在一条边
            if scc_id[u] != scc_id[v]:
                # 如果这条SCC间的边尚未被记录，则增加相应的入度和出度
                if (scc_id[u], scc_id[v]) not in condensation_graph_edges:
                    scc_out_degree[scc_id[u]] += 1
                    scc_in_degree[scc_id[v]] += 1
                    condensation_graph_edges.add((scc_id[u], scc_id[v]))

    num_source_sccs = 0 # 入度为0的SCC数量
    num_sink_sccs = 0   # 出度为0的SCC数量

    # 统计入度为0和出度为0的SCC
    for i in range(1, scc_count + 1):
        if scc_in_degree[i] == 0:
            num_source_sccs += 1
        if scc_out_degree[i] == 0:
            num_sink_sccs += 1

    # 子任务A的答案是入度为0的SCC数量
    # 从这些SCC中的任一学校开始分发，即可覆盖所有学校。
    ans_A = num_source_sccs
    print(ans_A)

    # --- 子任务 B: 计算最少需要添加多少条边才能使整个网络强连通 ---
    # 如果整个图本身就是一个SCC（scc_count == 1），则已经强连通，无需添加边。
    if scc_count == 1:
        print(0)
    else:
        # 否则，为了使整个图强连通，需要将所有“源”SCC连接到“汇”SCC，并最终形成一个大环。
        # 最少需要添加的边数是源SCC数量和汇SCC数量的最大值。
        ans_B = max(num_source_sccs, num_sink_sccs)
        print(ans_B)

# 执行主函数
solve()

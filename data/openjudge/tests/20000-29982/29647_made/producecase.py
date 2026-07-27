import random
REFERENCE="# External reference: /practice/29647/statistics/\n# Accepted submission: 52829529\n# Source: http://cs101.openjudge.cn/practice/solution/52829529/\n# License: not declared on the submission page; no license is inferred.\n\nimport sys\n\ndef solve():\n    # 增加递归深度限制，防止树退化为链时导致栈溢出\n    sys.setrecursionlimit(2000)\n    \n    # 一次性读取所有输入数据\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n    \n    n = int(input_data[0])\n    \n    # 存储快乐指数，下标从 1 开始\n    r = [0] * (n + 1)\n    for i in range(1, n + 1):\n        r[i] = int(input_data[i])\n    \n    # 构建邻接表和记录是否有上司\n    adj = [[] for _ in range(n + 1)]\n    has_parent = [False] * (n + 1)\n    \n    idx = n + 1\n    # 读取 n - 1 条关系\n    for _ in range(n - 1):\n        if idx >= len(input_data):\n            break\n        l = int(input_data[idx])\n        k = int(input_data[idx + 1])\n        adj[k].append(l)  # k 是 l 的直接上司\n        has_parent[l] = True\n        idx += 2\n        \n    # 寻找根节点（没有直接上司的职员）\n    root = 1\n    for i in range(1, n + 1):\n        if not has_parent[i]:\n            root = i\n            break\n            \n    # 定义树形 DP 的 DFS 函数\n    # 返回一个元组 (dp[u][0], dp[u][1])\n    # dp[u][0] 表示 u 不参加的最大值，dp[u][1] 表示 u 参加的最大值\n    def dfs(u):\n        dp_u_0 = 0\n        dp_u_1 = r[u]\n        \n        for v in adj[u]:\n            dp_v_0, dp_v_1 = dfs(v)\n            # u 不参加：子节点 v 可以参加，也可以不参加\n            dp_u_0 += max(dp_v_0, dp_v_1)\n            # u 参加：子节点 v 绝对不能参加\n            dp_u_1 += dp_v_0\n            \n        return dp_u_0, dp_u_1\n\n    # 从根节点开始搜索\n    ans_0, ans_1 = dfs(root)\n    \n    # 输出最大快乐指数\n    print(max(ans_0, ans_1))\n\nif __name__ == '__main__':\n    solve()"
SAMPLE='7\n1\n1\n1\n1\n1\n1\n1\n1 3\n2 3\n6 4\n7 4\n4 5\n3 5\n'
GENERATOR_NAME='g29647'
def g29647(r):
    n = r.randint(2, 80); value = [r.randint(0, 100) for _ in range(n)]
    edges = [f"{i} {r.randint(1, i - 1)}" for i in range(2, n + 1)]
    return f"{n}\n" + "\n".join(map(str, value)) + "\n" + "\n".join(edges) + "\n"

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

import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'import sys\n\n# 增加递归深度限制，防止处理大规模 $N$ 时溢出\nsys.setrecursionlimit(200000)\n\nclass SegmentTree:\n    def __init__(self, n):\n        self.n = n\n        # tree[i] 存储对应区间的最大值\n        self.tree = [0] * (4 * n)\n        # lazy[i] 存储懒标记（增加的力）\n        self.lazy = [0] * (4 * n)\n\n    def _push_up(self, node):\n        """向上更新，父节点的值等于子节点的最大值"""\n        self.tree[node] = max(self.tree[2 * node], self.tree[2 * node + 1])\n\n    def _push_down(self, node):\n        """向下传播懒标记"""\n        if self.lazy[node] != 0:\n            add_val = self.lazy[node]\n            \n            # 更新左子节点\n            self.tree[2 * node] += add_val\n            self.lazy[2 * node] += add_val\n            \n            # 更新右子节点\n            self.tree[2 * node + 1] += add_val\n            self.lazy[2 * node + 1] += add_val\n            \n            # 清除当前节点的标记\n            self.lazy[node] = 0\n\n    def update(self, node, start, end, l, r, v):\n        """区间更新：将 [l, r] 范围内的值加上 v"""\n        if l <= start and end <= r:\n            self.tree[node] += v\n            self.lazy[node] += v\n            return\n        \n        mid = (start + end) // 2\n        self._push_down(node)\n        \n        if l <= mid:\n            self.update(2 * node, start, mid, l, r, v)\n        if r > mid:\n            self.update(2 * node + 1, mid + 1, end, l, r, v)\n            \n        self._push_up(node)\n\n    def query(self, node, start, end, l, r):\n        """区间查询：获取 [l, r] 范围内的最大值"""\n        if l <= start and end <= r:\n            return self.tree[node]\n        \n        mid = (start + end) // 2\n        self._push_down(node)\n        \n        res = -float(\'inf\')\n        if l <= mid:\n            res = max(res, self.query(2 * node, start, mid, l, r))\n        if r > mid:\n            res = max(res, self.query(2 * node + 1, mid + 1, end, l, r))\n        return res\n\ndef solve():\n    # 使用快速读取\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n    \n    N = int(input_data[0])\n    Q = int(input_data[1])\n    \n    st = SegmentTree(N)\n    \n    idx = 2\n    results = []\n    \n    for _ in range(Q):\n        op = input_data[idx]\n        if op == "Add":\n            l = int(input_data[idx + 1])\n            r = int(input_data[idx + 2])\n            v = int(input_data[idx + 3])\n            st.update(1, 1, N, l, r, v)\n            idx += 4\n        elif op == "Query":\n            l = int(input_data[idx + 1])\n            r = int(input_data[idx + 2])\n            results.append(str(st.query(1, 1, N, l, r)))\n            idx += 3\n            \n    # 一次性输出所有查询结果\n    sys.stdout.write("\\n".join(results) + "\\n")\n\nif __name__ == "__main__":\n    solve()\n'
SAMPLE_IN = '5 4\nAdd 1 3 10\nQuery 2 4\nAdd 3 5 5\nQuery 2 4\n'
def generate_case(r):
    n = r.randint(2, 30); ops = []
    for _ in range(r.randint(4, 20)):
        l, rr = sorted((r.randint(1, n), r.randint(1, n)))
        if r.random() < .6: ops.append(f"Add {l} {rr} {r.randint(-50, 50)}")
        else: ops.append(f"Query {l} {rr}")
    if not any(x.startswith("Query") for x in ops): ops.append(f"Query 1 {n}")
    return f"{n} {len(ops)}\n" + "\n".join(ops) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(21):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(30878 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

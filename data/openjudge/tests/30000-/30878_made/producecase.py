import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'import sys\n\n# 增加递归深度限制，防止处理大规模 $N$ 时溢出\nsys.setrecursionlimit(200000)\n\nclass SegmentTree:\n    def __init__(self, n):\n        self.n = n\n        # tree[i] 存储对应区间的最大值\n        self.tree = [0] * (4 * n)\n        # lazy[i] 存储懒标记（增加的力）\n        self.lazy = [0] * (4 * n)\n\n    def _push_up(self, node):\n        """向上更新，父节点的值等于子节点的最大值"""\n        self.tree[node] = max(self.tree[2 * node], self.tree[2 * node + 1])\n\n    def _push_down(self, node):\n        """向下传播懒标记"""\n        if self.lazy[node] != 0:\n            add_val = self.lazy[node]\n            \n            # 更新左子节点\n            self.tree[2 * node] += add_val\n            self.lazy[2 * node] += add_val\n            \n            # 更新右子节点\n            self.tree[2 * node + 1] += add_val\n            self.lazy[2 * node + 1] += add_val\n            \n            # 清除当前节点的标记\n            self.lazy[node] = 0\n\n    def update(self, node, start, end, l, r, v):\n        """区间更新：将 [l, r] 范围内的值加上 v"""\n        if l <= start and end <= r:\n            self.tree[node] += v\n            self.lazy[node] += v\n            return\n        \n        mid = (start + end) // 2\n        self._push_down(node)\n        \n        if l <= mid:\n            self.update(2 * node, start, mid, l, r, v)\n        if r > mid:\n            self.update(2 * node + 1, mid + 1, end, l, r, v)\n            \n        self._push_up(node)\n\n    def query(self, node, start, end, l, r):\n        """区间查询：获取 [l, r] 范围内的最大值"""\n        if l <= start and end <= r:\n            return self.tree[node]\n        \n        mid = (start + end) // 2\n        self._push_down(node)\n        \n        res = -float(\'inf\')\n        if l <= mid:\n            res = max(res, self.query(2 * node, start, mid, l, r))\n        if r > mid:\n            res = max(res, self.query(2 * node + 1, mid + 1, end, l, r))\n        return res\n\ndef solve():\n    # 使用快速读取\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n    \n    N = int(input_data[0])\n    Q = int(input_data[1])\n    \n    st = SegmentTree(N)\n    \n    idx = 2\n    results = []\n    \n    for _ in range(Q):\n        op = input_data[idx]\n        if op == "Add":\n            l = int(input_data[idx + 1])\n            r = int(input_data[idx + 2])\n            v = int(input_data[idx + 3])\n            st.update(1, 1, N, l, r, v)\n            idx += 4\n        elif op == "Query":\n            l = int(input_data[idx + 1])\n            r = int(input_data[idx + 2])\n            results.append(str(st.query(1, 1, N, l, r)))\n            idx += 3\n            \n    # 一次性输出所有查询结果\n    sys.stdout.write("\\n".join(results) + "\\n")\n\nif __name__ == "__main__":\n    solve()\n'
SAMPLE_IN = '5 4\nAdd 1 3 10\nQuery 2 4\nAdd 3 5 5\nQuery 2 4\n'
SAMPLE_IN2 = '3 2\nAdd 1 3 -5\nQuery 1 3\n'   # 题面样例 2
def generate_case(r):
    n = r.randint(2, 30); ops = []
    for _ in range(r.randint(4, 20)):
        l, rr = sorted((r.randint(1, n), r.randint(1, n)))
        if r.random() < .6: ops.append(f"Add {l} {rr} {r.randint(-50, 50)}")
        else: ops.append(f"Query {l} {rr}")
    if not any(x.startswith("Query") for x in ops): ops.append(f"Query 1 {n}")
    return f"{n} {len(ops)}\n" + "\n".join(ops) + "\n"


def valid(text):
    """题面契约：第一行 N Q（1<=N,Q<=1e5）；接下来 Q 行，"Add l r v" 或 "Query l r"，
    1<=l<=r<=N，-1e9<=v<=1e9。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    def isint(x, signed=False):
        try:
            return str(int(x)) == x and (signed or x.isdigit())
        except ValueError:
            return False
    head = lines[0].split(" ")
    if len(head) != 2 or not all(isint(x) for x in head):
        return False
    n, q = map(int, head)
    if not (1 <= n <= 100000 and 1 <= q <= 100000) or len(lines) != q + 1:
        return False
    for line in lines[1:]:
        t = line.split(" ")
        if t[0] == "Add" and len(t) == 4:
            if not (isint(t[1]) and isint(t[2]) and isint(t[3], True)) or not -10**9 <= int(t[3]) <= 10**9:
                return False
        elif t[0] == "Query" and len(t) == 3:
            if not (isint(t[1]) and isint(t[2])):
                return False
        else:
            return False
        if not 1 <= int(t[1]) <= int(t[2]) <= n:
            return False
    return True


def make_case(r, n, q, add_p=0.5, vlo=-10**9, vhi=10**9, span="mixed"):
    ops = []
    for _ in range(q):
        mode = span if span != "mixed" else r.choice(["any", "any", "wide", "point", "short"])
        if mode == "wide":
            l = r.randint(1, max(1, n // 10)); rr = r.randint(n - n // 10, n)
        elif mode == "point":
            l = rr = r.randint(1, n)
        elif mode == "short":
            l = r.randint(1, n); rr = min(n, l + r.randint(0, 20))
        else:
            l, rr = sorted((r.randint(1, n), r.randint(1, n)))
        if r.random() < add_p: ops.append(f"Add {l} {rr} {r.randint(vlo, vhi)}")
        else: ops.append(f"Query {l} {rr}")
    return f"{n} {q}\n" + "\n".join(ops) + "\n"


def special_cases():
    """替换原第 20..39 组：原数据 N<=30、|v|<=50，O(NQ) 暴力与 int 溢出都卡不住。
    Q 受单组 .in<=1MB 限制，满规模 3 组取 4e4 左右（长区间，卡 O(NQ) 与溢出）；
    其余组 Q 取 1.1e4~1.5e4，控制 data/ 合计 <= 10MB。"""
    r = random.Random(308780)
    N = 100000
    out = []
    out.append("1 1\nQuery 1 1\n")                                          # 无 Add，最大值为 0
    out.append("1 3\nAdd 1 1 -1000000000\nQuery 1 1\nAdd 1 1 1000000000\n")  # 负值，末尾 Add 后无查询
    out.append("100000 1\nQuery 1 100000\n")                               # 大 N 只查询
    out.append(make_case(r, 2, 20, vlo=-5, vhi=5))
    out.append(make_case(r, 7, 40, vlo=-10**9, vhi=10**9))
    out.append(make_case(r, 50, 200, vlo=-100, vhi=100))
    out.append(make_case(r, 1000, 2000, vlo=-10**9, vhi=-1))                  # 全负：初值 0 不能参与比较
    out.append(make_case(r, 3000, 5000))
    out.append(make_case(r, 10000, 10000, add_p=0.3))
    out.append(make_case(r, N, 12000))                                          # 满值域随机
    out.append(make_case(r, N, 42000, add_p=0.6, span="wide"))                  # 满规模①长区间：卡 O(NQ)
    out.append(make_case(r, N, 40000, add_p=0.7, vlo=10**9, vhi=10**9, span="wide"))   # 满规模②累加到 ~3e13，卡 32 位
    out.append(make_case(r, N, 40000, add_p=0.7, vlo=-10**9, vhi=-10**9, span="wide")) # 满规模③负向溢出
    out.append(make_case(r, N, 15000, add_p=0.5, span="point"))
    out.append(make_case(r, N, 13000, add_p=0.5, span="short"))
    out.append(make_case(r, N, 14000, add_p=0.2))                               # 查询为主
    out.append(make_case(r, N, 11000, add_p=0.9))                               # 修改为主
    out.append(make_case(r, 65536, 13000, vlo=-3, vhi=3))                       # 2 的幂长度、小值域大量并列最大
    out.append(make_case(r, 99999, 12000, vlo=-10**9, vhi=10**9 // 2))         # 奇数长度，偏负
    out.append(make_case(r, N, 12000, add_p=0.5, vlo=-10**9, vhi=10**9, span="mixed"))
    return out


def main():
    specials = special_cases()
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        for index in range(40):
            if index == 0: content = SAMPLE_IN
            elif index == 1: content = SAMPLE_IN2
            elif index >= 20: content = specials[index - 20]
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(30878 + index + attempt * 1000))
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
            assert valid(content) and (index == 0 or content not in seen), index
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=60, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()

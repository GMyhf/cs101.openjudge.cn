import random, re, subprocess, sys, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'import sys\n\n\ndef solve():\n    # 使用 sys.stdin.read 快速读取所有输入\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n\n    k = int(input_data[0])\n    n = int(input_data[1])\n\n    num_nodes = 1 << k\n    sz = [0] * num_nodes\n\n    # 预计算每个节点的子树大小\n    for i in range(1, num_nodes):\n        depth = i.bit_length()  # i 的二进制长度即为其所在的深度\n        h = k - depth + 1\n        sz[i] = (1 << h) - 1\n\n    sum_tree = [0] * num_nodes\n    lazy = [0] * num_nodes\n\n    idx = 2\n    out = []\n\n    for _ in range(n):\n        op = int(input_data[idx])\n        if op == 1:\n            x = int(input_data[idx + 1])\n            y = int(input_data[idx + 2])\n            idx += 3\n\n            # 1. 更新操作\n            lazy[x] += y\n            add_val = sz[x] * y\n            p = x\n            # 向上更新所有祖先节点的 subtree sum\n            while p > 0:\n                sum_tree[p] += add_val\n                p >>= 1\n        else:\n            x = int(input_data[idx + 1])\n            idx += 2\n\n            # 2. 查询操作\n            lazy_sum = 0\n            p = x >> 1\n            # 向上累加所有严格祖先节点的 lazy 标记\n            while p > 0:\n                lazy_sum += lazy[p]\n                p >>= 1\n            res = sum_tree[x] + sz[x] * lazy_sum\n            out.append(str(res))\n\n    # 批量输出结果\n    sys.stdout.write("\\n".join(out) + "\\n")\n\n\nif __name__ == "__main__":\n    solve()\n'
SAMPLE_IN = '3 7\n1 2 1\n2 4\n1 6 3\n2 1\n1 3 -2\n1 4 1\n2 3\n'
SAMPLE_OUT = '1\n6\n-3\n'


def valid(text):
    """题面：第一行 k n（k<=15，n<=50000）；接下来 n 行，每行 "1 x y"（y 为整数且 |y|<=100）或 "2 x"，x 为 1..2^k-1 的节点编号。"""
    lines = text.split("\n")
    if not lines or lines[-1] != "":
        return False
    lines.pop()
    head = lines[0].split(" ") if lines else []
    if len(head) != 2 or not all(re.fullmatch(r"[1-9]\d*", t) for t in head):
        return False
    k, n = map(int, head)
    if not (1 <= k <= 15 and 1 <= n <= 50000) or len(lines) != n + 1:
        return False
    nodes = (1 << k) - 1
    for row in lines[1:]:
        t = row.split(" ")
        if t[0] == "1" and len(t) == 3:
            if not re.fullmatch(r"-?(0|[1-9]\d*)", t[2]) or t[2] == "-0" or abs(int(t[2])) > 100:
                return False
        elif not (t[0] == "2" and len(t) == 2):
            return False
        if not re.fullmatch(r"[1-9]\d*", t[1]) or int(t[1]) > nodes:
            return False
    return True


def old_case(r):
    k = r.randint(1, 8); nodes = 2 ** k - 1; lines = []
    for _ in range(r.randint(10, 45)):
        x = r.randint(1, nodes)
        if r.random() < .6:
            lines.append(f"1 {x} {r.randint(-100, 100)}")
        else:
            lines.append(f"2 {x}")
    return f"{k} {len(lines)}\n" + "\n".join(lines) + "\n"


def pack(k, ops):
    return f"{k} {len(ops)}\n" + "\n".join(ops) + "\n"


def pick_node(r, k, mode):
    nodes = (1 << k) - 1
    if mode == "top":            # 靠近根：子树大
        return r.randint(1, min(nodes, 15))
    if mode == "leaf":
        return r.randint(1 << (k - 1), nodes)
    d = r.randint(1, k)          # 按深度均匀
    return r.randint(1 << (d - 1), (1 << d) - 1)


def big(r, k, n, upd_mode, qry_mode, p_upd=.5, yfix=None):
    ops = []
    for i in range(n):
        if r.random() < p_upd and i < n - 1:
            y = yfix if yfix is not None else r.randint(-100, 100)
            ops.append(f"1 {pick_node(r, k, upd_mode)} {y}")
        else:
            ops.append(f"2 {pick_node(r, k, qry_mode)}")
    return pack(k, ops)


def build_cases():
    cases, seen = [SAMPLE_IN], [SAMPLE_IN]
    for index in range(1, 9):                         # 原随机小数据保留前 8 组
        for attempt in range(100):
            content = old_case(random.Random(24686 + index + attempt * 1000))
            if content not in seen: break
        seen.append(content); cases.append(content)
    r = random.Random(246860)
    cases.append(pack(1, ["2 1", "1 1 -100", "2 1", "1 1 100", "1 1 100", "2 1"]))     # k=1
    cases.append(pack(15, ["2 1", "1 16384 5", "2 1", "2 2", "2 3", "2 16384", "1 1 0", "2 32767"]))  # 叶子更新，y=0
    cases.append(big(r, 15, 50000, "top", "top", .6, 100))           # 根附近全 +100：和约 1.6e11，超 32 位
    cases.append(big(r, 15, 50000, "top", "top", .6, -100))          # 全 -100
    cases.append(big(r, 15, 50000, "top", "any", .5))                # 卡逐点更新的暴力
    cases.append(big(r, 15, 50000, "any", "top", .5))                # 卡逐点求和的暴力
    cases.append(big(r, 15, 50000, "any", "any", .5))
    cases.append(big(r, 15, 50000, "leaf", "leaf", .5))
    cases.append(big(r, 10, 50000, "any", "any", .3))
    cases.append(big(r, 4, 2000, "any", "any", .5))
    cases.append(big(r, 15, 50000, "top", "leaf", .9))                # 更新多、查询少
    return cases


def main():
    cases = build_cases()
    assert len(cases) == 20 and len(set(cases)) == 20 and all(valid(c) for c in cases)
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        for index, content in enumerate(cases):
            result = subprocess.run([sys.executable, handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            if index == 0: assert result.stdout == SAMPLE_OUT
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()

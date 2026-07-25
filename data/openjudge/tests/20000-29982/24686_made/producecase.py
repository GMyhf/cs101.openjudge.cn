import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'import sys\n\n\ndef solve():\n    # 使用 sys.stdin.read 快速读取所有输入\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        return\n\n    k = int(input_data[0])\n    n = int(input_data[1])\n\n    num_nodes = 1 << k\n    sz = [0] * num_nodes\n\n    # 预计算每个节点的子树大小\n    for i in range(1, num_nodes):\n        depth = i.bit_length()  # i 的二进制长度即为其所在的深度\n        h = k - depth + 1\n        sz[i] = (1 << h) - 1\n\n    sum_tree = [0] * num_nodes\n    lazy = [0] * num_nodes\n\n    idx = 2\n    out = []\n\n    for _ in range(n):\n        op = int(input_data[idx])\n        if op == 1:\n            x = int(input_data[idx + 1])\n            y = int(input_data[idx + 2])\n            idx += 3\n\n            # 1. 更新操作\n            lazy[x] += y\n            add_val = sz[x] * y\n            p = x\n            # 向上更新所有祖先节点的 subtree sum\n            while p > 0:\n                sum_tree[p] += add_val\n                p >>= 1\n        else:\n            x = int(input_data[idx + 1])\n            idx += 2\n\n            # 2. 查询操作\n            lazy_sum = 0\n            p = x >> 1\n            # 向上累加所有严格祖先节点的 lazy 标记\n            while p > 0:\n                lazy_sum += lazy[p]\n                p >>= 1\n            res = sum_tree[x] + sz[x] * lazy_sum\n            out.append(str(res))\n\n    # 批量输出结果\n    sys.stdout.write("\\n".join(out) + "\\n")\n\n\nif __name__ == "__main__":\n    solve()\n'
SAMPLE_IN = '3 7\n1 2 1\n2 4\n1 6 3\n2 1\n1 3 -2\n1 4 1\n2 3\n'
SAMPLE_OUT = '1\n6\n-3\n'
def generate_case(r):
    k = r.randint(1, 8); nodes = 2 ** k - 1; lines = []
    for _ in range(r.randint(10, 45)):
        x = r.randint(1, nodes)
        if r.random() < .6:
            lines.append(f"1 {x} {r.randint(-100, 100)}")
        else:
            lines.append(f"2 {x}")
    assert all(1 <= int(line.split()[1]) <= nodes for line in lines)
    return f"{k} {len(lines)}\n" + "\n".join(lines) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0:
            content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(24686 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

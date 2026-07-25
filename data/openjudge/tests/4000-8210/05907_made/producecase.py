"""5907 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001c
生成器与循环取自 scripts/build_001c.py（批次 001c），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 5907
SAMPLE_IN = '2\n5 5\n0 1 2\n1 -1 -1\n2 3 4\n3 -1 -1\n4 -1 -1\n2 0\n1 1 2\n2 0\n1 3 4\n2 2\n3 2\n0 1 2\n1 -1 -1\n2 -1 -1\n1 1 2\n2 0\n'
SAMPLE_OUT = '1\n3\n4\n2\n'
REFERENCE_SOURCE = '# 数学科学学院 王镜廷 2300010724\ndef find_leftmost_node(son, u):\n    while son[u][0] != -1:\n        u = son[u][0]\n    return u\n\ndef main():\n    t = int(input())\n    for _ in range(t):\n        n, m = map(int, input().split())\n\n        son = [-1] * (n + 1)  # 存储每个节点的子节点\n        parent = {}  # 存储每个节点的父节点和方向，{节点: (父节点, 方向)}\n\n        for _ in range(n):\n            i, u, v = map(int, input().split())\n            son[i] = [u, v]\n            parent[u] = (i, 0)  # 左子节点\n            parent[v] = (i, 1)  # 右子节点\n\n        for _ in range(m):\n            s = input().split()\n            if s[0] == "1":\n                u, v = map(int, s[1:])\n                fu, diru = parent[u]\n                fv, dirv = parent[v]\n                son[fu][diru] = v\n                son[fv][dirv] = u\n                parent[v] = (fu, diru)\n                parent[u] = (fv, dirv)\n            elif s[0] == "2":\n                u = int(s[1])\n                root = find_leftmost_node(son, u)\n                print(root)\n\nif __name__ == "__main__":\n    main()\n'

def g5907(r):
    cases = []
    for _ in range(r.randint(1, 3)):
        n = r.randint(3, 10); m = r.randint(2, 10)
        children = [[-1, -1] for _ in range(n)]
        leaves = list(range(n))
        for i in range(1, n):
            parent = (i - 1) // 2
            children[parent][i % 2] = i
        ops = []
        leaf_ids = [i for i, pair in enumerate(children) if pair == [-1, -1]]
        for _ in range(m):
            if len(leaf_ids) >= 2 and r.random() < .45:
                a, b = r.sample(leaf_ids, 2); ops.append(f"1 {a} {b}")
            else:
                ops.append(f"2 {r.randrange(n)}")
        lines = [f"{n} {m}"] + [f"{i} {a} {b}" for i, (a, b) in enumerate(children)] + ops
        cases.append("\n".join(lines))
    return str(len(cases)) + "\n" + "\n".join(cases) + "\n"

def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g5907(random.Random(NUMBER + i + attempt * 1000))
            if value not in cases:
                cases.append(value)
                break
        else:
            raise AssertionError("生成器多样性不足")
    return cases

def solve_reference(content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE)
        handle.flush()
        result = subprocess.run(["python3", handle.name], input=content, text=True,
                                capture_output=True, timeout=120, check=True)
    return result.stdout


def main():
    cases = build_cases()
    assert cases[0] == SAMPLE_IN, "第 0 组必须是题面样例"
    assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split(), "参考解法跑不出样例输出"
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for index, content in enumerate(cases):
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")


if __name__ == "__main__":
    main()

"""4109 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001a
生成器与循环取自 scripts/build_001a.py（批次 001a），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import re
import subprocess
import tempfile
from pathlib import Path

NUMBER = 4109
SAMPLE_IN = '2\n3 2 2\n1 2\n2 3\n1 3\n1 2\n5 5 2\n1 2\n1 3\n2 5\n3 5\n4 5\n1 5\n3 4\n'
SAMPLE_OUT = 'Case 1:\n1\n0\nCase 2:\n2\n1\n'
REFERENCE_SOURCE = 'def count_common_friends(n, m, k, friend_connections, queries):\n    # Create a dictionary to store friend connections\n    friends_dict = {}\n    for i in range(1, n + 1):\n        friends_dict[i] = set()\n\n    # Update the dictionary with friend connections\n    for i, j in friend_connections:\n        friends_dict[i].add(j)\n        friends_dict[j].add(i)\n\n    # Count common friends for each query\n    results = []\n    for i, j in queries:\n        common_friends = len(friends_dict[i].intersection(friends_dict[j]))\n        results.append(common_friends)\n\n    return results\n\n\ndef main():\n    test_cases = int(input())\n    for case in range(1, test_cases + 1):\n        n, m, k = map(int, input().split())\n        friend_connections = []\n        queries = []\n\n        # Read friend connections\n        for _ in range(m):\n            i, j = map(int, input().split())\n            friend_connections.append((i, j))\n\n        # Read queries\n        for _ in range(k):\n            i, j = map(int, input().split())\n            queries.append((i, j))\n\n        # Count common friends and output the results\n        print(f"Case {case}:")\n        results = count_common_friends(n, m, k, friend_connections, queries)\n        for result in results:\n            print(result)\n\n\nif __name__ == "__main__":\n    main()\n'

def valid(text):
    """题面契约：第一行正整数 c；随后 c 组，每组首行 n m k（2<=n<=100，m、k 为非负整数），
    接着 m 行朋友关系、k 行询问，每行两个整数 i j（1<=i,j<=n）。不允许多余 token。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if not re.fullmatch(r"[1-9]\d*", lines[0]):
        return False
    c = int(lines[0])
    pos = 1
    num = r"0|[1-9]\d*"
    for _ in range(c):
        if pos >= len(lines):
            return False
        head = lines[pos].split(" ")
        if len(head) != 3 or not all(re.fullmatch(num, x) for x in head):
            return False
        n, m, k = map(int, head)
        if not 2 <= n <= 100:
            return False
        pos += 1
        if pos + m + k > len(lines):
            return False
        for line in lines[pos:pos + m + k]:
            ij = line.split(" ")
            if len(ij) != 2 or not all(re.fullmatch(num, x) and 1 <= int(x) <= n for x in ij):
                return False
        pos += m + k
    return pos == len(lines)


def graph_block(r, n, m, k, edges=None, queries=None):
    """无自环、无重边的随机图；询问 i != j。"""
    if edges is None:
        allp = [(i, j) for i in range(1, n + 1) for j in range(i + 1, n + 1)]
        edges = r.sample(allp, min(m, len(allp)))
        edges = [(a, b) if r.random() < .5 else (b, a) for a, b in edges]
    if queries is None:
        queries = [tuple(r.sample(range(1, n + 1), 2)) for _ in range(k)]
    lines = [f"{n} {len(edges)} {len(queries)}"]
    lines += [f"{a} {b}" for a, b in edges] + [f"{a} {b}" for a, b in queries]
    return lines


def multi(blocks):
    return "\n".join([str(len(blocks))] + [x for b in blocks for x in b]) + "\n"


def g4109(r):
    blocks = []
    for _ in range(r.randint(2, 6)):
        n = r.randint(2, 30)
        m = r.randint(0, n * (n - 1) // 2)
        blocks.append(graph_block(r, n, m, r.randint(1, 15)))
    return multi(blocks)


def build_cases():
    r = random.Random(NUMBER)
    full = [(i, j) for i in range(1, 101) for j in range(i + 1, 101)]
    star = [(1, j) for j in range(2, 101)]
    cases = [
        SAMPLE_IN,
        multi([graph_block(r, 2, 1, 1, [(1, 2)], [(1, 2)])]),                  # 最小，答案 0
        multi([graph_block(r, 2, 0, 2, [], [(1, 2), (2, 1)])]),                # 没有朋友关系
        multi([graph_block(r, 3, 2, 3, [(1, 2), (3, 2)], [(1, 3), (3, 1), (1, 2)])]),
        multi([graph_block(r, 100, 0, 0, full, [tuple(r.sample(range(1, 101), 2)) for _ in range(300)])]),  # 完全图，98
        multi([graph_block(r, 100, 0, 0, star, [tuple(r.sample(range(2, 101), 2)) for _ in range(200)]
                           + [(1, j) for j in range(2, 30)])]),                 # 星形图
        multi([graph_block(r, 100, 0, 0, [(i, i + 1) for i in range(1, 100)],
                           [(i, i + 2) for i in range(1, 99)] + [(i + 1, i) for i in range(1, 50)])]),  # 链
        # 多组：卡没有在组间清空邻接表、没有按组编号输出
        multi([graph_block(r, 5, 0, 0, [(1, 2), (1, 3), (2, 3)], [(1, 2)])] +
              [graph_block(r, 5, 0, 0, [(4, 5)], [(1, 2), (4, 5)])] * 1 +
              [graph_block(r, 4, 0, 0, [(1, 3), (2, 3), (1, 4), (2, 4)], [(1, 2), (3, 4)])]),
        multi([graph_block(r, r.randint(2, 8), r.randint(0, 10), r.randint(1, 4)) for _ in range(15)]),  # Case 10.. 15
    ]
    for _ in range(7):
        cases.append(g4109(r))
    cases.append(multi([graph_block(r, 100, r.randint(50, 400), 2000) for _ in range(5)]))
    cases.append(multi([graph_block(r, 100, r.randint(2000, 4000), 3000) for _ in range(6)]))
    cases.append(multi([graph_block(r, 100, 4900, 5000) for _ in range(8)]))
    cases.append(multi([graph_block(r, r.randint(90, 100), r.randint(0, 4950), 5000) for _ in range(10)]))
    assert len(cases) == 20  # catalog.json 只登记了 0..19 组
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
        assert valid(content), index
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")


if __name__ == "__main__":
    main()

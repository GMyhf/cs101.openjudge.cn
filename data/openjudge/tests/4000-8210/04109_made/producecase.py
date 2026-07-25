"""4109 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001a
生成器与循环取自 scripts/build_001a.py（批次 001a），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 4109
SAMPLE_IN = '2\n3 2 2\n1 2\n2 3\n1 3\n1 2\n5 5 2\n1 2\n1 3\n2 5\n3 5\n4 5\n1 5\n3 4\n'
SAMPLE_OUT = 'Case 1:\n1\n0\nCase 2:\n2\n1\n'
REFERENCE_SOURCE = 'def count_common_friends(n, m, k, friend_connections, queries):\n    # Create a dictionary to store friend connections\n    friends_dict = {}\n    for i in range(1, n + 1):\n        friends_dict[i] = set()\n\n    # Update the dictionary with friend connections\n    for i, j in friend_connections:\n        friends_dict[i].add(j)\n        friends_dict[j].add(i)\n\n    # Count common friends for each query\n    results = []\n    for i, j in queries:\n        common_friends = len(friends_dict[i].intersection(friends_dict[j]))\n        results.append(common_friends)\n\n    return results\n\n\ndef main():\n    test_cases = int(input())\n    for case in range(1, test_cases + 1):\n        n, m, k = map(int, input().split())\n        friend_connections = []\n        queries = []\n\n        # Read friend connections\n        for _ in range(m):\n            i, j = map(int, input().split())\n            friend_connections.append((i, j))\n\n        # Read queries\n        for _ in range(k):\n            i, j = map(int, input().split())\n            queries.append((i, j))\n\n        # Count common friends and output the results\n        print(f"Case {case}:")\n        results = count_common_friends(n, m, k, friend_connections, queries)\n        for result in results:\n            print(result)\n\n\nif __name__ == "__main__":\n    main()\n'

def sample(body, label):
    fence = r"\x60\x60\x60"
    pattern = rf"(?:{label})\s*\n+{fence}\n(.*?){fence}"
    values = re.findall(pattern, body, re.S | re.I)
    if not values: raise ValueError("missing " + label)
    return values[0].strip() + "\n"

def g4109(r):
    n = r.randint(2, 20); edges = [(i, i + 1) for i in range(1, n)]
    queries = [tuple(r.sample(range(1, n + 1), 2)) for _ in range(r.randint(1, 8))]
    lines = [f"1", f"{n} {len(edges)} {len(queries)}"]
    lines += [f"{a} {b}" for a, b in edges] + [f"{a} {b}" for a, b in queries]
    return "\n".join(lines) + "\n"

def build_cases():
    return [SAMPLE_IN] + [g4109(random.Random(NUMBER + i)) for i in range(1, 20)]

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

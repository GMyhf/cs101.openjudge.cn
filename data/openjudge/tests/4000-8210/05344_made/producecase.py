"""5344 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001b
生成器与循环取自 scripts/build_001b.py（批次 001b），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 5344
SAMPLE_IN = '10 2\n'
SAMPLE_OUT = '2 4 6 8 10 3 7 1 9\n'
REFERENCE_SOURCE = "class Node:\n    def __init__(self, number):\n        self.number = number\n        self.next = None\n\ndef josephus_circle(n, k):\n    # 创建循环链表\n    head = Node(1)\n    current = head\n    for i in range(2, n + 1):\n        new_node = Node(i)\n        current.next = new_node\n        current = new_node\n    current.next = head  # 形成环\n\n    result = []\n    current = head\n    prev = None\n\n    while current.next != current:\n        # 找到第k个节点\n        for _ in range(k - 1):\n            prev = current\n            current = current.next\n        # 杀掉第k个节点\n        result.append(str(current.number))\n        prev.next = current.next\n        current = prev.next\n\n    # 最后剩下的一个人\n    #result.append(str(current.number))\n    #return ' '.join(result[:-1])  # 根据题意，只输出被杀掉的编号\n    return ' '.join(result)\n\n# 读取输入\nn, k = map(int, input().split())\n\n# 计算并输出结果\nprint(josephus_circle(n, k))\n"

def g5344(r):
    n = r.randint(3, 1000); return f"{n} {r.randint(2, n - 1)}\n"

def build_cases():
    return [SAMPLE_IN] + [g5344(random.Random(NUMBER + i)) for i in range(1, 20)]

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

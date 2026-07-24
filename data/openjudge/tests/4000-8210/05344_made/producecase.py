import random
import subprocess
import tempfile
from pathlib import Path
SAMPLE_IN = '10 2\n'
SAMPLE_OUT = '2 4 6 8 10 3 7 1 9\n'
CASES = ['10 2\n', '965 280\n', '552 175\n', '490 356\n', '456 346\n', '426 165\n', '752 351\n', '885 546\n', '752 432\n', '583 515\n', '612 257\n', '441 437\n', '963 740\n', '816 75\n', '194 43\n', '311 173\n', '34 17\n', '251 37\n', '56 36\n', '822 607\n']
REFERENCE_SOURCE = "class Node:\n    def __init__(self, number):\n        self.number = number\n        self.next = None\n\ndef josephus_circle(n, k):\n    # 创建循环链表\n    head = Node(1)\n    current = head\n    for i in range(2, n + 1):\n        new_node = Node(i)\n        current.next = new_node\n        current = new_node\n    current.next = head  # 形成环\n\n    result = []\n    current = head\n    prev = None\n\n    while current.next != current:\n        # 找到第k个节点\n        for _ in range(k - 1):\n            prev = current\n            current = current.next\n        # 杀掉第k个节点\n        result.append(str(current.number))\n        prev.next = current.next\n        current = prev.next\n\n    # 最后剩下的一个人\n    #result.append(str(current.number))\n    #return ' '.join(result[:-1])  # 根据题意，只输出被杀掉的编号\n    return ' '.join(result)\n\n# 读取输入\nn, k = map(int, input().split())\n\n# 计算并输出结果\nprint(josephus_circle(n, k))\n"
assert CASES[0] == SAMPLE_IN
random.seed(5344)
def solve_reference(content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        result = subprocess.run(["python3", handle.name], input=content, text=True,
                                capture_output=True, timeout=5, check=True)
    return result.stdout
assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split()
root = Path(__file__).parent / "data"
for index in range(20):
    content = CASES[index]
    (root / f"{index}.in").write_text(content, encoding="utf-8")
    (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")

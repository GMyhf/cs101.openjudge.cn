"""5343 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001b
生成器与循环取自 scripts/build_001b.py（批次 001b），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 5343
SAMPLE_IN = '8\nD8 A6 C3 B8 C5 A1 B5 D3\n'
SAMPLE_OUT = 'Queue1:A1\nQueue2:\nQueue3:C3 D3\nQueue4:\nQueue5:C5 B5\nQueue6:A6\nQueue7:\nQueue8:D8 B8\nQueue9:\nQueueA:A1 A6\nQueueB:B5 B8\nQueueC:C3 C5\nQueueD:D3 D8\nA1 A6 B5 B8 C3 C5 D3 D8\n'
REFERENCE_SOURCE = "from collections import deque\n\n\nn = int(input())\nqueues = [deque() for _ in range(9)]\ncards = deque(list(input().split()))\n\nwhile cards:\n    card = cards.popleft()\n    queues[int(card[1])-1].append(card)\n\nqs = {'A': deque(), 'B': deque(), 'C': deque(), 'D': deque()}\nfor i in range(9):\n    tmp = []\n    while queues[i]:\n        card = queues[i].popleft()\n        qs[card[0]].append(card)\n        tmp.append(card)\n    print(f'Queue{i+1}:'+' '.join(tmp))\n\nresult = []\nfor char in qs.keys():\n    tmp = []\n    while qs[char]:\n        card = qs[char].popleft()\n        result.append(card)\n        tmp.append(card)\n    print(f'Queue{char}:' + ' '.join(tmp))\nprint(*result)\n"

def g5343(r):
    cards = [s + str(v) for s in "ABCD" for v in range(1, 10)]
    values = r.sample(cards, r.randint(5, 30))
    return str(len(values)) + "\n" + " ".join(values) + "\n"

def build_cases():
    return [SAMPLE_IN] + [g5343(random.Random(NUMBER + i)) for i in range(1, 20)]

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

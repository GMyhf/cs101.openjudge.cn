"""4078 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001a
生成器与循环取自 scripts/build_001a.py（批次 001a），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 4078
SAMPLE_IN = '4\n1 5\n1 1\n1 7\n2\n'
SAMPLE_OUT = '1\n'
REFERENCE_SOURCE = "class BinaryHeap:\n    def __init__(self):\n        self._heap = []\n\n    def _perc_up(self, i):\n        while (i - 1) // 2 >= 0:\n            parent_idx = (i - 1) // 2\n            if self._heap[i] < self._heap[parent_idx]:\n                self._heap[i], self._heap[parent_idx] = (\n                    self._heap[parent_idx],\n                    self._heap[i],\n                )\n            i = parent_idx\n\n    def insert(self, item):\n        self._heap.append(item)\n        self._perc_up(len(self._heap) - 1)\n\n    def _perc_down(self, i):\n        while 2 * i + 1 < len(self._heap):\n            sm_child = self._get_min_child(i)\n            if self._heap[i] > self._heap[sm_child]:\n                self._heap[i], self._heap[sm_child] = (\n                    self._heap[sm_child],\n                    self._heap[i],\n                )\n            else:\n                break\n            i = sm_child\n\n    def _get_min_child(self, i):\n        if 2 * i + 2 > len(self._heap) - 1:\n            return 2 * i + 1\n        if self._heap[2 * i + 1] < self._heap[2 * i + 2]:\n            return 2 * i + 1\n        return 2 * i + 2\n\n    def delete(self):\n        self._heap[0], self._heap[-1] = self._heap[-1], self._heap[0]\n        result = self._heap.pop()\n        self._perc_down(0)\n        return result\n\n    def heapify(self, not_a_heap):\n        self._heap = not_a_heap[:]\n        i = len(self._heap) // 2 - 1    # 超过中点的节点都是叶子节点\n        while i >= 0:\n            #print(f'i = {i}, {self._heap}')\n            self._perc_down(i)\n            i = i - 1\n\n\n\nn = int(input().strip())\nbh = BinaryHeap()\nfor _ in range(n):\n    inp = input().strip()\n    if inp[0] == '1':\n        bh.insert(int(inp.split()[1]))\n    else:\n        print(bh.delete())\n"

def g4078(r):
    ops = []
    size = 0
    for _ in range(r.randint(10, 60)):
        if size == 0 or r.random() < .7:
            ops.append(f"1 {r.randint(-100, 100)}"); size += 1
        else:
            ops.append("2"); size -= 1
    return str(len(ops)) + "\n" + "\n".join(ops) + "\n"

def build_cases():
    return [SAMPLE_IN] + [g4078(random.Random(NUMBER + i)) for i in range(1, 20)]

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

"""4078 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 27 组数据。

2026-10 审计：原数据 n<=60，离题面 1<=n<=100000 太远，O(n^2) 的「每次线性找最小」写法也能过，
且没有 n=1、无删除操作、大量重复值、单调插入等边界。第 1..9 组保留原随机小组，其余换成
边界组与 n=100000 的满规模组（堆里同时留数万个元素，卡掉线性找最小）。

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

def valid(text):
    """题面：第一行 n（1<=n<=100000）；随后 n 次操作，每次一行：「1 u」（u 为整数）或「2」。
    题面未给 u 的范围，只核为整数；另核每次删除时数组非空（否则「输出并删除最小元素」无定义）。"""
    try:
        lines = text.split("\n")
        while lines and lines[-1].strip() == "":
            lines.pop()
        rows = [ln.split() for ln in lines]
        if not rows or len(rows[0]) != 1:
            return False
        n = int(rows[0][0])
        if not 1 <= n <= 100000 or len(rows) != n + 1:
            return False
        size = 0
        for row in rows[1:]:
            if row[:1] == ["1"] and len(row) == 2:
                int(row[1]); size += 1
            elif row == ["2"]:
                if size == 0:
                    return False
                size -= 1
            else:
                return False
        return True
    except ValueError:
        return False


def fmt(ops):
    return str(len(ops)) + "\n" + "\n".join(ops) + "\n"


def ops_random(r, n, p_ins, lo, hi):
    ops = []; size = 0
    for _ in range(n):
        if size == 0 or r.random() < p_ins:
            ops.append(f"1 {r.randint(lo, hi)}"); size += 1
        else:
            ops.append("2"); size -= 1
    return ops


def ops_fill_drain(vals):
    return [f"1 {v}" for v in vals] + ["2"] * len(vals)


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
    cases = [SAMPLE_IN] + [g4078(random.Random(NUMBER + i)) for i in range(1, 10)]
    r = random.Random(NUMBER * 13)
    cases.append(fmt(["1 42"]))                                    # n=1，无输出
    cases.append(fmt(["1 -7", "2"]))                               # n=2
    cases.append(fmt(["1 3", "1 3", "1 3", "2", "2", "1 1", "2", "2"]))   # 重复值
    cases.append(fmt([f"1 {v}" for v in range(10, 0, -1)] + ["2"] * 10))
    cases.append(fmt(["1 2147483647", "1 -2147483648", "1 0", "2", "2", "2"]))  # 32 位边界
    cases.append(fmt(ops_random(r, 1000, 0.5, -10 ** 9, 10 ** 9)))
    cases.append(fmt(ops_random(r, 5000, 0.6, 0, 3)))                # 大量重复
    # 满规模 n=100000（值控制在 6 位以内，保证 .in<=1MB）
    cases.append(fmt(ops_fill_drain([r.randint(0, 999999) for _ in range(50000)])))   # 堆里 5 万个
    cases.append(fmt(ops_fill_drain(list(range(99999, 49999, -1)))))                 # 递减插入
    cases.append(fmt(ops_fill_drain(list(range(50000)))))                            # 递增插入
    cases.append(fmt(ops_random(r, 100000, 0.7, -99999, 99999)))
    cases.append(fmt(ops_random(r, 100000, 0.55, 0, 999999)))
    cases.append(fmt([f"1 {r.randint(0, 999999)}" for _ in range(100000)]))         # 只插入，无输出
    cases.append(fmt([x for i in range(50000) for x in (f"1 {r.randint(0, 999999)}", "2")]))  # 交替
    cases.append(fmt(ops_fill_drain([r.randint(0, 9) for _ in range(50000)])))        # 满规模重复值
    ops = [f"1 {r.randint(0, 999999)}" for _ in range(60000)]
    ops += ops_random(r, 40000, 0.4, 0, 999999)
    cases.append(fmt(ops))                                            # 先填满再随机进出
    cases.append(fmt(ops_random(r, 60000, 0.6, -10 ** 9, 10 ** 9)))   # 大值域
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
    assert len(set(cases)) == len(cases), "组间不得重复"
    for i, c in enumerate(cases):
        assert valid(c), f"第 {i} 组越出题面约束"
        assert len(c.encode()) <= 1 << 20, f"第 {i} 组 .in 超过 1MB"
    assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split(), "参考解法跑不出样例输出"
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for index, content in enumerate(cases):
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")


if __name__ == "__main__":
    main()

"""4089 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001a
生成器与循环取自 scripts/build_001a.py（批次 001a），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 4089
SAMPLE_IN = '2\n3\n911\n97625999\n91125426\n5\n113\n12340\n123440\n12345\n98346\n'
SAMPLE_OUT = 'NO\nYES\n'
REFERENCE_SOURCE = 'class TrieNode:\n    def __init__(self):\n        self.children = {}\n        self.is_end_of_number = False\n\nclass Trie:\n    def __init__(self):\n        self.root = TrieNode()\n    \n    def insert(self, number):\n        node = self.root\n        for digit in number:\n            if digit not in node.children:\n                node.children[digit] = TrieNode()\n            node = node.children[digit]\n            # 如果当前节点已经是某个电话号码的结尾，则说明存在前缀冲突\n            if node.is_end_of_number:\n                return False\n        # 插入完成后，标记为完整电话号码\n        node.is_end_of_number = True\n        # 如果当前节点还有子节点，说明有其他号码以它为前缀\n        return len(node.children) == 0\n    \n    def is_consistent(self, numbers):\n        # 按长度从短到长排序，确保短号码先被检查\n        numbers.sort(key=len)\n        for number in numbers:\n            if not self.insert(number):\n                return False\n        return True\n\ndef main():\n    import sys\n    input = sys.stdin.read\n    data = input().splitlines()\n    \n    t = int(data[0])  # 测试样例数量\n    index = 1\n    results = []\n    \n    for _ in range(t):\n        n = int(data[index])  # 当前测试样例的电话号码数量\n        index += 1\n        numbers = data[index:index + n]\n        index += n\n        \n        trie = Trie()\n        if trie.is_consistent(numbers):\n            results.append("YES")\n        else:\n            results.append("NO")\n    \n    print("\\n".join(results))\n\n# 调用主函数\nif __name__ == "__main__":\n    main()\n'

def g4089(r):
    t = r.randint(2, 6); lines = [str(t)]
    for _ in range(t):
        nums = [str(r.randint(100, 999999)) for _ in range(r.randint(2, 12))]
        lines += [str(len(nums))] + nums
    return "\n".join(lines) + "\n"

def build_cases():
    return [SAMPLE_IN] + [g4089(random.Random(NUMBER + i)) for i in range(1, 20)]

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

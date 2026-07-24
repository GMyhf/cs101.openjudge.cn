import random
import subprocess
import tempfile
from pathlib import Path
SAMPLE_IN = '3\n'
SAMPLE_OUT = '5\n'
CASES = ['3\n', '2\n', '4\n', '8\n', '5\n', '3\n', '9\n', '12\n', '7\n', '2\n', '5\n', '1\n', '4\n', '9\n', '8\n', '10\n', '12\n', '5\n', '8\n', '11\n']
REFERENCE_SOURCE = 'def count_sequences(n):\n    def dfs(push_num, stack, popped):\n        nonlocal count\n        # 如果已经弹出了 n 个数，说明这个出栈序列是合法的\n        if popped == n:\n            count += 1\n            return\n        # 尝试进栈：如果还有数字没进栈\n        if push_num <= n:\n            stack.append(push_num)\n            dfs(push_num + 1, stack, popped)\n            stack.pop()\n        # 尝试出栈：如果栈不空\n        if stack:\n            top = stack.pop()\n            dfs(push_num, stack, popped + 1)\n            stack.append(top)\n\n    count = 0\n    dfs(1, [], 0)\n    return count\n\n# 读取输入\nn = int(input())\nprint(count_sequences(n))\n'
assert SAMPLE_IN.strip()
assert SAMPLE_OUT.strip()
random.seed(4077)
assert CASES[0] == SAMPLE_IN
def solve_reference(content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE)
        handle.flush()
        result = subprocess.run(["python3", handle.name], input=content, text=True,
                                capture_output=True, timeout=5, check=True)
    return result.stdout
assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split()
def generate_case(index):
    return CASES[index]
root = Path(__file__).parent / "data"
for index in range(20):
    content = generate_case(index)
    (root / f"{index}.in").write_text(content, encoding="utf-8")
    (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")

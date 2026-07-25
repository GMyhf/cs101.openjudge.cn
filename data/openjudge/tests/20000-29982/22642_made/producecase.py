import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = "# 23n2300011072(蒋子轩)\ndef add(n, left, right, string):\n    # 终止条件：如果已经放置了所有的括号\n    if left == n and right == n:\n        print(string)\n        return\n\n    # 如果我们仍然可以放置左括号，则添加左括号\n    if left < n:\n        add(n, left+1, right, string+'(')\n\n    # 如果右括号数量小于左括号数量，则添加右括号\n    if right < left:\n        add(n, left, right+1, string+')')\n\nn = int(input())\nadd(n, 0, 0, '')\n"
SAMPLE_IN = '3\n'
SAMPLE_OUT = '((()))\n(()())\n(())()\n()(())\n()()()\n'
def generate_case(r): return str(r.randint(1, 10)) + "\n"

assert SAMPLE_IN == '3\n'
with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(10):
        if index == 0:
            content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(22642 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError('insufficient diversity')
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

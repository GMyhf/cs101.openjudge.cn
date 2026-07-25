import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = "def min_employees(tasks, t):\n    left, right = 1, max(tasks)\n    while left < right:\n        mid = (left + right) // 2\n        total_hours = sum((task + mid - 1) // mid for task in tasks)\n        if total_hours > t:\n            left = mid + 1\n        else:\n            right = mid\n    return left\n\n# 读取输入并处理\ntasks = list(map(int, input().split(',')))\nt = int(input())\nprint(min_employees(tasks, t))\n"
SAMPLE_IN = '1,2,5,9\n5\n'
SAMPLE_OUT = '5\n'
def generate_case(r):
    a = [r.randint(1, 50) for _ in range(r.randint(2, 20))]; return ",".join(map(str, a)) + "\n" + str(r.randint(max(a), sum(a))) + "\n"

assert SAMPLE_IN == '1,2,5,9\n5\n'
with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0:
            content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(20746 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError('insufficient diversity')
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

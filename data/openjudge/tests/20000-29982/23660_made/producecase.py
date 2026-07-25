import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'def count_combinations(numbers, index, current_sum, count):\n    if index >= len(numbers):\n        if current_sum % 7 == 0:\n            return count + 1\n        else:\n            return count\n    \n    # 选择取当前位置的数\n    count = count_combinations(numbers, index + 1, current_sum + numbers[index], count)\n    \n    # 选择不取当前位置的数\n    count = count_combinations(numbers, index + 1, current_sum, count)\n    \n    return count\n\n\n# 主程序\nt = int(input())\nfor _ in range(t):\n    data = list(map(int, input().split()))\n    n = data[0]\n    numbers = data[1:]\n    \n    result = count_combinations(numbers, 0, 0, 0)\n    print(result)\n'
SAMPLE_IN = '3\n3 1 2 4\n5 1 2 3 4 5\n12 1 2 3 4 5 6 7 8 9 10 11 12\n'
SAMPLE_OUT = '2\n5\n586\n'
def generate_case(r):
    rows = []
    for _ in range(r.randint(2, 5)):
        n = r.randint(1, 15)
        values = r.sample(range(1, 100), n)
        rows.append(f"{n} " + " ".join(map(str, values)))
    return str(len(rows)) + "\n" + "\n".join(rows) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0:
            content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(23660 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

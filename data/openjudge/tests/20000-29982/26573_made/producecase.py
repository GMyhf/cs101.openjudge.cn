import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = "def print_cantor_set(n):\n    def cantor(start, end, level):\n        if level == 0:\n            for i in range(start, end):\n                cantor_set[i] = '*'  # Mark the segment as occupied\n        else:\n            segment_length = (end - start) // 3\n            # Recursively mark the first third and the last third\n            cantor(start, start + segment_length, level - 1)\n            cantor(end - segment_length, end, level - 1)\n\n    # Initialize the list with dashes, representing an empty line\n    cantor_set = ['-' for _ in range(3 ** n)]\n    cantor(0, 3 ** n, n)\n    return ''.join(cantor_set)\n\n# Read the input\nn = int(input())\n\n# Generate and print the Cantor set\nprint(print_cantor_set(n))\n"
SAMPLE_IN = '3\n'
SAMPLE_OUT = '*-*---*-*---------*-*---*-*\n'
def generate_case(r):
    n = r.randint(0, 8); width = 3 ** n; assert width == 3 ** n
    return str(n) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(9):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(26573 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

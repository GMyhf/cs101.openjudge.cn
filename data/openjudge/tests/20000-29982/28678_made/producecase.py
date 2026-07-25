import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'def collatz_sequence(n):\n    if n == 1:\n        print("End")\n        return\n\n    while n != 1:\n        if n % 2 == 1:\n            next_n = 3 * n + 1\n            print(f"{n}*3+1={next_n}")\n        else:\n            next_n = n // 2\n            print(f"{n}/2={next_n}")\n        n = next_n\n\n    print("End")\n\n# Sample input\nn = int(input())\n\n# Calculate and print the result\ncollatz_sequence(n)\n'
SAMPLE_IN = '5\n'
SAMPLE_OUT = '5*3+1=16\n16/2=8\n8/2=4\n4/2=2\n2/2=1\nEnd\n'
def generate_case(r):
    return f"{r.randint(1, 1000)}\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(28678 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

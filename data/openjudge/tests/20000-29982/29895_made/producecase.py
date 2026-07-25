import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'import math\n\nn = int(input())\nfor i in range(2, int(math.isqrt(n)) + 1):\n    if n % i == 0:\n        print(n // i)\n        break\n'
SAMPLE_IN = '21\n'
def generate_case(r):
    a = r.randint(2, 100000); b = r.randint(2, 100000)
    return f"{a * b}\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(21):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(29895 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

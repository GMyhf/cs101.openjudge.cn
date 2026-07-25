import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'import math\nt = int(input())\nfor _ in range(t):\n    n = int(input())\n    if n % 2 == 1:\n        sumv = (1 + n - 1)*(n-1)//2 + n\n    else:\n        sumv = (1 + n)*n//2\n    \n    maxp = int(math.log2(n))\n    \n    for i in range(maxp+1):\n        sumv -= 2*(2**i)\n    \n    print(sumv)\n'
SAMPLE_IN = '2\n4\n18864\n'
SAMPLE_OUT = '-4\n177869146\n'
def generate_case(r):
    values = [r.randint(1, 10**6) for _ in range(r.randint(2, 12))]
    return str(len(values)) + "\n" + "\n".join(map(str, values)) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(27273 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

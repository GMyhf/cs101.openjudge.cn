import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'import math\ns = input()\n\nslen = len(s)\nmaxp = int(math.log2(slen))\n\nextracted = ""\nfor i in range(maxp+1):\n    extracted += s[2**i - 1]\n\nleft, right = 0, len(extracted)-1\nns = ""\nwhile left < right:\n    ns = ns + extracted[left] + extracted[right]\n    left += 1\n    right -= 1\n\nif len(extracted) % 2 != 0:\n    ns += extracted[right]\nprint(ns)\n'
SAMPLE_IN = '01a2bcd3efghijk4lmnopqrst\n'
SAMPLE_OUT = '04132\n'
def generate_case(r):
    k = r.randint(3, 7); length = 2 ** k + r.randint(0, 20)
    value = "".join(r.choice("0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(length))
    assert len(value) >= 2 ** k
    return value + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(27274 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

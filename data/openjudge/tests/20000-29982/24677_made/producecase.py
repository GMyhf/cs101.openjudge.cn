import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = '"""\nGitHub Copilot Chat:\nThis solution works by recursively splitting the string into four parts and \nchecking if each part is a valid coordinate. \nThe safe_locations function takes the remaining string, the current parts, \nand the current depth as arguments. \nIf the depth is 4, it checks if the string is empty and if all parts are \nvalid coordinates. If so, it returns 1, otherwise it returns 0. \nIf the depth is less than 4, it tries to split the string at every possible \nposition and recursively calls itself with the new parts and increased depth. \n"""\n\n\ndef safe_locations(s, parts, depth=0):\n    if depth == 4:\n        if not s and all(0 <= int(part) <= 500 and \n                (part == \'0\' or not part.startswith(\'0\')) for part in parts):\n            return 1\n        return 0\n    return sum(safe_locations(s[i:], parts + [s[:i]], depth + 1) \n               for i in range(1, len(s) + 1))\n\n\ns = input().strip()\nprint(safe_locations(s, []))\n\n'
SAMPLE_IN = '010010\n'
def generate_case(r):
    if r.random() < .65:
        parts = [str(r.randint(0, 500)) for _ in range(4)]
        value = "".join(parts)
    else:
        value = "".join(r.choice("0123456789") for _ in range(r.randint(1, 24)))
    assert len(value) <= 30 and value.isdigit()
    return value + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(21):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(24677 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

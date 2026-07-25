import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = "from collections import defaultdict\nfrom itertools import permutations\n\na = defaultdict(int)\nb = defaultdict(int)\nc = defaultdict(int)\nd = defaultdict(int)\nn = int(input())\n\nfor i in input():\n    a[i] += 1\nfor i in input():\n    b[i] += 1\nfor i in input():\n    c[i] += 1\nfor i in input():\n    d[i] += 1\n\ndicts = [a, b, c, d]\n\ndef check(word):\n    for perm in permutations(dicts, len(word)):\n        for i, d in enumerate(perm):\n            if word[i] not in d:\n                break\n        else:\n            return 'YES'\n    else:\n        return 'NO'\n\nfor _ in range(n):\n    word = input()\n    print(check(word))\n"
SAMPLE_IN = '6\nMOOOOO\nOOOOOO\nABCDEF\nUVWXYZ\nCOW\nMOO\nZOO\nMOVE\nCODE\nFARM\n'
def generate_case(r):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; blocks = []
    for _ in range(4): blocks.append("".join(r.choice(alphabet) for _ in range(6)))
    words = []
    for _ in range(r.randint(4, 10)):
        if r.random() < .55:
            chosen = r.sample(range(4), r.randint(1, 4)); word = "".join(r.choice(blocks[i]) for i in chosen)
        else:
            word = "".join(r.choice(alphabet) for _ in range(r.randint(1, 4)))
        words.append(word)
    assert all(1 <= len(w) <= 4 and w.isupper() for w in words)
    return str(len(words)) + "\n" + "\n".join(blocks + words) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(21):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(27310 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

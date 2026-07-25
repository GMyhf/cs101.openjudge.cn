import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'from collections import deque\n\nM, N = map(int, input().split())\nwords = list(map(int, input().split()))\n\nmemory = deque()\nlookups = 0\n\nfor word in words:\n    if word not in memory:\n        if len(memory) == M:\n            memory.popleft()\n        memory.append(word)\n        lookups += 1\n\nprint(lookups)\n'
SAMPLE_IN = '3 7\n1 2 1 5 4 4 1\n'
def generate_case(r):
    m = r.randint(1, 10); n = r.randint(1, 60); words = [r.randint(0, 30) for _ in range(n)]
    assert 1 <= m <= 100 and len(words) == n and all(0 <= x <= 1000 for x in words)
    return f"{m} {n}\n" + " ".join(map(str, words)) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(21):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(27951 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

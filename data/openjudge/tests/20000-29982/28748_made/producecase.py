import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'import sys\n\ndef solve():\n    data = sys.stdin.read().split()\n    if not data: return\n    it = iter(data)\n    n, k = int(next(it)), int(next(it))\n    \n    counts = {}\n    last_owner = {}\n    for p_idx in range(n):\n        for _ in range(k):\n            val = int(next(it))\n            counts[val] = counts.get(val, 0) + 1\n            last_owner[val] = p_idx # 覆盖更新，由于 p_idx 递增，最后存的是最大编号\n\n    prob_weights = [0] * n\n    for val, c in counts.items():\n        prob_weights[last_owner[val]] += c\n        \n    total = n * k\n    for w in prob_weights:\n        print(f"{w/total:.9f}")\n\nsolve()\n'
SAMPLE_IN = '3 4\n1 2 3 4\n1 2 5 6\n3 4 7 8\n'
SAMPLE_OUT = '0.000000000\n0.500000000\n0.500000000\n'
def generate_case(r):
    n = r.randint(2, 6); k = r.randint(2, 6); boards = [[r.randint(1, 20) for _ in range(k)] for _ in range(n)]
    return f"{n} {k}\n" + "\n".join(" ".join(map(str, row)) for row in boards) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(28748 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

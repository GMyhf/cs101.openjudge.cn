import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'from functools import lru_cache\n\ndef count_partitions(n, k):\n    @lru_cache(maxsize=None)\n    def dfs(n, k, start):\n        if k == 1:\n            return 1 if n >= start else 0\n\n        count = 0\n        for i in range(start, n + 1):\n            count += dfs(n - i, k - 1, i)\n        return count\n    return dfs(n, k, 1)\n\nn, k = map(int, input().split())\nprint(count_partitions(n, k))\n'
SAMPLE_IN = '7 3\n'
def generate_case(r):
    n = r.randint(7, 60); k = r.randint(2, min(6, n))
    assert n > 6 and 2 <= k <= 6
    return f"{n} {k}\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(21):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(28906 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

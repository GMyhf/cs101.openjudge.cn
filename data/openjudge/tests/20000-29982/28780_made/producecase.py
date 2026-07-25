import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'from math import inf\nn, m = map(int, input().split())\ncoins = list(map(int, input().split()))\ndp = [0] + [inf for _ in range(m)]\nfor i in range(n):\n    for j in range(coins[i], m + 1):\n        dp[j] = min(dp[j], dp[j - coins[i]] + 1)\nprint(dp[m] if dp[m] != inf else -1)\n'
SAMPLE_IN = '3 11\n1 2 4\n'
SAMPLE_OUT = '4\n'
def generate_case(r):
    coins = sorted(set(r.randint(1, 30) for _ in range(r.randint(2, 6))))
    amount = r.randint(1, 100)
    return f"{len(coins)} {amount}\n" + " ".join(map(str, coins)) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(28780 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'def count_ways(N):\n    if N == 1:\n        return 1\n    dp = [0] * (N + 1)\n    dp[0] = 1  # Base case: 1 way to stay at the ground (0 steps)\n    \n    for i in range(1, N + 1):\n        for j in range(1, i + 1):\n            dp[i] += dp[i - j]\n    \n    return dp[N]\n\nif __name__ == "__main__":\n    import sys\n    input = sys.stdin.read\n    N = int(input().strip())\n    print(count_ways(N))\n'
SAMPLE_IN = '3\n'
SAMPLE_OUT = '4\n'
def generate_case(r):
    n = r.randint(1, 25); return f"{n}\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(27528 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

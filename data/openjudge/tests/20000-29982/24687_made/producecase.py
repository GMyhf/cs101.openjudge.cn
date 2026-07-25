import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = "def min_population_flow(n, m, populations):\n    # Initialize the prefix sum array for fast range sum computation\n    prefix_sum = [0] * (n + 1)\n    for i in range(1, n + 1):\n        prefix_sum[i] = prefix_sum[i - 1] + populations[i - 1]\n    \n    # Initialize the DP table\n    dp = [[float('inf')] * (m + 1) for _ in range(n + 1)]\n    \n    # Base case: with 0 control points, the flow index is just the sum of all populations times their district count\n    for i in range(1, n + 1):\n        dp[i][0] = prefix_sum[i] * i\n    \n    # Fill the DP table\n    for i in range(1, n + 1):\n        for j in range(1, min(i, m) + 1):\n            for k in range(j-1, i):\n                dp[i][j] = min(dp[i][j], dp[k][j-1] + (prefix_sum[i] - prefix_sum[k]) * (i - k))\n    \n    # The answer is the minimum flow index after setting up m control points\n    return dp[n][m]\n\n# Input\nn, m = map(int, input().split())\npopulations = list(map(int, input().split()))\n\n# Output\nprint(min_population_flow(n, m, populations))\n"
SAMPLE_IN = '5 1\n10 50 20 30 40\n'
SAMPLE_OUT = '380\n'
def generate_case(r):
    n = r.randint(2, 30); m = r.randint(1, n - 1); population = [r.randint(1, 1000) for _ in range(n)]
    assert 0 < m < n and all(0 < x <= 1000 for x in population)
    return f"{n} {m}\n" + " ".join(map(str, population)) + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0:
            content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(24687 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'def min_operations(s):\n    n = len(s)\n    dp = [[0]*n for _ in range(n)]\n    for i in range(n-1, -1, -1):\n        for j in range(i+1, n):\n            if s[i] == s[j]:\n                dp[i][j] = dp[i+1][j-1]\n            else:\n                dp[i][j] = min(dp[i+1][j], dp[i][j-1], dp[i+1][j-1]) + 1\n    return dp[0][n-1]\n\ns = input().strip()\nprint(min_operations(s))\n'
SAMPLE_IN = 'ABAD\n'
SAMPLE_OUT = '1\n'
def generate_case(r):
    value = "".join(r.choice("ABCD") for _ in range(r.randint(1, 80)))
    assert 1 <= len(value) <= 100 and value.isupper()
    return value + "\n"

with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0: content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(25815 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError("insufficient diversity")
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

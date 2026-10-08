import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = "def min_population_flow(n, m, populations):\n    # Initialize the prefix sum array for fast range sum computation\n    prefix_sum = [0] * (n + 1)\n    for i in range(1, n + 1):\n        prefix_sum[i] = prefix_sum[i - 1] + populations[i - 1]\n    \n    # Initialize the DP table\n    dp = [[float('inf')] * (m + 1) for _ in range(n + 1)]\n    \n    # Base case: with 0 control points, the flow index is just the sum of all populations times their district count\n    for i in range(1, n + 1):\n        dp[i][0] = prefix_sum[i] * i\n    \n    # Fill the DP table\n    for i in range(1, n + 1):\n        for j in range(1, min(i, m) + 1):\n            for k in range(j-1, i):\n                dp[i][j] = min(dp[i][j], dp[k][j-1] + (prefix_sum[i] - prefix_sum[k]) * (i - k))\n    \n    # The answer is the minimum flow index after setting up m control points\n    return dp[n][m]\n\n# Input\nn, m = map(int, input().split())\npopulations = list(map(int, input().split()))\n\n# Output\nprint(min_population_flow(n, m, populations))\n"
SAMPLE_IN = '5 1\n10 50 20 30 40\n'
SAMPLE_OUT = '380\n'
def generate_case(r):
    n = r.randint(2, 30); m = r.randint(1, n - 1); population = [r.randint(1, 1000) for _ in range(n)]
    assert 0 < m < n and all(0 < x <= 1000 for x in population)
    return f"{n} {m}\n" + " ".join(map(str, population)) + "\n"


def valid(text):
    """题面：第一行两个正整数 n, m（n<=100，m<n）；第二行 n 个数 ai（ai<=1000），空格分隔。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if len(lines) != 2:
        return False
    head = lines[0].split(" ")
    if len(head) != 2 or not all(t.isdigit() for t in head):
        return False
    n, m = map(int, head)
    if not (1 <= m < n <= 100):
        return False
    vals = lines[1].split(" ")
    if len(vals) != n or not all(t.isdigit() for t in vals):
        return False
    a = list(map(int, vals))
    # 输出为“正整数”，故人数非负且不全为 0；本数据只用 1..1000
    return all(0 <= x <= 1000 for x in a) and sum(a) > 0


def extra_cases():
    """补充规模与边界：n=100 满规模、m=1 / m=n-1、最小 n=2、全 1000、单峰与单调序列。"""
    r = random.Random(246870)
    cases = []
    def fmt(n, m, a):
        return f"{n} {m}\n" + " ".join(map(str, a)) + "\n"
    cases.append(fmt(2, 1, [1, 1000]))
    cases.append(fmt(100, 1, [r.randint(1, 1000) for _ in range(100)]))
    cases.append(fmt(100, 99, [r.randint(1, 1000) for _ in range(100)]))
    cases.append(fmt(100, 50, [1000] * 100))
    cases.append(fmt(100, 37, [r.randint(1, 1000) for _ in range(100)]))
    cases.append(fmt(100, 9, list(range(1000, 900, -1))))
    cases.append(fmt(100, 20, [1] * 45 + [1000] * 10 + [1] * 45))
    cases.append(fmt(100, 3, [r.choice([1, 1000]) for _ in range(100)]))
    cases.append(fmt(99, 70, [r.randint(1, 1000) for _ in range(99)]))
    cases.append(fmt(3, 1, [1000, 1, 1000]))
    return cases


def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        extras = extra_cases()
        for index in range(20 + len(extras)):
            if index == 0:
                content = SAMPLE_IN
            elif index >= 20:
                content = extras[index - 20]
                if content in seen: raise AssertionError("duplicate extra case")
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(24687 + index + attempt * 1000))
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()

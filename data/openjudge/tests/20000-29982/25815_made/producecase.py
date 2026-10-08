import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'def min_operations(s):\n    n = len(s)\n    dp = [[0]*n for _ in range(n)]\n    for i in range(n-1, -1, -1):\n        for j in range(i+1, n):\n            if s[i] == s[j]:\n                dp[i][j] = dp[i+1][j-1]\n            else:\n                dp[i][j] = min(dp[i+1][j], dp[i][j-1], dp[i+1][j-1]) + 1\n    return dp[0][n-1]\n\ns = input().strip()\nprint(min_operations(s))\n'
SAMPLE_IN = 'ABAD\n'
SAMPLE_OUT = '1\n'
def valid(text):
    """题面：字符串 S，长度不超过 100，只包含 'A'-'Z'（单行）。"""
    if not text.endswith("\n"): return False
    body = text[:-1]
    return 1 <= len(body) <= 100 and all("A" <= ch <= "Z" for ch in body)

def extra_cases():
    """补边界与满规模：长度 1/2、本身回文（答案 0）、长度 100、全字母表。"""
    r = random.Random(258150)
    A = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    half = "".join(r.choice(A) for _ in range(50))
    out = ["A\n", "AB\n", "AA\n", "ZZZZZ\n", half + half[::-1] + "\n", "ABCDEFGHIJKLMNOPQRSTUVWXYZ\n",
           "".join(r.choice(A) for _ in range(100)) + "\n", "".join(r.choice(A) for _ in range(100)) + "\n",
           "".join(r.choice("AB") for _ in range(100)) + "\n", "".join(r.choice("ABCD") for _ in range(100)) + "\n",
           ("ABCDEFGHIJKLMNOPQRSTUVWXY" * 4) + "\n", "A" * 99 + "B\n", "".join(r.choice(A) for _ in range(99)) + "\n"]
    # 几乎回文：改动少数位置
    t = list(half + half[::-1])
    for k in r.sample(range(100), 3): t[k] = r.choice(A)
    out.append("".join(t) + "\n")
    for _ in range(6):
        out.append("".join(r.choice("ABC") for _ in range(r.randint(3, 7))) + "\n")
    return out

def generate_case(r):
    value = "".join(r.choice("ABCD") for _ in range(r.randint(1, 80)))
    assert 1 <= len(value) <= 100 and value.isupper()
    return value + "\n"

def main():
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
        index = 19
        for content in extra_cases():
            if content in seen: continue  # 短随机串可能与前面重复，跳过
            index += 1
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
        for index in range(len(seen) - 1):
            assert valid((root / f"{index}.in").read_text(encoding="utf-8")), index

if __name__ == "__main__":
    main()

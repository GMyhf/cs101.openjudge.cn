import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'def collatz_sequence(n):\n    if n == 1:\n        print("End")\n        return\n\n    while n != 1:\n        if n % 2 == 1:\n            next_n = 3 * n + 1\n            print(f"{n}*3+1={next_n}")\n        else:\n            next_n = n // 2\n            print(f"{n}/2={next_n}")\n        n = next_n\n\n    print("End")\n\n# Sample input\nn = int(input())\n\n# Calculate and print the result\ncollatz_sequence(n)\n'
SAMPLE_IN = '5\n'
SAMPLE_OUT = '5*3+1=16\n16/2=8\n8/2=4\n4/2=2\n2/2=1\nEnd\n'
def valid(text):
    """题面：一个正整数 n (n <= 2,000,000)。"""
    if not isinstance(text, str) or not text.endswith("\n"):
        return False
    body = text[:-1]
    if not body.isdigit() or body[0] == "0":
        return False
    return 1 <= int(body) <= 2000000

# 固定的边界/卡点组：1 直接 End；2^20 全是除法；113383 中间值首次超 2^31；
# 704511 峰值约 5.7e10；1988859 是 2e6 内峰值最高者（约 1.57e11，超 2^32）；
# 1723519 是 2e6 内步数最多者（556 步）；2000000 为上限。
FIXED = {1: 1, 2: 2, 3: 3, 4: 27, 5: 2000000, 6: 1723519, 7: 1988859, 8: 704511,
         9: 113383, 10: 1048576, 11: 1999999, 12: 837799}

def generate_case(r, index):
    if index in FIXED:
        return f"{FIXED[index]}\n"
    hi = 1000 if index < 15 else 2000000
    return f"{r.randint(1, hi)}\n"

def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        for index in range(20):
            if index == 0: content = SAMPLE_IN
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(28678 + index + attempt * 1000), index)
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
            assert valid(content), index
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

if __name__ == "__main__":
    main()

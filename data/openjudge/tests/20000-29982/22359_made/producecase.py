import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'def is_prime(n):\n    if n < 2:\n        return False\n    for i in range(2, int(n**0.5) + 1):\n        if n % i == 0:\n            return False\n    return True\n\ndef goldbach(n):\n    for i in range(2, n):\n        if is_prime(i) and is_prime(n - i):\n            return i, n - i\n\nn = int(input())\na, b = goldbach(n)\nprint(a, b)\n'
SAMPLE_IN = '10\n'
SAMPLE_OUT = '3 7\n'
def generate_case(r):
    def is_prime(x):
        return x >= 2 and all(x % d for d in range(2, int(x ** 0.5) + 1))

    if r.random() < .3:
        while True:                                   # 奇数和：拒绝采样保证 sum-2 是素数
            value = r.randrange(5, 10001, 2)
            if is_prime(value - 2): break
    else:
        value = r.randrange(4, 10001, 2)              # 偶数和：下界改到 4，排除无解的 2
    assert value >= 4 and (value % 2 == 0 or is_prime(value - 2))
    return str(value) + "\n"

def valid(text):
    """题面：一个正整数（<= 10000），且是两个素数 A、B 之和。"""
    if not text.endswith("\n") or text.count("\n") != 1:
        return False
    s = text[:-1]
    if not s.isdigit() or s != str(int(s)):
        return False
    n = int(s)
    if not 1 <= n <= 10000:
        return False
    def is_prime(x):
        return x >= 2 and all(x % d for d in range(2, int(x ** 0.5) + 1))
    return any(is_prime(i) and is_prime(n - i) for i in range(2, n - 1))

# 边界补充：最小和 4(2+2)、5(2+3)、6(3+3)、7、9，上限 10000、9998，
# 以及 10000 以内最小素数分量最大的 7426(173+7253)，卡只试小素数的写法
EXTRA = [4, 5, 6, 7, 9, 10000, 9998, 7426]

def main():
    assert SAMPLE_IN == '10\n'
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        cases = []
        for index in range(20):
            if index == 0:
                content = SAMPLE_IN
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(22359 + index + attempt * 1000))
                    if content not in seen: break
                else: raise AssertionError('insufficient diversity')
            seen.append(content)
            cases.append(content)
        for v in EXTRA:
            content = f"{v}\n"
            assert content not in cases
            cases.append(content)
        for index, content in enumerate(cases):
            assert valid(content), index
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

if __name__ == "__main__":
    main()

import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'import math\n\nn = int(input())\nfor i in range(2, int(math.isqrt(n)) + 1):\n    if n % i == 0:\n        print(n // i)\n        break\n'
SAMPLE_IN = '21\n'
def generate_case(r):
    a = r.randint(2, 100000); b = r.randint(2, 100000)
    return f"{a * b}\n"

import math


def _is_prime(x):
    return x >= 2 and all(x % d for d in range(2, math.isqrt(x) + 1))


def valid(text):
    """题面契约：一行一个正整数 n，1 <= n <= 10^10；n 是合数，且能写成两个不同因数
    （均不为 1 和自身）的乘积 —— 即排除质数与质数的平方（p*p 两因数相同）。"""
    if not text.endswith("\n") or text.count("\n") != 1:
        return False
    s = text[:-1]
    if not s.isdigit() or s != str(int(s)):
        return False
    n = int(s)
    if not 1 <= n <= 10 ** 10:
        return False
    d = next((d for d in range(2, math.isqrt(n) + 1) if n % d == 0), None)
    if d is None:
        return False                      # 1 或质数
    r = math.isqrt(n)
    return not (r * r == n and _is_prime(r))


# 追加组：最小质因子很大的半素数（逼近 10^10，要求试除到 √n 级别）、上界 10^10、
# 超过 2^31/2^32 的奇数、质数立方、最小规模 6 和 8、两个大质数里含 2 的组。
EXTRA_CASES = [f"{v}\n" for v in (
    99991 * 99989,          # 9998000099，最小质因子 99989
    99971 * 100003,         # 最小质因子 99971，n 接近 10^10
    10 ** 10,
    6, 8,
    2153 ** 3,              # 2153 为质数，n = p^3
    3 * 3333333323,         # 3333333323 为质数
    2 * 4999999937,         # 4999999937 为质数
    65537 * 65539,          # 跨过 2^32
    46337 * 46349,          # 跨过 2^31
    97 * 101 * 103 * 107,   # 非半素数：答案是 n/97 而不是最大质因子
)]


def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        cases = list(range(40)) + EXTRA_CASES
        for index, extra in enumerate(cases):
            if index == 0: content = SAMPLE_IN
            elif index >= 40: content = extra
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(29895 + index + attempt * 1000))
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
            assert valid(content), content
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()

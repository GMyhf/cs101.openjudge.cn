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

assert SAMPLE_IN == '10\n'
with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0:
            content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(22359 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError('insufficient diversity')
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

import random,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\ns=sys.stdin.read().strip()\nsign="-" if s.startswith("-") else ""\ndigits=s[1:] if sign else s\nprint(sign + digits[::-1].lstrip("0") or "0")'
SAMPLE_IN='123\n'
import re


def valid(text):
    """题面契约：一行一个整数 N，-1,000,000,000 <= N <= 1,000,000,000（常规写法，无前导零）。"""
    if not text.endswith("\n") or text.count("\n") != 1:
        return False
    s = text[:-1]
    if not re.fullmatch(r"-?(0|[1-9][0-9]*)", s) or s == "-0":
        return False
    return -10 ** 9 <= int(s) <= 10 ** 9


# 手写边界：0、正负一位数、末尾带零（样例 2）、上下界、回文、反转后很多前导零等
FIXED = [
    "-380", "0", "1", "-1", "9", "-9", "10", "-10", "100", "-120",
    "1000000000", "-1000000000", "999999999", "-999999999", "-1000000",
    "123454321", "-900000000", "500000", "-102030400", "1999999999"[:9],
]


def gen(i, attempt=0):
    if i == 0:
        return SAMPLE_IN
    if i <= len(FIXED):
        return FIXED[i - 1] + "\n"
    r = random.Random(4029 * 1000 + i + attempt * 100)
    kind = i % 3
    if kind == 0:
        value = r.randint(-10 ** 9, 10 ** 9)
    elif kind == 1:      # 末尾若干个零
        value = r.randint(1, 10 ** r.randint(1, 8)) * 10 ** r.randint(1, 3)
        value = min(value, 10 ** 9)
        if r.random() < 0.5:
            value = -value
    else:                # 各种位数
        d = r.randint(1, 9)
        value = r.randint(10 ** (d - 1), 10 ** d - 1) * r.choice([1, -1])
    return f"{value}\n"


def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE)
        handle.flush()
        root = Path(__file__).parent / "data"
        seen = set()
        for index in range(40):
            content = gen(index)
            attempt = 0
            while content in seen:  # 极小值域下可能撞重，换种子重抽
                attempt += 1
                content = gen(index, attempt)
            assert valid(content) and content not in seen, index
            seen.add(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True,
                                    capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()

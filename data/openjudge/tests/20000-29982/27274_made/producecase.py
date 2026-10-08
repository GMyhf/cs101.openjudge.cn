import random, re, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'import math\ns = input()\n\nslen = len(s)\nmaxp = int(math.log2(slen))\n\nextracted = ""\nfor i in range(maxp+1):\n    extracted += s[2**i - 1]\n\nleft, right = 0, len(extracted)-1\nns = ""\nwhile left < right:\n    ns = ns + extracted[left] + extracted[right]\n    left += 1\n    right -= 1\n\nif len(extracted) % 2 != 0:\n    ns += extracted[right]\nprint(ns)\n'
SAMPLE_IN = '01a2bcd3efghijk4lmnopqrst\n'
SAMPLE_OUT = '04132\n'
ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def valid(text):
    """题面：一行字符串 s，由 ASCII 数字和大小写字母组成，0 < len(s) < 10^5。"""
    if not text.endswith("\n") or text.count("\n") != 1:
        return False
    s = text[:-1]
    return 0 < len(s) < 10**5 and re.fullmatch(r"[0-9A-Za-z]+", s) is not None


FIXED_LENGTHS = {1: 1, 2: 2, 3: 3, 4: 4, 5: 7, 6: 8, 7: 15, 8: 16, 9: 1023, 10: 1024,
                 11: 65535, 12: 65536, 13: 65537, 14: 99999, 15: 99998, 16: 32768}


def generate_case(r, index):
    if index in FIXED_LENGTHS:
        length = FIXED_LENGTHS[index]
    elif index <= 18:
        k = r.randint(3, 7); length = 2 ** k + r.randint(0, 20)
    else:
        length = r.randint(50000, 99999)
    value = "".join(r.choice(ALPHABET) for _ in range(length))
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
                    content = generate_case(random.Random(27274 + index + attempt * 1000), index)
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
            assert valid(content)
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            if index == 0: assert result.stdout == SAMPLE_OUT
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()

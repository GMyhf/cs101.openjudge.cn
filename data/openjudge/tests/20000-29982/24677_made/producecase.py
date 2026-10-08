import random, subprocess, sys, tempfile
from pathlib import Path
REFERENCE_SOURCE = '"""\nGitHub Copilot Chat:\nThis solution works by recursively splitting the string into four parts and \nchecking if each part is a valid coordinate. \nThe safe_locations function takes the remaining string, the current parts, \nand the current depth as arguments. \nIf the depth is 4, it checks if the string is empty and if all parts are \nvalid coordinates. If so, it returns 1, otherwise it returns 0. \nIf the depth is less than 4, it tries to split the string at every possible \nposition and recursively calls itself with the new parts and increased depth. \n"""\n\n\ndef safe_locations(s, parts, depth=0):\n    if depth == 4:\n        if not s and all(0 <= int(part) <= 500 and \n                (part == \'0\' or not part.startswith(\'0\')) for part in parts):\n            return 1\n        return 0\n    return sum(safe_locations(s[i:], parts + [s[:i]], depth + 1) \n               for i in range(1, len(s) + 1))\n\n\ns = input().strip()\nprint(safe_locations(s, []))\n\n'
SAMPLE_IN = '010010\n'


def valid(text):
    """题面：输入只有一行，是一个字符串 S，0<=len(S)<=30。S 要切成四个坐标（数），故只能由数字 0-9 组成。"""
    if not text.endswith("\n") or text.count("\n") != 1:
        return False
    s = text[:-1]
    return len(s) <= 30 and all(c in "0123456789" for c in s)


def old_case(r):
    if r.random() < .65:
        parts = [str(r.randint(0, 500)) for _ in range(4)]
        value = "".join(parts)
    else:
        value = "".join(r.choice("0123456789") for _ in range(r.randint(1, 24)))
    return value + "\n"


SPECIAL = [
    "",                     # 空串
    "0", "000", "0000",     # 长度不足 4 / 恰好 4 个 0
    "00000",                # 多余的 0 只能成前导 0
    "500500500500",         # 恰好上界，长度 12
    "501500500500",         # 第一段 501 越界
    "500500500501",         # 最后一段 501 越界
    "5005005005000",        # 长度 13
    "1111", "11111", "111111111111",
    "100100100100",
    "0500500500",
    "123456789012345678901234567890",   # 长度 30
    "000000000000000000000000000000",   # 长度 30 全 0
]


def build_cases():
    cases, seen = [SAMPLE_IN], [SAMPLE_IN]
    for index in range(1, 40 - len(SPECIAL)):            # 原随机数据保留前 23 组
        for attempt in range(100):
            content = old_case(random.Random(24677 + index + attempt * 1000))
            if content not in seen: break
        seen.append(content); cases.append(content)
    return cases + [x + "\n" for x in SPECIAL]


def main():
    cases = build_cases()
    assert len(cases) == 40 and len(set(cases)) == 40 and all(valid(c) for c in cases)
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        for index, content in enumerate(cases):
            result = subprocess.run([sys.executable, handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            if index == 0: assert result.stdout.strip() == "2"
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()

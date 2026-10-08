import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'import math\n\n\ndef bacteria_war(harmful: int, beneficial: int) -> int:\n    hours = 0\n    while harmful > 0:\n        # Step 1: 有益菌消灭有害菌\n        harmful = max(0, harmful - beneficial)\n\n        # Step 2: 有害菌繁殖（在消灭之后进行）\n        harmful *= 2\n        harmful = min(harmful, 1_000_000)\n\n        # Step 3: 有益菌繁殖\n        beneficial = math.floor(beneficial * 1.05)\n\n        # Step 4: 时间增加\n        hours += 1\n    return hours\n\n\n# 主程序部分\ndef main():\n    n = int(input())\n    results = []\n    for _ in range(n):\n        h, b = map(int, input().split())\n        results.append(bacteria_war(h, b))\n    for res in results:\n        print(res)\n\n\nif __name__ == "__main__":\n    main()\n\n'
SAMPLE_IN = '4\n364 78\n289 48\n952 40\n966 23\n'
def generate_case(r):
    rows = [(r.randint(1, 100), r.randint(50, 1000)) for _ in range(r.randint(2, 8))]
    return str(len(rows)) + "\n" + "\n".join(f"{a} {b}" for a, b in rows) + "\n"

import math

LIMIT = 1_000_000


def _terminates(h, b):
    """按题面规则模拟，确认有害菌最终会被消灭（否则该组没有答案）。"""
    for _ in range(100000):
        if h <= 0:
            return True
        h = min(max(0, h - b) * 2, LIMIT)
        b = math.floor(b * 1.05)
    return False


def valid(text):
    """题面：第一行 n；随后 n 行，每行两个整数（有害菌、有益菌初始数量），一个空格分隔。
    提示 2：有害菌总数最大为一百万。数量取正整数，并要求过程能终止（否则无答案）。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if not lines[0].isdigit():
        return False
    n = int(lines[0])
    if n < 1 or len(lines) != n + 1:
        return False
    for line in lines[1:]:
        toks = line.split(" ")
        if len(toks) != 2 or not all(t.isdigit() and t[0] != "0" for t in toks):
            return False
        h, b = map(int, toks)
        if not (1 <= h <= LIMIT and b >= 1):
            return False
        if not _terminates(h, b):
            return False
    return True


def _pair(r, mode):
    while True:
        if mode == "big":            # 有害菌多、有益菌少：会撞上一百万上限，耗时长
            h, b = r.randint(10**5, LIMIT), r.randint(20, 2000)
        elif mode == "small_b":      # 有益菌 < 20 永不增长，只有 h < 2b 时才会终止
            b = r.randint(1, 19); h = r.randint(1, 2 * b - 1)
        elif mode == "mid":
            h, b = r.randint(1, LIMIT), r.randint(1, LIMIT)
        else:                        # "any"
            h = r.choice([r.randint(1, 1000), r.randint(1, LIMIT)])
            b = r.choice([r.randint(1, 100), r.randint(1, 10**4), r.randint(1, LIMIT)])
        if _terminates(h, b):
            return h, b


def special_case(index):
    """第 25..39 组：补有害菌接近一百万、有益菌很少/小于 20、h<=b 一小时即灭等分支。"""
    r = random.Random(296460 + index)
    k = index - 25
    if k == 0:
        rows = [(1, 1)]
    elif k == 1:
        rows = [(LIMIT, 20), (LIMIT, 21), (LIMIT, 1), (999999, 500000), (LIMIT, LIMIT)]
        rows = [x for x in rows if _terminates(*x)]
    elif k == 2:
        rows = [(2 * b - 1, b) for b in range(1, 20)] + [(b, b) for b in range(1, 20)]
    elif k == 3:
        rows = [(LIMIT, b) for b in range(20, 2020, 10)]
    elif k in (4, 5, 6):
        rows = [_pair(r, "big") for _ in range(300 * (k - 3))]
    elif k in (7, 8):
        rows = [_pair(r, "small_b") for _ in range(500)]
    elif k in (9, 10):
        rows = [_pair(r, "mid") for _ in range(1000)]
    else:
        rows = [_pair(r, "any") for _ in range(400 * (k - 10))]
    return str(len(rows)) + "\n" + "\n".join(f"{a} {b}" for a, b in rows) + "\n"


def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        for index in range(40):
            if index == 0: content = SAMPLE_IN
            elif index >= 25: content = special_case(index)
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(29646 + index + attempt * 1000))
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
            assert valid(content) and content not in seen[1:], index
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=60, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()

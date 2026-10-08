import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = '"""\nthe toggle function is used to flip the bit, which simplifies the flip function. \nusing a for-loop to iterate over the two cases: pressing the first button or not. \n"""\ndef toggle(bit):\n    return \'0\' if bit == \'1\' else \'1\'\n\ndef flip(lock, i):\n    if i > 0:\n        lock[i-1] = toggle(lock[i-1])\n    lock[i] = toggle(lock[i])\n    if i + 1 < len(lock):\n        lock[i+1] = toggle(lock[i+1])\n\ndef main():\n    s = input()\n    fin = input()\n    n = len(s)\n    ans = float(\'inf\')\n\n    for press_first in [False, True]:\n        tmp = 0\n        lock = list(s)\n        if press_first:\n            flip(lock, 0)\n            tmp += 1\n        for i in range(1, n):\n            if lock[i-1] != fin[i-1]:\n                flip(lock, i)\n                tmp += 1\n        if lock[n-1] == fin[n-1]:\n            ans = min(ans, tmp)\n\n    if ans == float(\'inf\'):\n        print("impossible")\n    else:\n        print(ans)\n\nif __name__ == "__main__":\n    main()\n'
SAMPLE_IN = '011\n000\n'
SAMPLE_OUT = '1\n'
def valid(text):
    """题面契约：两行，两个由 0、1 组成的等长字符串，长度 n 满足 1 <= n < 30。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if len(lines) != 2:
        return False
    a, b = lines
    return 1 <= len(a) < 30 and len(a) == len(b) and set(a + b) <= set("01")


def generate_case(r):
    n = r.randint(1, 29)      # 题面 1<=n<30（原写 30，随机未撞上）
    start = "".join(r.choice("01") for _ in range(n))
    target = "".join(r.choice("01") for _ in range(n))
    assert len(start) == len(target) == n and set(start + target) <= set("01")
    return start + "\n" + target + "\n"


def _solvable(a, b):
    n = len(a)
    for first in (0, 1):
        x = [int(c) ^ int(d) for c, d in zip(a, b)]
        def press(i):
            for k in (i - 1, i, i + 1):
                if 0 <= k < n: x[k] ^= 1
        if first: press(0)
        for i in range(1, n):
            if x[i - 1]: press(i)
        if not x[-1]:
            return True
    return False


def generate_extra(r, kind):
    # 2026-10 补强：原 19 组只有 1 组 impossible，没有 n=1，也没有「本来就相同、答案 0」的情形。
    if kind == "n1diff":
        return "0\n1\n"
    if kind == "n1same":
        return "1\n1\n"
    if kind == "same29":
        a = "".join(r.choice("01") for _ in range(29)); return a + "\n" + a + "\n"
    if kind == "imp2":
        return "00\n01\n"
    n = 29 if kind == "imp29" else r.choice([5, 8, 14, 26])
    while True:
        a = "".join(r.choice("01") for _ in range(n)); b = "".join(r.choice("01") for _ in range(n))
        if not _solvable(a, b):
            return a + "\n" + b + "\n"


EXTRA_KINDS = ["n1diff", "n1same", "same29", "imp2", "imp29", "impmid"]


def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        first_extra = 20 - len(EXTRA_KINDS)     # 组数保持 20（catalog 显式列出），末 6 组换成补强组
        for index in range(20):
            if index == 0:
                content = SAMPLE_IN
            elif index >= first_extra:
                content = generate_extra(random.Random(23570 * 7 + index), EXTRA_KINDS[index - first_extra])
                assert content not in seen
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(23570 + index + attempt * 1000))
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
            assert valid(content), index
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()

import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'def count_combinations(numbers, index, current_sum, count):\n    if index >= len(numbers):\n        if current_sum % 7 == 0:\n            return count + 1\n        else:\n            return count\n    \n    # 选择取当前位置的数\n    count = count_combinations(numbers, index + 1, current_sum + numbers[index], count)\n    \n    # 选择不取当前位置的数\n    count = count_combinations(numbers, index + 1, current_sum, count)\n    \n    return count\n\n\n# 主程序\nt = int(input())\nfor _ in range(t):\n    data = list(map(int, input().split()))\n    n = data[0]\n    numbers = data[1:]\n    \n    result = count_combinations(numbers, 0, 0, 0)\n    print(result)\n'
SAMPLE_IN = '3\n3 1 2 4\n5 1 2 3 4 5\n12 1 2 3 4 5 6 7 8 9 10 11 12\n'
SAMPLE_OUT = '2\n5\n586\n'
def valid(text):
    """题面契约：首行 t（t<10，即 1..9）；接着 t 行，每行首个数 n（1<=n<=16），后跟 n 个互不相同的正整数。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if not lines[0].isdigit():
        return False
    t = int(lines[0])
    if not 1 <= t < 10 or len(lines) != 1 + t:
        return False
    for line in lines[1:]:
        tok = line.split(" ")
        if not all(x.isdigit() for x in tok):
            return False
        v = list(map(int, tok))
        n = v[0]
        if not 1 <= n <= 16 or len(v) != n + 1:
            return False
        a = v[1:]
        if min(a) < 1 or len(set(a)) != n:
            return False
    return True


def generate_case(r):
    rows = []
    for _ in range(r.randint(2, 5)):
        n = r.randint(1, 15)
        values = r.sample(range(1, 100), n)
        rows.append(f"{n} " + " ".join(map(str, values)))
    return str(len(rows)) + "\n" + "\n".join(rows) + "\n"


def generate_extra(r, kind):
    # 2026-10 补强：原 19 组 t<=5、n<=15、值 <100，没有上限 n=16、t=9，也没有 n=1、全是 7 的倍数（答案 2^n）
    # 这些边界。末 6 组换成下面这些；值放宽到 10^5（和仍在 32 位以内）。
    if kind == "max":
        rows = [r.sample(range(1, 10**5), 16) for _ in range(9)]
    elif kind == "n1":
        rows = [[7], [3], [14], [1], [100000]]
    elif kind == "mult7":
        rows = [r.sample(range(7, 10**5, 7), 16), r.sample(range(7, 200, 7), 16), [7 * k for k in range(1, 17)]]
    elif kind == "t1":
        rows = [list(range(1, 17))]
    else:   # mixed：各种 n，含大量同余 7 的数
        rows = [r.sample(range(1, 10**5), n) for n in r.sample(range(1, 17), 9)]
    return str(len(rows)) + "\n" + "\n".join(f"{len(v)} " + " ".join(map(str, v)) for v in rows) + "\n"


EXTRA_KINDS = ["max", "max", "n1", "mult7", "t1", "mixed"]


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
                content = generate_extra(random.Random(23660 * 7 + index), EXTRA_KINDS[index - first_extra])
                assert content not in seen
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(23660 + index + attempt * 1000))
                    if content not in seen: break
                else: raise AssertionError("insufficient diversity")
            assert valid(content), index
            seen.append(content)
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()

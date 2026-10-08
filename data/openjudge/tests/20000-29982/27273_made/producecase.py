import random, re, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'import math\nt = int(input())\nfor _ in range(t):\n    n = int(input())\n    if n % 2 == 1:\n        sumv = (1 + n - 1)*(n-1)//2 + n\n    else:\n        sumv = (1 + n)*n//2\n    \n    maxp = int(math.log2(n))\n    \n    for i in range(maxp+1):\n        sumv -= 2*(2**i)\n    \n    print(sumv)\n'
SAMPLE_IN = '2\n4\n18864\n'
SAMPLE_OUT = '-4\n177869146\n'
def valid(text):
    """题面：第一行 t (1<=t<=100)，接下来 t 行各一个整数 n (1<=n<=10^6)。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if not all(re.fullmatch(r"[1-9][0-9]*", x) for x in lines):
        return False
    t = int(lines[0])
    if not (1 <= t <= 100) or len(lines) != t + 1:
        return False
    return all(1 <= int(x) <= 10**6 for x in lines[1:])


def generate_case(r, index):
    pows = [1 << k for k in range(20)]  # 2^19 = 524288 <= 10^6 < 2^20
    special = [1, 2, 3, 10**6, 10**6 - 1, 524288, 524287, 524289, 262144, 1023, 1024, 1025]
    if index <= 5:
        values = [r.randint(1, 10**6) for _ in range(r.randint(2, 12))]
    elif index <= 9:
        # 小 n 与 2 的幂附近（卡 log2 浮点误差/边界差一）
        values = []
        for _ in range(r.randint(10, 40)):
            p = r.choice(pows)
            values.append(max(1, min(10**6, p + r.choice([-1, 0, 0, 1]))))
        values += [r.randint(1, 20) for _ in range(5)]
    elif index <= 11:
        values = special + [r.randint(1, 10**6) for _ in range(r.randint(0, 20))]
    elif index == 12:
        values = [1]
    elif index == 13:
        values = [10**6]
    else:
        # 满规模：t=100，n 接近上限，卡逐个枚举
        values = [r.randint(9 * 10**5, 10**6) for _ in range(100)]
        values[r.randrange(100)] = 10**6
    r.shuffle(values)
    return str(len(values)) + "\n" + "\n".join(map(str, values)) + "\n"


def main():
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        seen = [SAMPLE_IN]
        for index in range(20):
            if index == 0: content = SAMPLE_IN
            else:
                for attempt in range(100):
                    content = generate_case(random.Random(27273 + index + attempt * 1000), index)
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

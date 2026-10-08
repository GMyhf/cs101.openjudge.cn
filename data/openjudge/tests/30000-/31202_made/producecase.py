import random
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent


def render(a, b):
    return f"{len(a)}\n" + " ".join(map(str, a)) + "\n" + " ".join(map(str, b)) + "\n"


def generate(i):
    if i == 0:
        return render([4, 8, 2, 6, 2], [4, 5, 4, 1, 3])
    if i == 1:
        return render([1, 3, 2, 4], [1, 3, 2, 4])
    if i == 2:
        return render([2, 2, 2, 2], [1, 1, 1, 1])
    if i == 3:
        return render([1, 1, 1, 1], [2, 2, 2, 2])
    rng = random.Random(2732900 + i)
    n = 2 + (i * 37) % 31
    if i == 19:
        # 满值域大规模；受单组 .in <= 1MB 限制，n 取 47000（O(n^2) 仍远超时限）
        n = 47000
    if i == 20:
        # 答案约 4.5e9，超出 32 位整数
        n = 95000
        a = [rng.randint(500000, 999999) for _ in range(n)]
        b = [rng.randint(1, 99) for _ in range(n)]
        return render(a, b)
    if i == 21:
        # 大规模、小值域，大量 a[i]+a[j] == b[i]+b[j] 的平局（严格大于）
        n = 90000
        a = [rng.randint(1, 999) for _ in range(n)]
        b = [rng.randint(1, 999) for _ in range(n)]
        return render(a, b)
    if i == 22:
        return render([10**9], [1])
    if i >= 19:
        a = [rng.randint(1, 10**9) for _ in range(n)]
        b = [rng.randint(1, 10**9) for _ in range(n)]
    else:
        a = [rng.randint(1, 10**9 if i % 3 == 0 else 100) for _ in range(n)]
        b = [rng.randint(1, 10**9 if i % 3 == 0 else 100) for _ in range(n)]
    return render(a, b)


def valid(text):
    """题面契约：第一行 n（1 <= n <= 200000）；第二、三行各恰 n 个整数，1 <= a[i], b[i] <= 10^9。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if len(lines) != 3:
        return False
    def ints(line):
        parts = line.split(" ")
        if not all(p.isdigit() and p[0] != "0" for p in parts):
            return None
        return list(map(int, parts))
    first = ints(lines[0])
    if not first or len(first) != 1 or not 1 <= first[0] <= 200000:
        return False
    n = first[0]
    for line in lines[1:]:
        v = ints(line)
        if v is None or len(v) != n or not all(1 <= x <= 10**9 for x in v):
            return False
    return True


def main():
    for i in range(40):
        case = generate(i)
        result = subprocess.run(
            ["python3", str(ROOT / "samplecode.py")],
            input=case, text=True, capture_output=True, check=True,
        ).stdout
        (ROOT / "data" / f"{i}.in").write_text(case, encoding="utf-8")
        (ROOT / "data" / f"{i}.out").write_text(result, encoding="utf-8")


if __name__ == "__main__":
    main()

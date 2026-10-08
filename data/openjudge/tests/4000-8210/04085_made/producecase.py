"""4085 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的数据。

第 0 组是题面样例；1..39 组沿用原生成器（n<=80，值 0..10000）；
40 组起补满规模 n=1e5、大量重复、多空格分隔、边界值等。
"""
import random
import subprocess
import tempfile
from pathlib import Path

SAMPLE_IN = '3\n4 4 2\n'
REFERENCE_SOURCE='import sys\na=list(map(int,sys.stdin.read().split())); n=a[0]\nprint(" ".join(map(str,sorted(set(a[1:n+1])))))'


def valid(text):
    """题面契约：共 2 行；第一行 n（n<=1e5），第二行 n 个整数，
    整数之间以若干个空格分隔（题面原话“可能有若干个空格”），所有整数不超过 1e4。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if len(lines) != 2:
        return False
    head = lines[0].split()
    if len(head) != 1:
        return False
    try:
        n = int(head[0])
        vals = [int(t) for t in lines[1].split(" ") if t != ""]
    except ValueError:
        return False
    if set(lines[1]) - set("-0123456789 "):
        return False
    return 1 <= n <= 10 ** 5 and len(vals) == n and all(v <= 10 ** 4 for v in vals)


def g4085(r):
    n = r.randint(1, 80)
    return f"{n}\n" + " ".join(str(r.randint(0, 10_000)) for _ in range(n)) + "\n"


def fmt(vals, r=None, maxgap=1):
    if r is None or maxgap == 1:
        body = " ".join(map(str, vals))
    else:
        body = "".join(str(v) + " " * r.randint(1, maxgap) for v in vals).rstrip(" ")
    return f"{len(vals)}\n{body}\n"


def extra_cases():
    r = random.Random(4085 * 7 + 1)
    N = 10 ** 5
    cases = []
    cases.append(fmt([10000]))                                     # n=1，上界值
    cases.append(fmt([0, 0]))                                      # 全重复
    cases.append(fmt([7] * N))                                     # 满规模全相同
    cases.append(fmt([r.randint(0, 10000) for _ in range(N)]))     # 满规模随机，几乎覆盖全部值域
    cases.append(fmt(list(range(10000, -1, -1)) + [r.randint(0, 10000) for _ in range(N - 10001)]))
    cases.append(fmt([r.randint(0, 50) for _ in range(N)]))        # 满规模、值域很窄
    cases.append(fmt([r.randint(0, 10000) for _ in range(N)], r, 3))   # 多空格分隔
    cases.append(fmt([r.randint(0, 10000) for _ in range(500)], r, 5))
    cases.append(fmt([4, 4, 2, 2, 10000, 0, 10000], r, 4))
    cases.append(fmt(sorted(r.randint(0, 10000) for _ in range(N // 2))))
    return cases


def build_cases():
    cases = []
    seen = [SAMPLE_IN]
    for index in range(40):
        if index == 0:
            content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = g4085(random.Random(4085 + index + attempt * 1000))
                if content not in seen:
                    break
            else:
                raise AssertionError("insufficient diversity")
        seen.append(content)
        cases.append(content)
    return cases + extra_cases()


def main():
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE)
        handle.flush()
        for index, content in enumerate(build_cases()):
            assert valid(content), index
            result = subprocess.run(["python3", handle.name], input=content, text=True,
                                    capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()

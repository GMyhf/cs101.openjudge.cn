import random,subprocess,tempfile
from pathlib import Path
REFERENCE_SOURCE='import sys\na=sys.stdin.read().split(); t=int(a[0])\nprint("\\n".join(str(int(x,16)) for x in a[1:t+1]))'
SAMPLE_IN='4\nA\nF\nFFFE\n10001\n'

def valid(text):
    """题面契约：第一行 T；其后恰 T 行，每行一个十六进制无符号正整数：位数 1..8，
    只含 0-9 与大写 A-F，无前导 0（正整数故不为 0），对应十进制小于 2^31。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if not lines[0].isdigit() or lines[0][0] == "0":
        return False
    t = int(lines[0])
    if len(lines) != t + 1:
        return False
    for s in lines[1:]:
        if not 1 <= len(s) <= 8 or set(s) - set("0123456789ABCDEF") or s[0] == "0":
            return False
        if not 1 <= int(s, 16) < 2**31:
            return False
    return True

def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 15):    # 小规模随机：位数 1..8，值域 [1, 2^31)
        r = random.Random(4003 + i); t = r.randint(1, 8); v = []
        for _ in range(t):
            L = r.randint(1, 8)
            v.append(r.randint(16 ** (L - 1), min(16 ** L, 2 ** 31) - 1))
        cases.append(f"{t}\n" + "\n".join(f"{x:X}" for x in v) + "\n")
    r = random.Random(400300)
    edge = [1, 9, 10, 15, 16, 255, 256, 0xABCDEF, 0x10000000, 0x7FFFFFFF, 0x7FFFFFFE, 0x0FFFFFFF, 0x1000000, 0x10, 0x100, 2 ** 31 - 16]
    cases.append(f"{len(edge)}\n" + "\n".join(f"{x:X}" for x in edge) + "\n")
    cases.append("1\n7FFFFFFF\n")
    cases.append("1\n1\n")
    cases.append("6\nA\nB\nC\nD\nE\nF\n")
    cases.append("16\n" + "\n".join(f"{x:X}" for x in range(1, 17)) + "\n")
    cases.append("8\n" + "\n".join("1" + "0" * k for k in range(8)) + "\n")
    cases.append("7\n" + "\n".join("F" * k for k in range(1, 8)) + "\n")
    while len(cases) < 40:
        k = len(cases); t = [10, 100, 1000, 10000, 50000][k % 5]
        if k % 3 == 0: v = [r.randint(1, 2 ** 31 - 1) for _ in range(t)]
        elif k % 3 == 1: v = [r.randint(0x10000000, 2 ** 31 - 1) for _ in range(t)]
        else:
            v = []
            for _ in range(t):
                L = r.randint(1, 8); v.append(r.randint(16 ** (L - 1), min(16 ** L, 2 ** 31) - 1))
        c = f"{t}\n" + "\n".join(f"{x:X}" for x in v) + "\n"
        if c not in cases: cases.append(c)
    return cases

def main():
    cases = build_cases()
    assert len(cases) == 40 and len(set(cases)) == 40
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE); handle.flush()
        root = Path(__file__).parent / "data"
        for index, content in enumerate(cases):
            assert valid(content), index
            result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")

if __name__ == "__main__":
    main()

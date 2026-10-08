"""3718 位操作练习 测试数据生成器：固定种子，重跑可逐字节复现 data/。

题面约束：第一行整数 n（0 < n < 300000），后面 n 行，每行两个不大于 65535 的非负整数。

2026-10 审计修正：原数据 n 最大只有 50，b 一半是纯随机数（几乎都是 popcount 不同的
NO），只数 1 的个数、漏判循环 0 位 / 15 位、不做 16 位截断的错误写法都抓不住，
效率也完全没考。现在：
  - 加 n=1 的边界组（0 0、65535 65535、1 与 32768 等）；
  - 随机组里混入「循环移位 k∈[0,15]」「1 的个数相同但不是循环移位」「a==b」
    「周期串 0x5555/0xAAAA/0x0F0F…」几类；
  - 大组 n=80000（题面上限 299999 的文本约 3.6MB，超出单组 1MB 的数据体积限制，
    所以取 1MB 以内能放下的最大规模）。
"""
import random
import re
import subprocess
import tempfile
from pathlib import Path

REFERENCE_SOURCE = 'import sys\na=list(map(int,sys.stdin.buffer.read().split())); n=a[0] if a else 0; out=[]\nfor i in range(min(n,(len(a)-1)//2)):\n    x,y=a[1+2*i],a[2+2*i]\n    bits=f"{x:016b}"\n    out.append("YES" if any(bits[k:]+bits[:k]==f"{y:016b}" for k in range(16)) else "NO")\nprint("\\n".join(out))'
SAMPLE_IN = '4\n2 4\n9 18\n45057 49158\n7 12\n'
SAMPLE_OUT = 'YES\nYES\nYES\nNO\n'
LINE_RE = re.compile(r"(0|[1-9]\d{0,4}) (0|[1-9]\d{0,4})")


def valid(text):
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if not re.fullmatch(r"[1-9]\d*", lines[0]):
        return False
    n = int(lines[0])
    if not 0 < n < 300000 or len(lines) != n + 1:
        return False
    for line in lines[1:]:
        m = LINE_RE.fullmatch(line)
        if not m or int(m.group(1)) > 65535 or int(m.group(2)) > 65535:
            return False
    return True


def rot(a, k):
    return ((a << k) | (a >> (16 - k))) & 65535 if k else a


def is_rot(a, b):
    return any(rot(a, k) == b for k in range(16))


def same_pop_not_rot(r, a):
    bits = [i for i in range(16)]
    for _ in range(50):
        pos = r.sample(bits, bin(a).count("1"))
        b = sum(1 << p for p in pos)
        if not is_rot(a, b):
            return b
    return None


PERIODIC = [0x5555, 0xAAAA, 0x0F0F, 0xF0F0, 0x3333, 0xCCCC, 0x00FF, 0xFF00, 0x0101, 0x8888, 0, 65535]


def pair(r):
    t = r.random()
    a = r.randint(0, 65535)
    if t < .35:
        b = rot(a, r.randint(0, 15))
    elif t < .40:
        b = rot(a, r.choice([1, 15]))
    elif t < .65:
        b = same_pop_not_rot(r, a)
        if b is None:
            b = rot(a, r.randint(0, 15))
    elif t < .72:
        b = a
    elif t < .80:
        a = r.choice(PERIODIC)
        b = rot(a, r.randint(0, 15)) if r.random() < .6 else r.choice(PERIODIC)
    elif t < .85:
        a = 1 << r.randint(0, 15)
        b = 1 << r.randint(0, 15)
    else:
        b = r.randint(0, 65535)
    if r.random() < .5:
        a, b = b, a
    return a, b


def make(pairs):
    return f"{len(pairs)}\n" + "".join(f"{a} {b}\n" for a, b in pairs)


def build_cases():
    cases = [SAMPLE_IN]
    for p in [(0, 0), (65535, 65535), (0, 65535), (1, 32768), (32768, 1), (0x5555, 0xAAAA),
              (65534, 32767), (1, 3)]:
        cases.append(make([p]))
    k = 0
    while len(cases) < 34:
        k += 1
        r = random.Random(3718 * 100 + k)
        n = r.choice([r.randint(2, 20), r.randint(20, 300), r.randint(300, 5000)])
        c = make([pair(r) for _ in range(n)])
        if c not in cases:
            cases.append(c)
    for k, n in enumerate([20000, 50000, 80000, 80000, 80000, 80000]):
        r = random.Random(3718 * 1000 + k)
        cases.append(make([pair(r) for _ in range(n)]))
    return cases


def main():
    cases = build_cases()
    assert cases[0] == SAMPLE_IN
    assert all(valid(c) for c in cases) and len(set(cases)) == len(cases)
    assert all(len(c.encode()) <= 1 << 20 for c in cases)
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE)
        handle.flush()
        for index, content in enumerate(cases):
            result = subprocess.run(["python3", handle.name], input=content, text=True,
                                    capture_output=True, timeout=60, check=True)
            if index == 0:
                assert result.stdout.split() == SAMPLE_OUT.split()
            (root / f"{index}.in").write_text(content, encoding="utf-8")
            (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")


if __name__ == "__main__":
    main()

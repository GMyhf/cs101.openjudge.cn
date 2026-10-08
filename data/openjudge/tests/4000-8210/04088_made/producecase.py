"""4088 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的数据。

第 0 组是题面样例；1..39 组沿用原生成器（n<=20，值 <100）；40 组起补大规模、
C 为空、B 全在 A 内、B 与 A 不交、B 落在 A 两端之外、含 0 与大值等。
题面上限 n=1e6，但单组 .in 需 <=1MB，故大组 n 取到 9 万~15 万；m 按 O(log n) 取 1..40。
2026-10 体积收口（data/ 合计 ≤10MB）：满规模只留 45（值域 1e9、n=9 万）、47（B 全在 A 内）、
49（混合、含 0 与越过最大值）三组，46/48/50 缩到 3 万~5 万。
"""
import random
import subprocess
from pathlib import Path

I = '8 1 3 5 6 8 10 12 30\n3 1 3 7\n'


def valid(text):
    """题面契约：共 2 行；第 1 行 n 后跟 A 的 n 个非负整数，第 2 行 m 后跟 B 的 m 个非负整数；
    两个集合（元素互异）均按从小到大给出，n<=1e6。m=O(log n) 不是具体数值，不核。"""
    if not text.endswith("\n"):
        return False
    lines = text[:-1].split("\n")
    if len(lines) != 2:
        return False
    for idx, line in enumerate(lines):
        t = line.split(" ")
        if not all(x.isdigit() for x in t):
            return False
        cnt = int(t[0])
        vals = [int(x) for x in t[1:]]
        if len(vals) != cnt:
            return False
        if idx == 0 and cnt > 10 ** 6:
            return False
        if any(a >= b for a, b in zip(vals, vals[1:])):
            return False
    return True


def g4088(r):
    A = sorted(r.sample(range(100), r.randint(6, 20)))
    B = sorted(r.sample(range(100), r.randint(1, 8)))
    return f"{len(A)} " + " ".join(map(str, A)) + f"\n{len(B)} " + " ".join(map(str, B)) + "\n"


def fmt(A, B):
    A = sorted(A)
    B = sorted(B)
    return " ".join(map(str, [len(A)] + A)) + "\n" + " ".join(map(str, [len(B)] + B)) + "\n"


def extra_cases():
    r = random.Random(4088 * 7 + 1)
    cases = []
    cases.append(fmt([0], [0]))                            # C 为空：输出空行
    cases.append(fmt([1, 5, 9], [1, 5, 9]))                # A==B
    cases.append(fmt([0], [1]))
    cases.append(fmt([5, 6, 7], [0, 100]))                 # B 落在 A 两端之外
    cases.append(fmt([0, 2, 4], [10 ** 9]))
    # 大规模、值域 1e9
    for m, n in ((17, 90000), (30, 30000)):
        A = r.sample(range(10 ** 9 + 1), n)
        Aset = set(A)
        inA = r.sample(A, m // 2)
        B = set(inA)
        while len(B) < m:
            x = r.randint(0, 10 ** 9)
            if x not in Aset:
                B.add(x)
        cases.append(fmt(A, B))
    # 大规模、稠密值域；B 全在 A 内 / 与 A 不交 / 混合并含 0 和超过 A 最大值的元素
    N = 150000
    A = sorted(r.sample(range(300000), N))
    cases.append(fmt(A, r.sample(A, 17)))
    A2 = sorted(r.sample(range(100000), 50000))           # 与 A 不交一组缩到 5 万
    A2set = set(A2)
    out2 = [x for x in range(100000) if x not in A2set]
    cases.append(fmt(A2, r.sample(out2, 17)))
    Aset = set(A)
    out = [x for x in range(300000) if x not in Aset]
    B = set(r.sample(A, 8)) | set(r.sample(out, 8)) | {0, 300000, 300001}
    cases.append(fmt(A, B))
    A = list(range(1, 50001))                              # 连续整数，B 首尾越界
    cases.append(fmt(A, [0, 1, 2, 25000, 49999, 50000, 50001, 50002]))
    # 中等规模随机
    for _ in range(6):
        n = r.randint(1000, 20000)
        A = r.sample(range(10 * n), n)
        m = r.randint(1, 15)
        cases.append(fmt(A, r.sample(range(10 * n + 50), m)))
    return cases


def build_cases():
    return [I if i == 0 else g4088(random.Random(4088 + i)) for i in range(40)] + extra_cases()


def main():
    root = Path(__file__).parent
    binary = root / "reference"
    subprocess.run(["g++", "-std=c++17", "-O2", str(root / "samplecode.cpp"), "-o", str(binary)], check=True)
    try:
        for i, c in enumerate(build_cases()):
            assert valid(c), i
            p = subprocess.run([str(binary)], input=c, text=True, capture_output=True, check=True)
            (root / "data" / f"{i}.in").write_text(c)
            (root / "data" / f"{i}.out").write_text(p.stdout)
    finally:
        binary.unlink()


if __name__ == "__main__":
    main()

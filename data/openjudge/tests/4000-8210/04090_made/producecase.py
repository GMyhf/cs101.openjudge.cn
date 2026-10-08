"""4090 超级备忘录 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 40 组数据。

2026-10 审计：原数据 n≤10、每组仅 12 个操作，远离题面上限 n、M≤100000，
改为小规模（可暴力核对）+ 中规模 + 满规模三档，并单独构造各操作的边界。
答案由 samplecode.cpp（Treap）给出；小中规模组另有列表暴力模拟核对。
"""
import random
import subprocess
from pathlib import Path

SAMPLE_IN = '5\n1 \n2 \n3 \n4 \n5\n2\nADD 2 4 1\nMIN 4 5\n'
OPS = ("ADD", "REVERSE", "REVOLVE", "INSERT", "DELETE", "MIN")


def valid(text):
    """题面契约：n（≤100000）、n 个数、M（≤100000）、M 行操作；下标须落在当前序列内。"""
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines.pop()

    def ints(tokens):
        out = []
        for s in tokens:
            if not s.lstrip("-").isdigit() or s.startswith("+"):
                return None
            out.append(int(s))
        return out

    if not lines:
        return False
    head = ints(lines[0].split())
    if head is None or len(head) != 1 or not 1 <= head[0] <= 100000:
        return False
    n = head[0]
    if len(lines) < n + 2:
        return False
    for line in lines[1:n + 1]:
        v = ints(line.split())
        if v is None or len(v) != 1:
            return False
    m = ints(lines[n + 1].split())
    if m is None or len(m) != 1 or not 0 <= m[0] <= 100000:
        return False
    m = m[0]
    if len(lines) != n + 2 + m:
        return False
    length = n
    arity = {"ADD": 3, "REVERSE": 2, "REVOLVE": 3, "INSERT": 2, "DELETE": 1, "MIN": 2}
    for line in lines[n + 2:]:
        parts = line.split()
        if not parts or parts[0] not in arity or len(parts) != arity[parts[0]] + 1:
            return False
        a = ints(parts[1:])
        if a is None:
            return False
        op = parts[0]
        if op in ("ADD", "REVERSE", "REVOLVE", "MIN"):
            if not 1 <= a[0] <= a[1] <= length:
                return False
        elif op == "INSERT":
            if not 1 <= a[0] <= length:
                return False
            length += 1
        else:  # DELETE
            if not 1 <= a[0] <= length or length == 1:
                return False
            length -= 1
    return True


LIMIT = 1_000_000  # 每组 .in 不超过 1MB


def gen(r, n, m, vlo, vhi, dlo, dhi, tmax, weights, span=None, limit=LIMIT):
    """随机生成一组：weights 为六种操作的权重；span 限制区间长度上界（None 为不限）。
    操作数最多 m 个，同时受 1MB 文件上限约束（写满为止），最后一个操作总是 MIN。"""
    length = n
    vals = [r.randint(vlo, vhi) for _ in range(n)]
    ops = []
    size = sum(len(str(v)) + 1 for v in vals) + len(str(n)) + 1 + 7
    for k in range(m):
        if size > limit - 40:
            break
        z = r.choices(OPS, weights)[0]
        if k == m - 1 or size > limit - 80:
            z = "MIN"
        if z == "DELETE" and length == 1:
            z = "INSERT"
        if z == "DELETE":
            ops.append(f"DELETE {r.randint(1, length)}")
            length -= 1
            size += len(ops[-1]) + 1
            continue
        elif z == "INSERT":
            ops.append(f"INSERT {r.randint(1, length)} {r.randint(vlo, vhi)}")
            length += 1
            size += len(ops[-1]) + 1
            continue
        else:
            if span is None or r.random() < 0.2:
                x = r.randint(1, length)
                y = r.randint(x, length)
            else:
                ln = r.randint(1, min(span, length))
                x = r.randint(1, length - ln + 1)
                y = x + ln - 1
            if r.random() < 0.05:
                x, y = 1, length
            if z == "ADD":
                ops.append(f"ADD {x} {y} {r.randint(dlo, dhi)}")
            elif z == "REVERSE":
                ops.append(f"REVERSE {x} {y}")
            elif z == "REVOLVE":
                t = r.choice([0, y - x + 1, r.randint(0, tmax), r.randint(0, tmax)])
                ops.append(f"REVOLVE {x} {y} {t}")
            else:
                ops.append(f"MIN {x} {y}")
        size += len(ops[-1]) + 1
    assert ops[-1].startswith("MIN")
    return f"{n}\n" + "\n".join(map(str, vals)) + f"\n{len(ops)}\n" + "\n".join(ops) + "\n"


def edge_case():
    """手工边界：单元素序列、x=y、整段、轮换次数为区间长度倍数/0、插到末尾、删到只剩一个。"""
    ops = [
        "MIN 1 1", "INSERT 1 7", "MIN 1 2", "REVOLVE 1 2 1", "MIN 1 1", "REVOLVE 1 2 4",
        "MIN 2 2", "ADD 1 2 -10", "MIN 1 2", "REVERSE 1 2", "MIN 1 1", "DELETE 1", "MIN 1 1",
        "INSERT 1 -100", "INSERT 2 50", "REVOLVE 1 3 1000000000", "MIN 1 1", "MIN 3 3",
        "ADD 2 2 0", "REVERSE 2 2", "REVOLVE 3 3 5", "MIN 2 3", "DELETE 3", "DELETE 2", "MIN 1 1",
    ]
    return "1\n5\n" + f"{len(ops)}\n" + "\n".join(ops) + "\n"


def build_cases():
    r = random.Random(4090)
    w_all = [2, 2, 2, 1, 1, 3]
    cases = [SAMPLE_IN, edge_case()]
    # 2-19 小规模随机（n≤12，暴力可核）
    for i in range(2, 20):
        cases.append(gen(r, r.randint(1, 12), r.randint(5, 40), -9, 9, -3, 3, 30, w_all))
    # 20-27 中规模（n、M≈1000~3000）
    for i in range(20, 28):
        cases.append(gen(r, r.randint(500, 3000), r.randint(1000, 3000), -10 ** 6, 10 ** 6,
                         -1000, 1000, 10 ** 9, w_all, span=r.choice([None, 50])))
    # 28-39 大规模，各有侧重。题面上限 n、M≤100000，但两者同时取满时输入约 2MB，
    # 受 1MB 文件上限约束：偶数组 n=100000、操作写满 1MB（约 3 万个），奇数组 n 较小、M 尽量大。
    big = [
        [2, 2, 2, 1, 1, 3],   # 均衡
        [5, 0, 0, 0, 0, 5],   # 只 ADD/MIN：线段树也能做
        [0, 5, 0, 0, 0, 5],   # 翻转 + 查询
        [0, 0, 5, 0, 0, 5],   # 轮换（T 最大 1e9，逐次轮换会超时）
        [1, 1, 1, 5, 0, 2],   # 大量插入
        [1, 1, 1, 0, 5, 2],   # 大量删除
    ]
    # 体积收口（data/ 合计 ≤10MB）：只有 28（均衡、n=1e5）、31（翻转）、33（轮换）三组写满 1MB，
    # 其余大组文件上限压到 45 万字节，偶数组 n 相应降到 4 万。
    full = {28, 31, 33}
    for i in range(28, 40):
        wts = big[(i - 28) // 2]
        if i % 2 == 0:
            n, m = (100000 if i in full else 40000), 100000
        else:
            n, m = r.randint(9000, 12000), 100000
        tmax = 10 ** 9 if wts[2] == 5 else 10 ** 5
        cases.append(gen(r, n, m, -999, 999, -99, 99, tmax, wts,
                         span=None if i % 4 < 2 else 3000,
                         limit=LIMIT if i in full else 450_000))
    return cases


def main():
    root = Path(__file__).parent
    binary = root / "reference"
    subprocess.run(["g++", "-std=c++17", "-O2", str(root / "samplecode.cpp"), "-o", str(binary)], check=True)
    try:
        cases = build_cases()
        assert cases[0] == SAMPLE_IN, "第 0 组必须是题面样例"
        (root / "data").mkdir(exist_ok=True)
        for i, c in enumerate(cases):
            assert valid(c), f"第 {i} 组不满足题面约束"
            p = subprocess.run([str(binary)], input=c, text=True, capture_output=True, check=True)
            (root / "data" / f"{i}.in").write_text(c)
            (root / "data" / f"{i}.out").write_text(p.stdout)
    finally:
        binary.unlink(missing_ok=True)


if __name__ == "__main__":
    main()

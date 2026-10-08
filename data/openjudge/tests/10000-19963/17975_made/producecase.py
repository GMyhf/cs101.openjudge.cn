"""17975 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001d
生成器与循环取自 scripts/build_001d.py（批次 001d），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 17975
SAMPLE_IN = '5 11\n24 13 35 15 14\n'
SAMPLE_OUT = '2 3 1 4 7\n'
REFERENCE_SOURCE = 'def quadratic_probe_insert(keys, M):\n    table = [None] * M\n    result = []\n\n    for key in keys:\n        pos = key % M\n        if table[pos] is None or table[pos] == key:\n            table[pos] = key\n            result.append(pos)\n            continue\n\n        # 否则开始二次探查\n        i = 1\n        instered = False\n        while not instered:\n            for sign in [1, -1]:\n                new_pos = (pos + sign * (i ** 2)) % M\n                if table[new_pos] is None or table[new_pos] == key:\n                    table[new_pos] = key\n                    result.append(new_pos)\n                    instered = True\n                    break\n\n            i += 1  # 探查次数增加\n\n    return result\n\n\nimport sys\n\ninput = sys.stdin.read\ndata = input().split()\nN = int(data[0])\nM = int(data[1])\nkeys = list(map(int, data[2:2 + N]))\n\npositions = quadratic_probe_insert(keys, M)\nprint(*positions)\n\n'

def is_prime(x):
    return x>=2 and all(x%d for d in range(2,int(x**0.5)+1))

def next_prime(x):
    y=max(2,x)
    while not is_prime(y): y+=1
    return y

def valid(text):
    """题面：第一行两个正整数 N（N<=1000）和 M（一般为 >=2N 的最小素数）；第二行 N 个整型关键字。
    硬保证只有：散列表长 M 为素数（题面「素数P」）且不小于关键字总数的 2 倍。
    题面未限定关键字取值范围与互异性。"""
    if not text.endswith("\n"): return False
    lines=text[:-1].split("\n")
    if len(lines)!=2: return False
    try:
        head=lines[0].split()
        if len(head)!=2 or lines[0]!=" ".join(head): return False
        n,m=map(int,head)
        if not (1<=n<=1000) or m<2*n or not is_prime(m): return False
        keys=lines[1].split()
        if len(keys)!=n or lines[1]!=" ".join(keys): return False
        for x in keys: int(x)
    except ValueError:
        return False
    return True

def g17975(r,kind):
    if kind=="small":                         # 原有形状：小表、小关键字，冲突与重复较多
        m=r.choice([11,13,17,19,23]); n=r.randint(2,m//2)
        return f"{n} {m}\n"+" ".join(str(r.randint(-100,100)) for _ in range(n))+"\n"
    n=r.choice([1000,1000,r.randint(300,1000)]) if kind!="mid" else r.randint(20,300)
    m=next_prime(2*n)
    if r.random()<0.25: m=next_prime(m+1)    # 「一般为」：偶尔用更大的素数
    if kind=="cluster":                       # 同余关键字扎堆，探查序列拉得很长
        res=[r.randrange(m) for _ in range(r.randint(1,3))]
        keys=[r.choice(res)+m*r.randint(-1000,1000) for _ in range(n)]
    elif kind=="dup":                         # 大量重复关键字：重复的关键字输出同一位置
        pool=[r.randint(-10**6,10**6) for _ in range(max(1,n//4))]
        keys=[r.choice(pool) for _ in range(n)]
    else:
        lo=r.choice([0,-10**6,-10**9]); hi=r.choice([10**6,10**9])
        keys=[r.randint(lo,hi) for _ in range(n)]
    return f"{n} {m}\n"+" ".join(map(str,keys))+"\n"

KINDS=["small"]*5+["mid"]*3+["big"]*4+["cluster"]*4+["dup"]*2
FIXED=["1 2\n-7\n"]

def build_cases():
    cases = [SAMPLE_IN] + FIXED
    for i, kind in enumerate(KINDS, 1):
        for attempt in range(100):
            value = g17975(random.Random(NUMBER + i + attempt * 1000), kind)
            if value not in cases:
                cases.append(value)
                break
        else:
            raise AssertionError("生成器多样性不足")
    assert len(cases) == 20 and all(valid(c) for c in cases)
    return cases

def solve_reference(content):
    with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
        handle.write(REFERENCE_SOURCE)
        handle.flush()
        result = subprocess.run(["python3", handle.name], input=content, text=True,
                                capture_output=True, timeout=120, check=True)
    return result.stdout


def main():
    cases = build_cases()
    assert cases[0] == SAMPLE_IN, "第 0 组必须是题面样例"
    assert solve_reference(SAMPLE_IN).split() == SAMPLE_OUT.split(), "参考解法跑不出样例输出"
    root = Path(__file__).parent / "data"
    root.mkdir(exist_ok=True)
    for index, content in enumerate(cases):
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(solve_reference(content), encoding="utf-8")


if __name__ == "__main__":
    main()

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

def g17975(r):
    m=r.choice([11,13,17,19,23]); n=r.randint(2,m//2); return f"{n} {m}\n"+" ".join(str(r.randint(-100,100)) for _ in range(n))+"\n"

def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g17975(random.Random(NUMBER + i + attempt * 1000))
            if value not in cases:
                cases.append(value)
                break
        else:
            raise AssertionError("生成器多样性不足")
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

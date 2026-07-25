"""17968 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001d
生成器与循环取自 scripts/build_001d.py（批次 001d），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 17968
SAMPLE_IN = '4 5\n24 13 66 77\n'
SAMPLE_OUT = '4 3 1 2\n'
REFERENCE_SOURCE = 'def insert_hash_table(keys, M):\n    table = [0.5] * M  # 用 0.5 表示空位\n    result = []\n\n    for key in keys:\n        index = key % M\n        i = index\n\n        while True:\n            if table[i] == 0.5 or table[i] == key:\n                result.append(i)\n                table[i] = key\n                break\n            i = (i + 1) % M\n\n    return result\n\n# 使用标准输入读取数据\nimport sys\ninput = sys.stdin.read\ndata = input().split()\n\nN = int(data[0])\nM = int(data[1])\nkeys = list(map(int, data[2:2 + N]))\n\npositions = insert_hash_table(keys, M)\nprint(*positions)\n\n'

def next_prime(x):
    y=max(2,x)
    while any(y%d==0 for d in range(2,int(y**0.5)+1)): y+=1
    return y

def g17968(r):
    n=r.choice([1,2,3,5,10,50,200,999,1000]) if r.random()<0.5 else r.randint(1,1000)
    lo,hi=(-100,100) if n<=10 else (-10**6,10**6)
    return f"{n} {next_prime(n)}\n"+" ".join(str(r.randint(lo,hi)) for _ in range(n))+"\n"

def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g17968(random.Random(NUMBER + i + attempt * 1000))
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

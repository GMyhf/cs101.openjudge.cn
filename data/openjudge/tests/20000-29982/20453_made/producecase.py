"""20453 测试数据生成器：固定种子，重跑可逐字节复现 data/ 下的 20 组数据。

出处：build_001d
生成器与循环取自 scripts/build_001d.py（批次 001d），保持同一形状；
不再内嵌 CASES —— 输入由种子重新生成，避免同一份数据在仓库里存两遍。
"""
import random
import subprocess
import tempfile
from pathlib import Path

NUMBER = 20453
SAMPLE_IN = '1 1 1\n2\n'
SAMPLE_OUT = '2\n'
REFERENCE_SOURCE = 'def subarray_sum(nums, k):\n    count = 0\n    sums = 0\n    d = dict()\n    d[0] = 1\n\n    for i in range(len(nums)):\n        sums += nums[i]\n        count += d.get(sums - k, 0)\n        d[sums] = d.get(sums, 0) + 1\n\n    return count\n\nnums = list(map(int, input().split()))\nk = int(input().strip())\nprint(subarray_sum(nums, k))\n'

def g20453(r):
    a=[r.randint(-5,8) for _ in range(r.randint(2,20))]; return " ".join(map(str,a))+"\n"+str(r.randint(-8,15))+"\n"

def build_cases():
    cases = [SAMPLE_IN]
    for i in range(1, 20):
        for attempt in range(100):
            value = g20453(random.Random(NUMBER + i + attempt * 1000))
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
